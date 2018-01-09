#import jsonschema
import json, os
import validictory

from framework.helper.Globals import logs
from framework.helper.Report import Report


class JSONSchemaValidator(object):
    def __init__(self, report, schema_file):
#         self.__schema_file_name = os.path.join(os.getcwd(), "../../../schema20", schema_file)
        self.__schema_file_name = os.path.join(self.getSchemaPath(), schema_file)
        print "using schema file Name as {}".format(self.__schema_file_name)
        self.__schema_file = open(self.__schema_file_name)
        self.__json_schema_obj = json.load(self.__schema_file)
        self.__data_file = report
        
    def getSchemaPath(self):
        for dirname, dirnames, filenames in os.walk('.'):
    # print path to all subdirectories first.
            for subdirname in dirnames:
                if "schema" == subdirname:
                    return os.path.join(dirname, subdirname)
    
        # print path to all filenames.
#             for filename in filenames:
#                 print(os.path.join(dirname, filename))
    
        # Advanced usage:
        # editing the 'dirnames' list will stop os.walk() from recursing into there.
#             if '.git' in dirnames:
#             # don't go into any .git directories.
#                 dirnames.remove('.git')
        
    def validate(self):
        json_file=self.__data_file
        json_data_obj = json.loads(json_file)#open(json_file))
        try:
            validictory.validate(json_data_obj, self.__json_schema_obj)
            return True, ""
        except Exception as e:#jsonschema.exceptions.ValidationError as extraInfo:
#             logs.error(str(e))
            logs.debug("Schema File used is \"{}\"".format(self.__schema_file_name))
            return False, str(e)
        
