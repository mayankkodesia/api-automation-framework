__author__ = 'LT-CSIN'
'''
Created on 20-Feb-2014
@author: Mayank Kodesia
'''
from framework.helper.Globals import logs


class ConfigFileReader():
    '''
    This class is used to read the property file
    property files are available under input/config folder
    '''

    def __init__(self):
        #self.getFileHandler()
        pass

    '''
    Below function returns the value when config fileName and key is given as an arguments
    '''
    def getValueByKey(self, fileName, key):
        self.getFileHandler(fileName)

        lines = self.file.readlines()
        for line in lines:
            if len(line) > 0 and not str(line).startswith("#") and str(key).strip() in line:
                line = line.rstrip('\n')
                key_values = str(line).split("=",1)
                left=key_values[0]
                right=key_values[1]
                if str(left).strip()==key:
                    key = str(right).strip()
                    return key

        self.file.close()

    def getValueByIdKey(self, fileName, key):
        '''
        This function returns the ID and key of the test
        A test is defined in conf file includes <id>.<url> format.
        '''
        self.getFileHandler(fileName)

        lines = self.file.readlines()
        for line in lines:
            if len(line) > 0 and not str(line).startswith("#"):
                line = line.rstrip('\n')
                key_values = str(line).split("=",1)
                left=key_values[0]
                right=key_values[1]
                if str(left).strip()==key:
                    key = str(right).strip()
                    if "." in key:
                        key_split = str(key).split(".")
                        ids = str(key_split[0])
                        key = str(key_split[1]).strip()
                    return ids, key

        self.file.close()



    def getFileHandler(self, fileName):
        import os
        script_dir = os.path.dirname(__file__)
        try:
            #self.file = open("../input/config/"+ fileName,"r")
            rel_path = "/../input/config/"+fileName
            self.file = open(script_dir+ rel_path,"r")
        except Exception:
            logs.error("File "+ fileName +" Not Found")


    def getAllLinesFromFile(self, fileName):
        '''
        Returns all lines from file, takes fileName as argument and return list of lines.
        '''
        self.getFileHandler(fileName)
        lines = self.file.readlines()
        return lines

    def getAllTestLinesFromFileWithID(self, fileName):
        '''This function removes all the comments, lines starting from
           format_supported, endpoint and other lines except tests
           For Advance search having matchedon in test line, it also returns the dictionary which contains {<testline>:<matched on>}
        '''
        self.getFileHandler(fileName)
        lines = self.file.readlines()
        basicSearch=True
        tests=[]
        testline_matchedon_dict = {}#{'dummy':'dummy'}
        for line in lines:
            line = str(line).rstrip('\n').rstrip('\t')
            if not str(line).startswith("format") and len(line)> 0 and not str(line).startswith("#") and not str(line).startswith("endpoint"):
                if not 'matchedon' in str(line).lower():
                    basicSearch=True
                    tests+=[line]
                else:
                    basicSearch=False ## Advance search
                    test_matchedon = str(line).split(";",1)
                    try:
                        key=str(test_matchedon[0]).rstrip('\n').rstrip('\t').strip()
                        value = str(test_matchedon[1]).rstrip('\n').rstrip('\t').strip()
                        testline_matchedon_dict[key]= value
                    except Exception as e:
                        logs.error("Error in forming dictionary ", e)
        if basicSearch:
            return tests
        else:
            return testline_matchedon_dict


    def getIDAndTestFromLine(self, test_line):
        '''
        Returns ID and Test from the line <ID>.<TestLine>
        '''
        test_line=str(test_line)
        if("." in test_line):
            id_test = str(test_line).split(".",1)
            ids = id_test[0]
            test = id_test[1]
            return str(ids).strip(), str(test).strip()
        else:
            return 0, test_line




