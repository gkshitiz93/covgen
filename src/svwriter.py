from __future__ import absolute_import
from __future__ import print_function
import sys
import os
import re

class SVWriter(object):
    def __init__(self):
        self.ante=[]
        self.ante_temp=[]#Conditions which are not finalized
        self.conseq=None
        self.conseqclock=None
        self.buf=sys.stdout
        self.delay=1
        self.counter=1
        self.data=None
        self.state=None

    def setFile(self, buf=sys.stdout):
        self.buf=buf

    def setAnteClock(self, clk, edge):
        self.anteclock=clk
        self.anteclockedge=edge

    def setConseqClock(self, clkstr):
        self.conseqclock=clkstr
    
    def clearAnte(self):
        del self.ante[:]
        del self.ante_temp[:]

    def addAnte(self, anteinfo):
        self.ante.extend(anteinfo)

    def setConseq(self, consequent):
        self.conseq = consequent

    def addAntetemp(self, anteinfo):
        self.ante_temp.extend(anteinfo)
    
    def clearAntetemp(self):
        del self.ante_temp[:]

    def newSet(self, data, state):
        self.data=str(data[-1])
        self.state=str(state[-1])

    def commitAntetemp(self):
        self.ante.extend(self.ante_temp)
        del self.ante_temp[:]

    def setDelay(self, delay):
        self.delay=delay

    def getName(self):
        string = self.state + "_" + self.data + "_" + str(self.counter)
        self.counter+=1
        return string

    def write(self):
        for ante in self.ante:
            self.buf.write(self.getName() + ': cover property(')
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
        self.clearAnte()

