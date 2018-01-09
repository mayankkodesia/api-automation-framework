'''
Created on 11-Jul-2017
@author: Mayank Kodesia
'''
import os
class Config():
    def __init__(self, compName, compDir, firstEndPoint):
        self.compName = compName
        self.compDir = compDir
        self.firstEndPointName = firstEndPoint

        
    def getStruct(self):    
        isightCompDir = os.path.join(self.compDir, self.compName)
        print isightCompDir
        isightProduct = os.path.join(isightCompDir, "iSightProduct_"+self.compName)
        print "isightproduct", isightProduct
        struct = {
            "dirs":[  isightCompDir,
                      isightProduct,
                      os.path.join(self.compDir, self.compName),
                      os.path.join(isightProduct, "EP_suites"),
                      os.path.join(isightProduct, "EP_suites", "test_cases"),
                      os.path.join(isightProduct, "EP_suites", "test_cases", "test_data"),
                      os.path.join(isightProduct, "helper")
                          ], 
                  
           "files":[   (os.path.join(isightProduct, "__init__.py"), "__init__.py"),
                       (os.path.join(isightCompDir,'Main.py'), 'Main.txt'),
                       (os.path.join(isightCompDir,'__init__.py'), '__init__.py'),
                       
                       (os.path.join(isightProduct, "iSightProduct_"+self.compName+ "_config.py"),"config.txt"),
                       (os.path.join(isightProduct, "iSightProduct_"+self.compName+ "_test_suite.py"), "test_suite.txt"),
                       
                       (os.path.join(isightProduct, "EP_suites", "__init__.py"), "__init__.py"),
                       (os.path.join(isightProduct, "EP_suites", "TS_"+self.firstEndPointName+".py"),"TSSample.txt"),
                       (os.path.join(isightProduct, "EP_suites", "__init__.py"),"__init__.py"),
                       (os.path.join(isightProduct, "EP_suites", "test_cases", "__init__.py"), "__init__.py"),
                       (os.path.join(isightProduct, "EP_suites", "test_cases", "TC_"+self.firstEndPointName+".py"),"TCSample.txt"),
                       (os.path.join(isightProduct, "EP_suites", "test_cases", "TC_Base.py"),"TC_Base.txt"),
                       (os.path.join(isightProduct, "EP_suites", "test_cases", "test_data", "TC_"+self.firstEndPointName+".json"),"TCSample.json"),
                       (os.path.join(isightProduct, "helper", "__init__.py"),"__init__.py"),
                       (os.path.join(isightProduct, "helper", "Converters.py"),"Converters.txt"),
                       (os.path.join(isightProduct, "helper", "utils.py"), "utils.txt")
                    ]
                  }
        return struct
    
class CreateStructureOnDisk():
    def __init__(self, struct, compName, endPointName):
        self.__struct = struct
        self.__compName = compName
        self.__endPoint = endPointName
        
    def getCompName(self):
        return self.__compName
        
    def writeFiles(self):
        for di in self.__struct.get("dirs"):
            try:
                os.mkdir(di)
            except:
                pass
            
        for fi in self.__struct.get("files"):
            with open(os.path.join(os.getcwd(), "dummyFiles",fi[1]), "r") as fread:
                for line in fread:
                    with open(fi[0], "a") as fwrite:
                        fwrite.write(line.replace("<compName>", self.getCompName()).replace("Sample", self.__endPoint).replace("sample", self.__endPoint))
                else:
                    with open(fi[0], "a") as fwrite:
                        fwrite.write("")
                        
    
    
    