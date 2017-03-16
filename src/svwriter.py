from __future__ import absolute_import
from __future__ import print_function
import sys
import os
import re

class SVWriter(object):
    def __init__(self):
        self.ante=[]
        self.conseq=None
        self.conseqclock=None
        self.buf=sys.stdout
        self.delay=1

    def setFile(self, buf=sys.stdout):
        self.buf=buf

    def setAnteClock(self, clk, edge):
        self.anteclock=clk
        self.anteclockedge=edge

    def setConseqClock(self, clkstr):
        self.conseqclock=clkstr
    
    def clearAnte(self):
        del self.ante[:]

    def addAnte(self, anteinfo):
        self.ante.extend(anteinfo)

    def setConseq(self, consequent):
        self.conseq = consequent

    def setDelay(self, delay):
        self.delay=delay

    def write(self):
        for ante in self.ante:
            self.buf.write('cover property(')
            cond, clkstr = ante
            self.buf.write("@(" + clkstr + ") ")
            self.buf.write(cond)
            if(self.conseq):
                self.buf.write("|->##" + str(self.delay) + " ")
                if self.conseqclock:
                    if self.conseqclock == clkstr:
                        pass
                    else:
                        self.buf.write("@(" + self.conseqclock + ") ")
                self.buf.write(self.conseq)
            self.buf.write(");\n\n")

