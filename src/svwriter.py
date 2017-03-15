from __future__ import absolute_import
from __future__ import print_function
import sys
import os
import re

class SVWriter(object):
    def __init__(self):
        self.ante=None
        self.conseq=None
        self.anteclock=None
        self.anteclockedge=None
        self.conseqclock=None
        self.conseqclockedge=None
        self.buf=sys.stdout
        self.delay=1

    def setFile(self, buf=sys.stdout):
        self.buf=buf

    def setAnteClock(self, clk, edge):
        self.anteclock=clk
        self.anteclockedge=edge

    def setConseqClock(self, clk, edge):
        self.conseqclock=clk
        self.conseqclockedge=edge
    
    def setAnte(self, antecedent):
        self.ante = antecedent

    def setConseq(self, consequent):
        self.conseq = consequent

    def setDelay(self, delay):
        self.delay=delay

    def write(self):
        self.buf.write('cover property: (')
        if self.anteclock:
            if self.anteclockedge:
                self.buf.write("(@" + self.anteclockedge + " " + self.anteclock + ") ")
        self.buf.write(self.ante)
        if(self.conseq):
            self.buf.write("->##" + str(self.delay) + " ")
            if self.conseqclock:
                if self.conseqclockedge:
                    self.buf.write("(@" + self.conseqclockedge + " " + self.anteclock + ") ")

            self.buf.write(self.conseq)
        self.buf.write(")\n\n")

