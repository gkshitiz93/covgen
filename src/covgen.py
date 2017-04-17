from __future__ import absolute_import
from __future__ import print_function
import sys
import os
from optparse import OptionParser
from pyverilog.vparser.parser import VerilogCodeParser
from pyverilog.dataflow.modulevisitor import ModuleVisitor
from pyverilog.dataflow.signalvisitor import SignalVisitor
from pyverilog.dataflow.bindvisitor import BindVisitor
import pyverilog.utils.version
from pyverilog.dataflow.dataflow_analyzer import VerilogDataflowAnalyzer
from pyverilog.dataflow.visit import AlwaysInfo
from propwriter import *
sys.setrecursionlimit(16 * 1024)

class CoverageGenerator(VerilogDataflowAnalyzer):
    def __init__(self, filelist, topmodule='TOP', preprocess_include=None,preprocess_define=None,exhaustive=False, getlocal=True, getglobal=True, ignore=[], unique=False, debug=False):
        VerilogDataflowAnalyzer.__init__(self, filelist, topmodule,True,True,preprocess_include,preprocess_define)
        self.moduleinfotable=None
        self.exhaustive=exhaustive
        self.getlocal=getlocal
        self.getglobal=getglobal
        self.modulelist=[]
        self.ignore=[]
        self.unique=unique
        self.debug=debug

    def generate(self, buf=sys.stdout):
        ast = self.parse()

        module_visitor = ModuleVisitor()
        module_visitor.visit(ast)
        self.moduleinfotable = module_visitor.get_moduleinfotable()
        #for name in self.moduleinfotable.get_names():
        #    print(name)
        self.moduleinfotable.findInteresting()
        
        signal_visitor = SignalVisitor(self.moduleinfotable, self.topmodule, self.debug)
        signal_visitor.start_visit()
        
        frametable = signal_visitor.getFrameTable()
        blackboxed = signal_visitor.getBlackboxed()
        
        bind_visitor = BindVisitor(self.moduleinfotable, self.topmodule, frametable, blackboxed, False, self.debug)
        bind_visitor.start_visit()
        dataflow = bind_visitor.getDataflows()
        self.frametable = bind_visitor.getFrameTable()
        #self.binddict = dataflow.getBinddict()
        #print("\n\nBinding done:\n\n")
        prop_writer = PropWriter(self.moduleinfotable, self.topmodule, self.frametable, dataflow, blackboxed, self.exhaustive, self.getlocal, self.getglobal, buf, self.unique, self.debug)
        prop_writer.start_visit()

    def showModuleInfo(self,buf=sys.stdout):
        mtable = self.moduleinfotable
        for modulename in mtable.get_names():
            buf.write('Module: ' + modulename + '\n')
            module=mtable.getModule(modulename)
            module.printInfo(buf)
           # if mtable.getConsts(modulename):
           #     buf.write('\nConstants:\n')
           #     for name,var in mtable.getConsts(modulename).items():
           #         string='Name : ' + str(name) + ' Var: ' + str(var) + '\n'
           #         buf.write(string)

           # if mtable.getSignals(modulename):
           #     buf.write('\nSignals:\n')
           #     for name,var in mtable.getSignals(modulename).items():
           #         string='Name : ' + str(name) + ' Var: ' + str(var) + '\n'
           #         buf.write(string)
           # 
           # if mtable.getIOPorts(modulename):
           #     buf.write('\nIOPorts:\n')
           #     for port in mtable.getIOPorts(modulename):
           #         string='Name : ' + str(port) + '\n'
           #         buf.write(string)
           # buf.write('\n')
   
    def showAST(self,buf=sys.stdout):
        ast=self.parse()
        ast.show(buf)
        return
    
    #def parseModule(self, modulename):
    #    signal_visitor = SignalVisitor(self.moduleinfotable, modulename)
    #    signal_visitor.start_visit()
    #    frametable = signal_visitor.getFrameTable()
    #    
    #    self.modulelist.append(modulename)

    #    for instance in self.moduleinfotable.getInstances(modulename):
    #        self.visitInstance(instance)

    #    for ilist in self.moduleinfotable.getInstanceLists(modulename):
    #        for node in ilist.instances:
    #            self.visitInstance(node)

    #def visitInstance(self, node):
    #    if node.module in self.modulelist:
    #        return
    #    parseModule(node.module)
            

   # def showInfo(self,buf=sys.stdout):
   #     directives = self.get_directives()
   #     buf.write('Directive:\n')
   #     buf.write('\n')
   #     for dr in sorted(directives, key=lambda x:str(x)):
   #         buf.write(dr)
   #         buf.write('\n')
   #     
   #     instances = self.getInstances()
   #     buf.write('Instance:')
   #     buf.write('\n')
   #     for module, instname in sorted(instances, key=lambda x:str(x[1])):
   #         string="(" +str(module) + " , " + str(instname) + ")"
   #         buf.write(string)
   #         buf.write('\n')

   #     buf.write('Signal:')
   #     buf.write('\n')
   #     signals = self.getSignals()
   #     for sig in signals:
   #         string=str(sig)
   #         buf.write(string)
   #         buf.write('\n')

   #     buf.write('Const:')
   #     buf.write('\n')
   #     consts = self.getConsts()
   #     for con in consts:
   #         string=str(con)
   #         buf.write(string)
   #         buf.write('\n')

   #     return

   # def printFrames(self,buf=sys.stdout):
   #     for dk,dv in self.frametable.dict.items():
   #         string='Scope = ' + str(dk) + '\n'
   #         buf.write(string)
   #         string='Frametype = ' + dv.getFrametype() + '\n'
   #         buf.write(string)
   #        
   #         buf.write('Signals:\n')
   #         for name,var in dv.getSignals().items():
   #             string='Name : ' + str(name) + ' Var: ' + str(var) + '\n'
   #             buf.write(string)
   #         
   #         buf.write('Consts:\n')
   #         for name,var in dv.getConsts().items():
   #             string='Name : ' + str(name) + ' Var: ' + str(var) + '\n'
   #             buf.write(string)

