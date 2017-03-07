from __future__ import absolute_import
from __future__ import print_function
import sys
import os
from optparse import OptionParser

import pyverilog.utils.version
from pyverilog.dataflow.dataflow_analyzer import VerilogDataflowAnalyzer
from pyverilog.dataflow.visit import AlwaysInfo

class CoverageGenerator(VerilogDataflowAnalyzer):
    def __init__(self, filelist, topmodule='TOP', preprocess_include=None,preprocess_define=None):
        VerilogDataflowAnalyzer.__init__(self, filelist, topmodule,True,True,preprocess_include,preprocess_define)

    def showInfo(self,buf=sys.stdout):
        directives = self.get_directives()
        buf.write('Directive:\n')
        buf.write('\n')
        for dr in sorted(directives, key=lambda x:str(x)):
            buf.write(dr)
            buf.write('\n')
        
        instances = self.getInstances()
        buf.write('Instance:')
        buf.write('\n')
        for module, instname in sorted(instances, key=lambda x:str(x[1])):
            string="(" +str(module) + " , " + str(instname) + ")"
            buf.write(string)
            buf.write('\n')

        buf.write('Signal:')
        buf.write('\n')
        signals = self.getSignals()
        for sig in signals:
            string=str(sig)
            buf.write(string)
            buf.write('\n')

        buf.write('Const:')
        buf.write('\n')
        consts = self.getConsts()
        for con in consts:
            string=str(con)
            buf.write(string)
            buf.write('\n')

        return

    def printFrames(self,buf=sys.stdout):
        for dk,dv in self.frametable.dict.items():
            string='Scope = ' + str(dk) + '\n'
            buf.write(string)
            string='Frametype = ' + dv.getFrametype() + '\n'
            buf.write(string)
           
            buf.write('Signals:\n')
            for name,var in dv.getSignals().items():
                string='Name : ' + str(name) + ' Var: ' + str(var) + '\n'
                buf.write(string)
            
            buf.write('Consts:\n')
            for name,var in dv.getConsts().items():
                string='Name : ' + str(name) + ' Var: ' + str(var) + '\n'
                buf.write(string)

    def showModuleInfo(self,buf=sys.stdout):
        mtable = self.frametable.moduleinfotable
        for name in mtable.get_names():
            buf.write('Module: ' + name + '\n')
            for key,info in mtable.getAlways(name).items():
                info.printInfo(buf)
                buf.write('\n')
            buf.write('\n')
            for name,var in mtable.getConsts(name).items():
                string='Name : ' + str(name) + ' Var: ' + str(var) + '\n'
                buf.write(string)

            buf.write('\n')
    
    def showAST(self,buf=sys.stdout):
        ast=self.parse()
        ast.show(buf)
        return
