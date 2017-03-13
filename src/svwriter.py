from __future__ import absolute_import
from __future__ import print_function
import sys
import os
import re

class SVWriter(object):
    def __init__(self):
        self.ante=[]
        self.conseq=[]
        self.clock=None
        self.clockedge=None
        self.buf=sys.stdout
        self.delay=1

    def setFile(buf=sys.stdout):
        self.buf=buf

    def newProp(self, antecedent=[], consequent=[], clk='', edge='', delay=1):
        del self.ante[:]
        del self.conseq[:]
        self.ante.extend(antecedent)
        self.conseq.extend(consequent)
        if clk is not '':
            self.clock=clk
        if edge is not '':
            self.clockedge=edge
        self.delay=delay
    
    def setClock(self, clk, edge):
        self.clock=clk
        self.clockedge=edge

    def addAnte(self, antecedent):
        self.ante.extend(antecedent)

    def addConseq(self, consequent):
        self.conseq.extend(consequent)

    def setDelay(self, delay):
        self.delay=delay

    def write(self):
        self.buf.write('cover property:')
        ##TODO##
        self.buf.write('\n')

