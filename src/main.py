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
    optparser.add_option("-i","--ignore",dest="ignore",action="append",
                         default=[],help="Module definitions to be ignored")
    optparser.add_option("-t","--top",dest="topmodule",
                         default="TOP",help="Top module, Default=TOP")
    optparser.add_option("--ex","-e",action="store_true",dest="exhaustive",
                         default=False,help="Get exhaustive properties, Default - False")
    (options, args) = optparser.parse_args()

    filelist = args

    for f in filelist:
        if not os.path.exists(f): raise IOError("file not found: " + f)

    if len(filelist) == 0:
        showVersion()

    generator = CoverageGenerator(filelist, options.topmodule,preprocess_include=options.include,preprocess_define=options.define, exhaustive=options.exhaustive, getlocal=True, getglobal=True, ignore=options.ignore)
    g=open("props","w")
    generator.generate(g)

    f=open("ast","w")
    generator.showAST(f)
    f.close()

    #f=open("info","w")
    #generator.showInfo(f)
    #f.close()
    #
    #f=open("frame","w")
    #generator.printFrames(f)
    #f.close()
    
    f=open("modules","w")
    generator.showModuleInfo(f)
    f.close()
    g.close()

if __name__ == '__main__':
    main()
