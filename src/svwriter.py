from __future__ import absolute_import
from __future__ import print_function
import sys
import os
import re

class SVWriter(object):
    def __init__(self, unique=False):
        self.ante=[]
        self.conseq=None
        self.conseqclock=None
        self.buf=sys.stdout
        self.delay=1
        self.counter=1
        self.data=None
        self.state=None
        self.proplist=[]
        self.unique=unique

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
        self.ante.append(anteinfo)

    def setConseq(self, consequent):
        self.conseq = consequent

    def newSet(self, data, state):
        self.data=str(data[-1])
        self.state=str(state[-1])

    def clearLast(self):
        del self.ante[-1] 

    def setDelay(self, delay):
        self.delay=delay

    def getName(self):
        string = self.state + "_" + self.data + "_" + str(self.counter) + " : "
        self.counter+=1
        return string

    def write(self):
        for antelist in self.ante:
            for ante in antelist:
                string=""
                if not self.unique:
                    string+=self.getName() 
                string+= 'cover property('
                cond, clkstr = ante
                string+="@(" + clkstr + ") "
                string+=cond
                if(self.conseq):
                    string+="|->##" + str(self.delay) + " "
                    if self.conseqclock:
                        if self.conseqclock == clkstr:
                            pass
                        else:
                            string+="@(" + self.conseqclock + ") "
                    string+=self.conseq
                    string+=");\n\n"
                    self.proplist.append(string)

    def writeAll(self):
        if self.unique:
            for prop in set(self.proplist):
                self.buf.write(prop)
        else:
            for prop in self.proplist:
                self.buf.write(prop)
        self.proplist=[]
