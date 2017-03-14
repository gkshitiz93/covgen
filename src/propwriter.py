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

class PropWriter(NodeVisitor):
    def __init__(self, moduleinfotable, top, frames, dataflow, buf=sys.stdout):
        self.moduleinfotable=moduleinfotable
        self.top = top
        self.frames = frames
        self.dataflow = dataflow
        self.binddict = self.dataflow.getBinddict()
        self.optimizer = VerilogOptimizer({}, {})
        self.writer = SVWriter()
        self.moduleinfotable.setCurrent(top)
        self.chain = ScopeChain()
        self.chain += ScopeLabel(top, 'module')
        self.optimizer = VerilogOptimizer({}, {})
        self.buf=buf

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
        filename=str(self.chain)+'_test'
        f=open(filename,"w")
        filename=filename.replace(".","_")
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
        f.write(');')

        for const in self.frames.getConsts(self.chain).keys():
            self.buf.write(str(const) + ': ' + '\n')
            for bind in self.binddict[const]:
                for name, node, cond in bind.getValues():
                    self.buf.write(name + ' : ' + cond + '\n')
                    
        for reg in self.moduleinfotable.getInteresting():
            scope=self.chain + ScopeLabel(reg,'signal')
            self.buf.write(str(scope) + ': ' + '\n')
            for bind in self.binddict[scope]:
                for name, node, cond in bind.getValues():
                    self.buf.write(name + ' : ' + cond + '\n')
        f.write('\nendmodule')
        f.close()
        self.generic_visit(node)

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

