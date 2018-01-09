'''
Created on 20-Feb-2014
@author: Mayank Kodesia
'''
from framework.helper.XmlValidator import XMLSchemaValidator
from framework.helper.JsonValidator import JSONSchemaValidator
from framework.helper.Report import Report
import os
from framework.helper.Utility import Utility
from framework.helper.Globals import logs
import commands
import time



class ProcessValidation():
    '''
    This class will validate the report and its schema
    It will call the schema as per file Name passed i.e. if xsd it will call XML validator
    If its JSON it will call JSON Validator and same for stix
    '''
  
    def __init__(self):
        '''
        Constructor
        '''
        
    def validateSchema(self, report, schemaFileName ):
        if schemaFileName=="Invalid":
            logs.error("Invalid File Name")
            return
       
        if 'xsd' in schemaFileName and not 'stix' in schemaFileName:
            result, message = XMLSchemaValidator(report, schemaFileName).validate()
            if result:
                return True, message
            else:
                return False, message
       
        elif 'schema' in schemaFileName:
            result, message = JSONSchemaValidator(report, schemaFileName).validate()
            if result:
                return True, message
            else:
                return False, message
        
        elif 'stix' in schemaFileName:
            result, message = self.stixValidator(report)
            if result:
                return True, message
            else:
                return False, message
            
        elif 'csv' in schemaFileName:
            result = self.csvValidator(report)
            if result:
                return True, ""
            else:
                return False, "csv output does not have required headers"
        else:
            logs.error("Schema is not known type")
            return False
        
    def validate(self, response, schemaFileName ):
        result, message = self.validateSchema(response, schemaFileName)
        if result:
            return True, message
        else:
            return False, message
        
    def stixValidator(self, report):
        reportObj = Report()
        with open("/tmp/stix_temp.xml", 'w') as f:
            f.write(report)
    
        fileId = str(int(time.time()))
        #os.system("python ../external/stix-validator-master/sdv.py --input-file /tmp/stix_temp.xml > /tmp/stix_out")
        commands.getoutput("python ../external/stix-validator-master/sdv.py --input-file /tmp/stix_temp.xml > /tmp/stix_out"+fileId)
#         --input-dir ../external/stix-validator-master/schema 
        result=""
        with open("/tmp/stix_out"+fileId, 'r') as f:
            for ot in f:
                result+=ot
        #os.system("rm -f /tmp/stix_out")
        commands.getoutput("rm -f /tmp/stix_out"+fileId)
        if 'INVALID' in result:
            reportObj.setReportErrorMessage(result)
            return False, str(result)
        else:
            return True, ""
         
            
    def csvValidator(self, response):
        return Utility().isResponseCsv(response)
        
          
        
    
