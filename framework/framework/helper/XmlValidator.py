from lxml import etree
import os
from framework.helper.Report import Report
from framework.helper.Globals import logs
class XMLSchemaValidator(object):
    '''
    Validates XMl as per schema and return the Result and Response
    '''
    def __init__(self, report_string, schema_file):
        self.__schema_file = schema_file
        #self.__createSchemaTree()
        self.__report=report_string
#         self.__reportobj = Report()

    def getSchemaPath(self):
        for dirname, dirnames, filenames in os.walk('.'):
    # print path to all subdirectories first.
            for subdirname in dirnames:
                if "schema" == subdirname:
                    return os.path.join(dirname, subdirname)

    
    def __createSchemaTree(self):
        ''' Find out the schema file in directory '''
        self.__schema_file = os.path.join(self.getSchemaPath(), self.__schema_file)
        #print(self.__schema_file)
        with open(self.__schema_file, 'r') as f:
            schema_root = etree.XML(f.read())

        schema = etree.XMLSchema(schema_root)
        self.__xml_parser = etree.XMLParser(schema=schema)
        #self.validate()

    def validate(self):
        self.__createSchemaTree()
        #extraInfo=""
        try:
            #with open(self.__report, 'r') as f:
            etree.fromstring(self.__report, self.__xml_parser)
            return True, ""
        except Exception as e:
            logs.error(str(e))
            logs.debug("Schema File used is \"{}\"".format(self.__schema_file))
            return False, str(e)
        
            
            

