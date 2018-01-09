import argparse
import sys
from config import Config
from config import CreateStructureOnDisk
import os
p = argparse.ArgumentParser(description='Here is the complete list for endPoints.')
p.add_argument('-compName', default='', help='Please provide the component name by which parent folder should be created')
p.add_argument('-compDir', default='', help='Please provide absolute directory path')
p.add_argument('-firstEndPoint', default='', help='Please provide first endpoint name which you are going to automation')

args = p.parse_args()
if not args.compName:
    print "-compName(component name) is not provided\n"
    sys.exit()

if not args.compDir:
    print "-compDir(component dir) is not provided\n"
    sys.exit()
else:
    if not os.path.exists(args.compDir):
        os.mkdir(args.compDir)
    
if not args.firstEndPoint:
    print "-firstEndPoint(first end point name) is not provided\n"
    sys.exit()

struct = Config(args.compName, args.compDir, args.firstEndPoint).getStruct()
CreateStructureOnDisk(struct, args.compName, args.firstEndPoint).writeFiles()







