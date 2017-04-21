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
        #self.state=None
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

    def newSet(self, data):
        self.data=str(data[-1])
        #self.state=str(state[-1])

    def clearLast(self):
        del self.ante[-1] 

    def setDelay(self, delay):
        self.delay=delay

    def getName(self):
        #string = self.state + "_" + self.data + "_" + str(self.counter) + " : "
        #string = self.data + "_" + str(self.counter) + " : "
        string = "prop_" + str(self.counter) + " : " 
        self.counter+=1
        return string

    def write(self):
        ##Debug props using printAnte and printConseq
        printAnte=True
        printConseq=True

        for antelist in self.ante:
            for ante in antelist:
                string=""
                #if not self.unique:
                #    string+=self.getName() 
                string+= 'cover property('
                cond, clkstr = ante
                if printAnte:
                    string+="@(" + clkstr + ") "
                    string+=cond
                if(self.conseq):
                    if printAnte and printConseq:
                        string+="|->##" + str(self.delay) + " "
                    if printConseq:
                        if self.conseqclock:
                            if self.conseqclock == clkstr and printAnte:
                                pass
                            else:
                                string+="@(" + self.conseqclock + ") "
                        else:
                            if not printAnte:
                                string+="@(" + clkstr + ") "
                        string+=self.conseq
                    string+=");\n\n"
                    self.proplist.append(string)

    def writeAll(self):
        if self.unique:
            for prop in set(self.proplist):
                self.buf.write(self.getName() + prop)
        else:
            for prop in self.proplist:
                self.buf.write(self.getName() + prop)
        self.proplist=[]

    def anyProp(self):
        return bool(self.proplist)
