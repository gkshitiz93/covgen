from __future__ import absolute_import
from __future__ import print_function
import sys
import os
from optparse import OptionParser

import pyverilog.utils.version
from covgen import CoverageGenerator

def main():
    INFO = "Automatic cover property generator"
    USAGE = "Usage: python main.py -t TOPMODULE [*.v]"

    def showVersion():
        print(INFO)
        print(USAGE)
        sys.exit()
    
    optparser = OptionParser()
    optparser.add_option("-I","--include",dest="include",action="append",
                         default=[],help="Include path")
    optparser.add_option("-D",dest="define",action="append",
                         default=[],help="Macro Definition")
    optparser.add_option("-t","--top",dest="topmodule",
                         default="TOP",help="Top module, Default=TOP")
    (options, args) = optparser.parse_args()

    filelist = args

    for f in filelist:
        if not os.path.exists(f): raise IOError("file not found: " + f)

    if len(filelist) == 0:
        showVersion()

    generator = CoverageGenerator(filelist, options.topmodule,preprocess_include=options.include,preprocess_define=options.define)
    generator.generate()

    f=open("ast","w")
    generator.showAST(f)
    f.close()

    f=open("info","w")
    generator.showInfo(f)
    f.close()

if __name__ == '__main__':
    main()
