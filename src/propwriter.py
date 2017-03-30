from __future__ import absolute_import
from __future__ import print_function
import sys
import os
import re

from pyverilog.vparser.ast import *
import pyverilog.utils.util as util
import pyverilog.utils.verror as verror
import pyverilog.utils.signaltype as signaltype
from pyverilog.utils.scope import ScopeLabel, ScopeChain
from pyverilog.dataflow.dataflow import *
from pyverilog.dataflow.visit import *
from pyverilog.dataflow.optimizer import VerilogOptimizer
import pyverilog.dataflow.reorder as reorder
import pyverilog.dataflow.replace as replace
from pyverilog.dataflow.moduleinfo import *
from pyverilog.dataflow.frames import *
from svwriter import *

def dictunion(dict1, dict2):
    z=dict1.copy()
    for key in dict2.keys():
        if key in z.keys():
            z[key]=list(set(z[key]) | set(dict2[key]))
    return z

def dictintersect(dict1, dict2):
    z={}
    for key in dict2.keys():
        if key in dict1.keys():
            z[key]=list(set(z[key]) & set(dict2[key]))
    return z

def listintersect(list1, list2):
    newlist = list(set(list1) & set(list2))
    if newlist:
        return True
    else:
        return False

class PropWriter(NodeVisitor):
    def __init__(self, moduleinfotable, top, frames, dataflow,exhaustive=False, getlocal=True, getglobal=True, buf=sys.stdout, unique=False):
        self.moduleinfotable=moduleinfotable
        self.top = top
        self.frames = frames
        self.dataflow = dataflow
        self.binddict = self.dataflow.getBinddict()
        self.optimizer = VerilogOptimizer(dataflow.getTerms())
        self.writer = SVWriter(unique)
        self.moduleinfotable.setCurrent(top)
        self.chain = ScopeChain()
        self.chain += ScopeLabel(top, 'module')
        self.buf=buf
        self.cond=[]
        self.exhaustive=exhaustive
        self.getlocal=getlocal
        self.getglobal=getglobal

    def start_visit(self):
        oldpath=os.getcwd()
        path=os.getcwd()+'/SVA/'
        if os.path.exists(path):
            print("SVA already exists")
            sys.exit()
        os.mkdir(path)
        os.chdir(path)
        self.visit(self.moduleinfotable.getDefinition(self.top))
        os.chdir(oldpath)

    def visit_ModuleDef(self, node):
        for const in self.frames.getConsts(self.chain).keys():
            for bind in self.binddict[const]:
                self.optimizer.setConstant(const, DFEvalValue(bind.tree.eval()))

        filename=str(self.chain)+'_test'
        filename=filename.replace(".","_")
        f=open(filename + '.sv',"w")
        f.write('module ' + filename + '(\n')
        string=''
        for signal in self.frames.getSignals(self.chain).keys():
            string+='input '
            msb, lsb, lenmsb, lenlsb = self.getTermWidths(signal)
            if msb: 
                v_msb = str(self.optimizer.optimize(msb).value)
            if lsb: 
                v_lsb = str(self.optimizer.optimize(lsb).value)
                if v_msb is not v_lsb:
                    string+='[' + v_msb + ':' + v_lsb + '] '
            string+=signal.getSignalName()
            if lenmsb: 
                v_lmsb = str(self.optimizer.optimize(lenmsb).value)
            if lenlsb: 
                v_llsb = str(self.optimizer.optimize(lenlsb).value)
                if v_lmsb is not v_llsb:
                    string+=' [' + v_lmsb + ':' + v_llsb + '] '
            string+=',\n'
        string=string[:-2]
        f.write(string)
        f.write(');\n\n')
        #The file has been set with a module name and signal list
        self.writer.setFile(f)
        
        valuetable={}
                    
        for reg in self.moduleinfotable.getInteresting():
            regtable={}
            clkstr=""
            scope=self.chain + ScopeLabel(reg,'signal')
            for bind in self.binddict[scope]:
                if(bind.isClockEdge()):
                    clkstr=bind.getClockEdge()
                    clkstr=clkstr+"("+ bind.getClockName().getSignalName() + ")"
                else:
                    clkstr=bind.getClockName().getSignalName()

                for value, cond in self.getValues(bind, scope):
                    #print(value + ":" + cond)
                    if value in regtable.keys():
                        regtable[value].append(cond)
                    else:
                        regtable[value]=[cond]
                    
                    self.buf.write(str(value) + ' : ' + cond + '\n\n\n')

                if not self.exhaustive:
                    for value in regtable.keys():
                        if len(regtable[value])==1:
                            del regtable[value]
            valuetable[reg]=(clkstr, regtable)

        for always in self.moduleinfotable.getAlways().values():
            if listintersect(always.getControl(), valuetable.keys()):
                for data in always.getState():
                    datascope=self.chain+ScopeLabel(data,'signal')
                    for bind in self.binddict[datascope]:
                        self.writeProps(datascope, bind, valuetable)
        
        self.writer.writeAll()
        f.write('\nendmodule')
        f.write("\n\n\n\n")
        f.write("module " + filename + "_wrapper;\n")
        if len(self.chain)==1:
            #TOP module
            f.write("bind ")
            f.write(str(self.chain) + " " + filename + " " + filename + "_props(.*);\n")
        else:
            f.write("bind " + self.moduleinfotable.getCurrent() + " : ")
            f.write(str(self.chain) + " " + filename + " " + filename + "_props(.*);\n")
        f.write("\n\nendmodule")
        f.close()
        self.generic_visit(node)

    def getValues(self, bind, name):
        ret=[]
        #print(name)
        ret=self.parseTree(self.optimizer.optimize(bind.tree), name, ret)
        return ret 

    def parseTree(self, tree, name, oldlist = []):
        ret = oldlist
        if self.isDFBranch(tree):
            string=self.getstr(tree.condnode)
            if(tree.truenode): 
                self._addTrue(string)
                self.parseTree(tree.truenode, name, ret)
                self._popCond()
            if(tree.falsenode): 
                self._addFalse(string)
                self.parseTree(tree.falsenode, name, ret)
                self._popCond()

        if self.isDFterm(tree):
            if "Rename" in self.dataflow.getTerm(tree.name).termtype:
                #print("Reached rename" + str(tree.getTermName()))
                for bind in self.binddict[tree.name]:
                        ret.extend(self.getValues(bind, name))
            else:
                ret.append((str(tree.getTermName()), self._getCond()))
                #print("Reached " + str(tree.getTermName()))
                #always=self.moduleinfotable.getAlwaysfromState(tree.getTermName())
                #if always:
                    #if name.getSignalName() in always.getControl():
                for bind in self.binddict[tree.name]:
                    if bind.isCombination():
                        ret.extend(self.getValues(bind, name))

        if self.isDFeval(tree):
            ret.append((str(tree.value), self._getCond()))
        
        if self.isDFConst(tree):
            ret.append((str(tree.eval()), self._getCond()))
        
        if self.isDFOp(tree):
            ret.append((self.getstr(tree), self._getCond()))
        
        if self.isDFparts(tree):
            ret.append((self.getstr(tree), self._getCond()))
        
        if(isinstance(tree, DFPointer)):
            print("What is a pointer!!!")
            ret.append(("What is a pointer", self_getCond()))
        return ret
    
    def _addTrue(self, condition):
        self.cond.append(condition)

    def _addFalse(self, condition):
        self.cond.append(self._invert(condition))

    def _invert(self, condition):
        return '!' + '(' + condition + ')'

    def _popCond(self):
        del self.cond[-1]

    def _getCond(self):
        if self.cond:
            ret = '('
            for cond in self.cond:
                ret+='(' + cond + ')' + '&&'
            ret=ret[:-2]
            ret+=')'
            return ret
        else:
            return '(1)'

    def isDFterm(self, tree):
        return isinstance(tree, DFTerminal)

    def isDFConst(self, tree):
        return isinstance(tree, DFIntConst) or isinstance(tree,DFFloatConst) or isinstance(tree, DFStringConst)

    def isDFBranch(self, tree):
        return isinstance(tree, DFBranch)

    def isDFeval(self, tree):
        return isinstance(tree, DFEvalValue)

    def isDFOp(self, tree):
        if isinstance(tree, DFPointer):
            print("What is a pointer!")
            sys.exit()
        return isinstance(tree, DFOperator) 
    
    def isDFparts(self, tree):
        return isinstance(tree, DFPartselect) or isinstance(tree, DFConcat)


    def writeProps(self, data, bind, valuetable):
        self.writer.newSet(data)
        clkstr=""
        if(bind.isCombination()):
            #print("Combinational Bind: " + str(data))
            pass
        else:
            if(bind.isClockEdge()):
                clkstr=bind.getClockEdge()
                clkstr=clkstr+"("+bind.getClockName().getSignalName() + ")"
            else:
                clkstr=bind.getClockName().getSignalName()
        self.writer.setConseqClock(clkstr)
        self._parseandwrite(data, self.optimizer.optimize(bind.tree), valuetable)
    
    def _getConditionAntes(self, data, tree):
        if self.isDFterm(tree):
            if "Rename" in self.dataflow.getTerm(tree.name).termtype:
                for bind in self.binddict[tree.name]:
                    return(self.getstr(self.optimizer.optimize(bind.tree)), {})
            else:
                return (str(tree.getTermName()), {})

        if self.isDFeval(tree):
            return (str(tree.value), {})

        if self.isDFConst(tree):
            return (str(tree.eval()), {})
        
        if self.isDFOp(tree):
            valuelist=[]
            for node in tree.nextnodes:
                valuelist.append(self._getConditionAntes(data, node))
            
            newdict={}
            string=""
            if tree.operator == 'Eq' or tree.operator == 'Eql':
                string="(" + valuelist[0][0] + "==" + valuelist[1][0] + ")"
                #if valuelist[0][0]==state.getSignalName():
                newdict[valuelist[0][0]]=[valuelist[1][0]]

            if tree.operator == 'NotEq' or tree.operator == 'NotEql':
                string="(" + valuelist[0][0] + "!=" + valuelist[1][0] + ")"
            
            if tree.operator == 'Ulnot':
                if valuelist[0][0] == "0" or valuelist[0][0] == "False":
                    return ("1", found or valuelist[0][1])
                if valuelist[0][0] == "1" or valuelist[0][0] == "True":
                    return ("0", found or valuelist[0][1])
                string="(!(" + valuelist[0][0] + "))"

            if tree.operator == 'Unot':
                if valuelist[0][0] == "0" or valuelist[0][0] == "False":
                    return ("1", found or valuelist[0][1])
                if valuelist[0][0] == "1" or valuelist[0][0] == "True":
                    return ("0", found or valuelist[0][1])
                string="(~(" + valuelist[0][0] + "))"

            if tree.operator == 'LessThan':
                string="(" + valuelist[0][0] + "<" + valuelist[1][0] + ")"
            if tree.operator == 'GreaterThan':
                string="(" + valuelist[0][0] + ">" + valuelist[1][0] + ")"
            if tree.operator == 'LessEq':
                string="(" + valuelist[0][0] + "<=" + valuelist[1][0] + ")"
            if tree.operator == 'GreaterEq':
                string="(" + valuelist[0][0] + ">=" + valuelist[1][0] + ")"
            
            if tree.operator == 'Land':
                string="(" + valuelist[0][0] + "&&" + valuelist[1][0] + ")"
                newdict=dictintersect(valuelist[0][1], valuelist[1][1])

            if tree.operator == 'Lor':
                string="(" + valuelist[0][0] + "||" + valuelist[1][0] + ")"
                newdict=dictunion(valuelist[0][1], valuelist[1][1])
            
            if tree.operator == 'Uminus':
                string = "-1*" + valuelist[0][0]
            if tree.operator == 'Uand': 
                string="(& " + valuelist[0][0] + ")"
            if tree.operator == 'Unand': 
                string="(~(& " + valuelist[0][0] + "))"
            if tree.operator == 'Uor': 
                string="(| " + valuelist[0][0] + ")"
            if tree.operator == 'Unor': 
                string="(~(| " + valuelist[0][0] + "))"
            if tree.operator == 'Uxor':
                string="(^ " + valuelist[0][0] + ")"
            if tree.operator == 'Uxnor':
                string="(~(^ " + valuelist[0][0] + "))"
            if tree.operator == 'Power':
                string="(" + valuelist[0][0] + "**" +valuelist[1][0] + ")"
            if tree.operator == 'Times':
                string="(" + valuelist[0][0] + "*" +valuelist[1][0] + ")"
            if tree.operator == 'Divide':
                string="(" + valuelist[0][0] + "/" +valuelist[1][0] + ")"
            if tree.operator == 'Mod':
                string="(" + valuelist[0][0] + "%" +valuelist[1][0] + ")"
            if tree.operator == 'Plus':
                string="(" + valuelist[0][0] + "+" +valuelist[1][0] + ")"
            if tree.operator == 'Minus':
                string="(" + valuelist[0][0] + "-" +valuelist[1][0] + ")"
            if tree.operator == 'Sll':
                string="(" + valuelist[0][0] + "<<" +valuelist[1][0] + ")"
            if tree.operator == 'Srl':
                string="(" + valuelist[0][0] + ">>" +valuelist[1][0] + ")"
            if tree.operator == 'Sra':
                string="(" + valuelist[0][0] + ">>" +valuelist[1][0] + ")"
            if tree.operator == 'And':
                string="(" + valuelist[0][0] + "&" +valuelist[1][0] + ")"
            if tree.operator == 'Xor':
                string="(" + valuelist[0][0] + "^" +valuelist[1][0] + ")"
            if tree.operator == 'Xnor':
                string="(~(" + valuelist[0][0] + "^" +valuelist[1][0] + "))"
            if tree.operator == 'Or':
                string="(" + valuelist[0][0] + "|" +valuelist[1][0] + ")"
            return (string, newdict)
        
        if self.isDFparts(tree):
            return (self.getstr(tree), {})
            #if isinstance(tree, DFPartselect):
            #    msb=tree.msb.value
            #    lsb=tree.lsb.value
            #    string = self.getstr(tree.var)
            #    if msb==lsb:
            #        string+="["+str(msb)+"]"
            #    else:
            #        string+="["+str(msb)+":"+str(lsb)+"]"
            #    return (string, {})
            #
            #if isinstance(tree, DFConcat):
            #    string="{"
            #    newfound = False
            #    for nodes in tree.nextnodes:
            #        nodestr, nodefound = self._parseandwrite(data, state, node, valuetable, cond, found)
            #        string += nodestr + ','
            #        newfound = newfound or nodefound
            #    string=string[:-1]
            #    string+="}"
            #    return (string, newfound)
        
    
    def _parseandwrite(self, data, tree, valuetable): 
        if self.isDFBranch(tree):
            string, antetable = self._getConditionAntes(data, tree.condnode)
            if(tree.truenode):
                antelist=[]
                for statename,values in antetable.items():
                    if statename in valuetable.keys():
                        clkstr, table = valuetable[statename]
                        for value in values:
                            if value in table.keys():
                                antelist.extend([(cond, clkstr) for cond in table[value]])
                self.writer.addAnte(antelist)
                self._addTrue(string)
                self._parseandwrite(data, tree.truenode, valuetable)
                self._popCond()
                self.writer.clearLast()
            if(tree.falsenode): 
                self._addFalse(string)
                self._parseandwrite(data, tree.falsenode, valuetable)
                self._popCond()
        else:
            #val,newfound = self._parseandwrite(data, state, tree, valuetable, True, found)
            #self._addTrue(data.getSignalName() + "==" + val)
            #print(str(data) + ":" + val + " - " + self._getCond())
            self.writer.setConseq(self._getCond())
            self.writer.write()
            #self._popCond()

    def getstr(self, tree):
        if self.isDFterm(tree):
            return str(tree.getTermName())

        if self.isDFeval(tree):
            return str(tree.value)

        if self.isDFConst(tree):
            return str(tree.eval())
        
        if self.isDFeval(tree):
            return str(tree.value)
        
        if self.isDFOp(tree):
            valuelist=[]
            for node in tree.nextnodes:
                valuelist.append(self.getstr(node))
            
            if tree.operator == 'Eq' or tree.operator == 'Eql':
                string="(" + valuelist[0] + "==" + valuelist[1] + ")"
                return string
            if tree.operator == 'NotEq' or tree.operator == 'NotEql':
                string="(" + valuelist[0] + "!=" + valuelist[1] + ")"
                return string

            if tree.operator == 'LessThan':
                string="(" + valuelist[0] + "<" + valuelist[1] + ")"
                return string
            if tree.operator == 'GreaterThan':
                string="(" + valuelist[0] + ">" + valuelist[1] + ")"
                return string
            if tree.operator == 'LessEq':
                string="(" + valuelist[0] + "<=" + valuelist[1] + ")"
                return string
            if tree.operator == 'GreaterEq':
                string="(" + valuelist[0] + ">=" + valuelist[1] + ")"
                return string
            if tree.operator == 'Land':
                string="(" + valuelist[0] + "&&" + valuelist[1] + ")"
                return string
            if tree.operator == 'Lor':
                string="(" + valuelist[0] + "||" + valuelist[1] + ")"
                return string
            if tree.operator == 'Uminus':
                string = "-1*" + valuelist[0]
                return string
            if tree.operator == 'Ulnot':
                if valuelist[0] == "0" or valuelist[0] == "False":
                    return "1"
                if valuelist[0] == "1" or valuelist[0] == "True":
                    return "0"
                string="(!(" + valuelist[0] + "))"
                return string 
            if tree.operator == 'Unot':
                if valuelist[0] == "0" or valuelist[0] == "False":
                    return "1"
                if valuelist[0]== "1" or valuelist[0] == "True":
                    return "0"
                string="(~(" + valuelist[0] + "))"
                return string
            if tree.operator == 'Uand': 
                string="(& " + valuelist[0] + ")"
                return string  
            if tree.operator == 'Unand': 
                string="(~(& " + valuelist[0] + "))"
                return string  
            if tree.operator == 'Uor': 
                string="(| " + valuelist[0] + ")"
                return string  
            if tree.operator == 'Unor': 
                string="(~(| " + valuelist[0] + "))"
                return string  
            if tree.operator == 'Uxor':
                string="(^ " + valuelist[0] + ")"
                return string  
            if tree.operator == 'Uxnor':
                string="(~(^ " + valuelist[0] + "))"
                return string  
            if tree.operator == 'Power':
                string="(" + valuelist[0] + "**" +valuelist[1] + ")"
                return string  
            if tree.operator == 'Times':
                string="(" + valuelist[0] + "*" +valuelist[1] + ")"
                return string  
            if tree.operator == 'Divide':
                string="(" + valuelist[0] + "/" +valuelist[1] + ")"
                return string  
            if tree.operator == 'Mod':
                string="(" + valuelist[0] + "%" +valuelist[1] + ")"
                return string  
            if tree.operator == 'Plus':
                string="(" + valuelist[0] + "+" +valuelist[1] + ")"
                return string  
            if tree.operator == 'Minus':
                string="(" + valuelist[0] + "-" +valuelist[1] + ")"
                return string  
            if tree.operator == 'Sll':
                string="(" + valuelist[0] + "<<" +valuelist[1] + ")"
                return string  
            if tree.operator == 'Srl':
                string="(" + valuelist[0] + ">>" +valuelist[1] + ")"
                return string  
            if tree.operator == 'Sra':
                string="(" + valuelist[0] + ">>" +valuelist[1] + ")"
                return string  
            if tree.operator == 'And':
                string="(" + valuelist[0] + "&" +valuelist[1] + ")"
                return string  
            if tree.operator == 'Xor':
                string="(" + valuelist[0] + "^" +valuelist[1] + ")"
                return string  
            if tree.operator == 'Xnor':
                string="(~(" + valuelist[0] + "^" +valuelist[1] + "))"
                return string  
            if tree.operator == 'Or':
                string="(" + valuelist[0] + "|" +valuelist[1] + ")"
                return string  
            return None
        
        if self.isDFparts(tree):
            if isinstance(tree, DFPartselect):
                msb=tree.msb.value
                lsb=tree.lsb.value
                string = self.getstr(tree.var)
                if msb==lsb:
                    string+="["+str(msb)+"]"
                else:
                    string+="["+str(msb)+":"+str(lsb)+"]"
                return string
            
            if isinstance(tree, DFConcat):
                string="{"
                newfound = False
                for node in tree.nextnodes:
                    nodestr = self.getstr(node)
                    string += nodestr + ','
                string=string[:-1]
                string+="}"
                return string

    def visit_InstanceList(self, node):
        for i in node.instances:
            self.visit(i)
    
    def visit_Instance(self, node):
        if node.array: return self._visit_Instance_array(node)
        nodename = node.name
        return self._visit_Instance_body(node, nodename)

    def _visit_Instance_array(self, node):
        if node.name == '':
            raise verror.FormatError("Module %s requires an instance name" % node.module)

        lsb, msb = self.moduleinfotable.getlimiters(node)

        for i in range(lsb, msb+1):
            nodename = node.name + '_' + str(i)
            self._visit_Instance_body(node, nodename, arrayindex=i)

    def _visit_Instance_body(self, node, nodename, arrayindex=None):
        if node.module in primitives: return self._visit_Instance_primitive(node, arrayindex)

        if nodename == '':
            raise verror.FormatError("Module %s requires an instance name" % node.module)

        topmodule=self.moduleinfotable.getCurrent()
        self.chain+=ScopeLabel(nodename,'module')
        self.moduleinfotable.setCurrent(node.module)
        self.visit(self.moduleinfotable.getDefinition(node.module))
        self.moduleinfotable.setCurrent(topmodule)
        self.chain.pop()

    def _visit_Instance_primitive(self, node, arrayindex=None):
        pass
    
    def getTermWidths(self, name):
        term = self.dataflow.getTerm(name)
        return term.msb, term.lsb, term.lenmsb, term.lenlsb

