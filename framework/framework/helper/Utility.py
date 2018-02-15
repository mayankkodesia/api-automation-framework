'''
Created on 24-Mar-2014
@author: Mayank Kodesia
'''
import calendar
import json
import re
import time

from framework.helper.Globals import logs
import framework.helper.Globals as Globals
from framework.helper.TestLinkHandler import TestLinkHandler
from framework.helper.URLFormer import URLFormer
from Crypto.Cipher import XOR
import base64
#another checkin

class Utility(object):
    '''
    This class has miscellaneous functions those can be used around the workspace.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.daysBackAllowed=90
        self.notFound = []
        self.__URLFormer = URLFormer()
        self.__csvHeader = "reportId,title,ThreatScape,productType,publishDate,reportLink,webLink,emailIdentifier,senderAddress,senderName,sourceDomain,sourceIp,subject,recipient,language,fileName,fileSize,fuzzyHash,fileIdentifier,md5,sha1,sha256,description,fileType,packer,userAgent,registry,networkName,asn,cidr,domain,domainTimeOfLookup,networkIdentifier,ip,port,url,protocol,registrantName,registrantEmail"



    def getEpochTime(self, daysBack, second=False, minute=False, hour=False, future=False):
        '''
        Return epoch time by current time - days passed
        if 10 is passed it will return epoch time of 10 days back from current time
        This def is enhanced for giving future date, if future=True is passed it returns future time than current time

        '''
        if future:
            if second:
                currentTime = int(time.time())
                return int(currentTime + daysBack)
            elif minute:
                currentTime = int(time.time())
                return int(currentTime + daysBack*60)
            elif hour:
                currentTime = int(time.time())
                return int(currentTime + daysBack*3600)
            else:
                currentTime = int(time.time())
                return int(currentTime + daysBack*24*3600)

        else:
            if second:
                currentTime = int(time.time())
                return int(currentTime - daysBack)
            elif minute:
                currentTime = int(time.time())
                return int(currentTime - daysBack*60)
            elif hour:
                currentTime = int(time.time())
                return int(currentTime - daysBack*3600)
            else:
                currentTime = int(time.time())
                return int(currentTime - daysBack*24*3600)


    def convertToEpoch(self,date_time=None, pattern="%B %d, %Y %H:%M:%S %p"):
        """
        Pattern default : "%Y-%m-%d %H:%M:%S"
        """
        if date_time is None:
            return int(time.time())
        else:
            if isinstance(date_time, str) or isinstance(date_time, unicode):
                epoch = int(calendar.timegm(time.strptime(date_time, pattern)))
            else:
                logs.error("Date time is not passed properly in pattern: {}".format(pattern))

        return epoch

    def validateValues(self, diction):
        '''
        dictionary format allowed is {'userDefinedKeys': ['expectedValue', 'actualValue', 'operator']}
        allowed operators are 
        =,!=, > , >=, <, <=, in
        '''
        operatorList = ['=','!=', '>' , '>=', '<', '<=', 'in', "notIn"]
        
        if not isinstance(diction,dict):
            return False, "This function, validateValues(), expects dictionary as an argument"
        
        else:
            keysNotMatched = []
            operatorNotMatched = []
            diction = dict(diction)
            for key in diction.keys():
                expectedActualOperator = diction.get(key)
                if not isinstance(expectedActualOperator,list):
                    return False, "Expected value, actual value and operator should be in a list like [<expectedValue>, <actualValue>, <operator>]"

                elif len(expectedActualOperator) == 2:
                    if expectedActualOperator[0] != expectedActualOperator[1]:
                        keysNotMatched.append(key)
                        operatorNotMatched.append("=")
                
                elif len(expectedActualOperator) == 3:
                    expected = expectedActualOperator[0]
                    actual = expectedActualOperator[1]
                    operator = str(expectedActualOperator[2]).strip()                    
                    
                    if operator == "=":
                        if not expected==actual:
                            keysNotMatched.append(key)
                            operatorNotMatched.append(operator)
                    
                    elif operator == "!=":
                        if expected==actual:
                            keysNotMatched.append(key)
                            operatorNotMatched.append(operator)
                    
                    elif operator == ">":
                        if not expected > actual:
                            keysNotMatched.append(key)
                            operatorNotMatched.append(operator)
                    
                    elif operator == ">=":
                        if not expected >= actual:
                            keysNotMatched.append(key)
                            operatorNotMatched.append(operator)
                    
                    elif operator == "<":
                        if not expected < actual:
                            keysNotMatched.append(key)
                            operatorNotMatched.append(operator)
                    
                    elif operator == "<=":
                        if not expected <= actual:
                            keysNotMatched.append(key)
                            operatorNotMatched.append(operator)
                            
                    elif operator == "in":
                        if not (expected in actual):
                            keysNotMatched.append(key)
                            operatorNotMatched.append(operator)
                    
                    elif operator == "notIn":
                        if (expected in actual):
                            keysNotMatched.append(key)
                            operatorNotMatched.append(operator)

                    elif not operator in operatorList:
                        return False, "invalid operator for key '{}' is passed, allowed operators are: {}".format(key, operatorList)

                else:
                    return False, "invalid list is passed for key: '{}', length of list can be only 2(without operator) or 3(with operator)".format(key)
            response = {}
            
            if keysNotMatched: #that means few values did not match the criteria 
                for k,op in zip(keysNotMatched,operatorNotMatched):
                    response[k] = 'Expected : {}, but found : {}, validated for operator {}'.format(diction.get(k)[0], diction.get(k)[1], op)                           
                return False, json.dumps(response)
            else :
                return True, ""

    def getElementsSortedListByFieldName(self, response, field, URL='', sort=True, intValues=True, limit=None, lowerCase=False, removeEmptyValue=True, text='id=":', closetext='" version'):
        '''
        returns sorted list of elements from response
        Check if response is xml, json or csv.
        cut the response till the field is found, then take the other part and take out its value,
        again repeat this process and so on, keep storing all values in list and return as per parameter passed.
        '''
        if URL:
            self.__URL = URL
        else:
            self.__URL = response

        response = str(response).replace("'", "\"")
        csvFile = False
        if 'stix' in URL:
            pass

        elif self.is_xml(response) or '<?xml version=\"1.0\"' in response:
            text = "<"+field+">"
            closetext = "</"+ field +">"
        elif self.is_json(self.__URL) or 'json' in self.__URL :
            text = "\""+ field + "\":"
            closetext = ","

        elif 'csv' in self.__URL or self.isResponseCsv(response):
            csvFile=True
            with (open("/tmp/temp.csv", 'w')) as f:
                f.write(response)
        else:
            logs.debug("Making default as json")
            text = "\""+ field + "\":"
            closetext = ","

        findList = []
        if csvFile:
            i=1;index=0
            with(open("/tmp/temp.csv", 'r')) as f:
                for line in f:
                    line = self.removeExtraCommaFromCSV(line)
                    line = self.cleanResponse(line)
                    if i==1:
                        #get the index for required field in list split by ","
                        array = line.split(",")
                        try:
                            index = list(array).index(field)
                            i+=1
                        except Exception as e:
                            logs.error("Required field {} not found in line: {}, returning empty array".format(field, line))
                            logs.error(str(e))
                            return []
                    else:
                        #then for that index take out the value in next coming rows
                        try:
                            value = line.split(",")[index]
                            if intValues:
                                findList.append(int(value))
                            elif lowerCase:
                                findList.append(str(value).lower().strip())
                            else:
                                findList.append(value.strip())
                        except:
                            pass
                f.close()

        else:
            string=response
            maximum = string.count(text)

            if limit < maximum and not limit==None :
                maximum=limit

            for temp in range(0, maximum):
                try:
                    tup = str(string).partition(text)
                    string = tup[2]
                    tup2 = string.partition(closetext)
                    if intValues:
                        findList.append(int(str(tup2[0]).strip().replace("\"", "")))

                    elif lowerCase:
                        findList.append(str(tup2[0]).replace("{", '').replace('[', '').replace(']', '').replace('}', '').replace("\"", '').strip().lower())

                    else:
                        findList.append(str(tup2[0]).replace("{", '').replace('[', '').replace(']', '').replace('}', '').replace("\"", '').strip())
                except:
                    pass
        if removeEmptyValue:
            new = []
            # To remove empty values in a list
            for li in findList:
                if li:
                    new.append(li)
            findList = new

        if sort:
            findList = sorted(findList)

        return findList

    def removeExtraCommaFromCSV(self, line):
        #there are some time comma in double quoted csv line, when we split by "," it creates a problem
        #This function removes that "," which comes after "\""
        flag=False
        sub=""
        newstring=""
        for c in line:
            if "\"" in c:
                if flag:
                    flag=False
                else:
                    flag=True

            if flag and not "," in c:
                sub+=c

            else:
                if sub:
                    newstring+=sub
                    sub=""
                else:
                    newstring+=c
        return newstring


    def is_json(self, myjson):
        import json
        try:
            json.loads(myjson)
            return True
        except ValueError:
            return False


    def is_xml(self, string):
        from xml.etree import ElementTree as ET
        try:
            ET.fromstring(string)
            return True
        except Exception:
            return False
        
    def generateUniqueName(self, prefix="", suffix=""):
        """generate_unique_name complex"""
        curTime = str(int(time.time()))
        uniqueName = prefix + curTime + suffix
        return uniqueName

    def markTestCasePassed(self, reportObj, valType, testCaseObj):
        self.__report = reportObj
#         testCaseObj['status'] = 'PASS'
        dataDiction =  testCaseObj.get(testCaseObj.keys()[0])
#         dataDiction.update({'status':{'value':'PASS', 'visible': True}})  
        dataDiction['status']['value'] = 'PASS'
        testCaseObj[testCaseObj.keys()[0]] = dataDiction
        
        self.__report.updatePassedTestCount(valType)
        self.__report.updateResult(valType, testCaseObj, 'Passed')
        if dataDiction.get('testLinkId').get('value') and Globals.TESTLINK:
            # print "Updating test link"
            self.updateTestLink(dataDiction)


        logs.debug("Total test Cases executed till now: "+ str(self.__report.getTestStats()[0]))
        logs.debug("Total test Cases Passed till now: "+ str(self.__report.getTestStats()[1]))
        logs.debug("Total test Cases Failed till now: "+ str(self.__report.getTestStats()[2]))



    def markTestCaseFailed(self, reportObj, valType,  testCaseObj):
        self.__report=reportObj
#         print testCaseObj
#         testCaseObj['status'] = 'FAIL'
        dataDiction =  testCaseObj.get(testCaseObj.keys()[0])
#         dataDiction.update({'status':{'value':'FAIL', 'visible': True, 'order': 0}}) 
        dataDiction['status']['value'] = 'FAIL'
        testCaseObj[testCaseObj.keys()[0]] = dataDiction

        self.__report.updateFailedTestCount(valType)
        self.__report.updateResult(valType, testCaseObj, 'Failed')
        if dataDiction.get('testLinkId').get('value') and Globals.TESTLINK:
#             self.updateTestLink(testCaseObj['testLinkId'], "FAIL", reason=testCaseObj['description']['failReason'])
            self.updateTestLink(dataDiction)

        logs.debug("Total test Cases executed till now: "+ str(self.__report.getTestStats()[0]))
        logs.debug("Total test Cases Passed till now: "+ str(self.__report.getTestStats()[1]))
        logs.debug("Total test Cases Failed till now: "+ str(self.__report.getTestStats()[2]))


    def updateTestLink(self, testCaseObj):
        self.testLinkHandler = TestLinkHandler(testCaseObj.get('testPlanId').get('value'), testCaseObj.get('projectId').get('value'), testCaseObj.get('userKey').get('value'))
#         print "inside updattestLink with testCaseObj: {}".format(testCaseObj)
        self.testLinkHandler.addTestCaseToTestPlan(testCaseObj.get('testLinkId').get('value'))
        self.testLinkHandler.createBuild()
        self.testLinkHandler.TestLinkUpdate(testCaseObj.get('testLinkId').get('value'), testCaseObj.get('status').get('value'), reason=testCaseObj.get('description').get('value').get('failReason'))



    def isResponseCsv(self, response):
        string = self.cleanResponse(self.__csvHeader)
        response = self.cleanResponse(response[0:1000])
        #         print(response)
        if response.startswith(string):
            return True
        return False


    def compareJsonResponses(self, fromURL, fromTest):
        fromURL = self.cleanResponse(fromURL).split(",")
        fromTest  = self.cleanResponse(fromTest).split(",")
        finalResult = []
        self.notFound = []
        for test in fromTest:
            if not test in fromURL and not "$" in test:
                finalResult.append(False)
                self.notFound.append(test)
            #                 return False

        if False in finalResult and self.notFound:
            logs.error("These values {} from reference string does not match with actual response".format(", ".join(self.notFound)))
            return False, "These elements mismatched %s "% ",".join(self.notFound)
        
        return True, ""


    def cleanResponse(self, response):
        ''' removes extra spaces and new line characters from response so that
        matchedOn can be easily matched'''
        new = ''
        response = str(response).replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "")
        for s in response:
            if not s==" " or s=="\n":
                new+=s
        new = new.replace(" ", "").replace("\t", "")
        return new

    def encryptToken(self, key, plaintext):
        cipher = XOR.new(key)
        return base64.b64encode(cipher.encrypt(plaintext))

    def decryptToken(self, key, ciphertext):
        cipher = XOR.new(key)
        return cipher.decrypt(base64.b64decode(ciphertext))
