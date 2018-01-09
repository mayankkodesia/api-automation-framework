from framework.helper import writeSummary
import time
__author__ = 'LT-CSIN'

import datetime, os

import framework.helper.Globals as Globals
from framework.helper.HTMLWriter import HTMLWriter


class Report(object):
    '''
    This class provide methods to write the result in a Report in report folder and also to dump the results
    in a file under logs folder.
    '''
    __totalTestCases=0
    __passedTestCases=0
    __failedTestCases=0
 
    __SVTotalTestCases=0
    __SVPassedTestCases=0
    __SVFailedTestCases=0
 
    __DVTotalTestCases=0
    __DVPassedTestCases=0
    __DVFailedTestCases=0
 
    __FVTotalTestCases=0
    __FVPassedTestCases=0
    __FVFailedTestCases=0
 
    __EVTotalTestCases=0
    __EVPassedTestCases=0
    __EVFailedTestCases=0
 
    __BCTotalTestCases=0
    __BCPassedTestCases=0
    __BCFailedTestCases=0

    __reportName=''
    __reportHandler=''
    __suiteName=''
    __resultTable = {}  # would be a list of list elements
    __reportErrorMessage =[]
    __reportDirName =''

    schemaErrorMessage = ''

    def __init__(self, dirName, stringAppendToReport=""):
        self.__reportDirName = dirName
        self.createFileName()
        if stringAppendToReport:
            self.addToReportName(stringAppendToReport)
        self.__resultTable = {'SchemaValidation':{'Passed':{}, 'Failed':{}}, 'DataValidation':{'Passed':{},'Failed':{}}, 'FlagValidation':{'Passed':{},'Failed':{}}, 'ErrorValidation':{'Passed':{}, 'Failed':{}}}


    def setReportErrorMessage(self, string):
        self.__reportErrorMessage.append(string)
    
    def addToReportName(self, string):
        reportName = self.__reportName
        lists = reportName.split("Report_")
        lists[0] = "Report_" + string
        self.__reportName = "_".join(lists).replace("__", "_")
    
    def createFileName(self):
        '''
        Return the file Name of the report, create the report if not exist
        '''
        dates = datetime.datetime.now().strftime("%I_%M%p %d %B %Y")
        self.__reportName = 'Report_'+ self.__reportDirName+'_'+(str(dates).replace(' ', "_")) + "_"+str(Globals.reportName)+".html"
        self.__currentDate=(str(dates).replace(' ', "_"))

    def getReportHandler(self):
        '''
        Return the file pointer for the current report
        '''

        script_dir = os.path.dirname(__file__)
        reportPath =script_dir +  "/../report/"+self.__reportDirName+'/'+self.__reportName
        dir = os.path.dirname(reportPath)
        if not os.path.exists(dir):
            os.makedirs(dir)
        self.__reportHandler = open(reportPath, 'a+')

    def getFailedReportHandler(self):
        '''
        Return the file pointer for the failed test cases report
        '''
        script_dir = os.path.dirname(__file__)
        reportPath = script_dir + "/../report/failed/"+self.__reportDirName + '/' + "Failed_"+ self.__reportName
        dir = os.path.dirname(reportPath)

        if not os.path.exists(dir):
            os.makedirs(dir)
        self.__failedReportHandler = open(reportPath, 'a+')

    def updatePassedTestCount(self, suiteName):
        '''
        Increment passed test count of respective suiteName
        Also increases the total test count
        '''
        self.__passedTestCases+=1
        self.__totalTestCases+=1

        if 'schema' in suiteName.lower():
            self.__SVPassedTestCases+=1
            self.__SVTotalTestCases+=1

        if 'error' in suiteName.lower():
            self.__EVPassedTestCases+=1
            self.__EVTotalTestCases+=1

        if 'data' in suiteName.lower():
            self.__DVPassedTestCases+=1
            self.__DVTotalTestCases+=1

        if 'flag' in suiteName.lower():
            self.__FVPassedTestCases+=1
            self.__FVTotalTestCases+=1

        if 'sanity' in suiteName.lower():
            self.__BCPassedTestCases+=1
            self.__BCTotalTestCases+=1

    def getTestStats(self):
        return [self.__totalTestCases, self.__passedTestCases, self.__failedTestCases]

    def updateFailedTestCount(self, suiteName):
        '''
        Increment failed test count of respective suiteName
        Also increase the total passed test count
        '''
        self.__failedTestCases+=1
        self.__totalTestCases+=1

        if 'schema' in suiteName.lower():
            self.__SVFailedTestCases+=1
            self.__SVTotalTestCases+=1

        if 'error' in suiteName.lower():
            self.__EVFailedTestCases+=1
            self.__EVTotalTestCases+=1

        if 'data' in suiteName.lower():
            self.__DVFailedTestCases+=1
            self.__DVTotalTestCases+=1

        if 'flag' in suiteName.lower():
            self.__FVFailedTestCases+=1
            self.__FVTotalTestCases+=1

        if 'sanity' in suiteName.lower():
            self.__BCFailedTestCases+=1
            self.__BCTotalTestCases+=1


    def getReportName(self):
        return self.__reportName


    def dumpReport(self, suiteName, report, dumpedReportName, url, message):
        '''
        Writes the whole report in a file under logs/<suiteName_Date>
        '''
        parent_dir = "logs_" + str(self.__currentDate)
        directoryName= suiteName+"_"+self.__currentDate
        parent_path = "../logs/" + parent_dir-+9
        upToDir = parent_path + "/" + directoryName
        try:
            os.mkdir(parent_path)
        except:
            pass
        try:
            os.mkdir(upToDir)
        except Exception:
            pass

        f = open(upToDir+"/"+ dumpedReportName, 'w')
        with f:
            f.write("URL = "+url)
            f.write("\n======================\n")
            f.write("RESULT: "+ message+ "\n")


            if len(self.__reportErrorMessage)>0:
                for temp in self.__reportErrorMessage:
                    f.write(temp+"\n")
            #f.write("Error: \n")
            f.write("========================\n")
            f.write(report[0:5000])
            del self.__reportErrorMessage[:]


    def setSuiteName(self, suiteName):
        self.__suiteName=suiteName

    def updateResult(self,valType,  testCaseObj, status):
        self.__resultTable[valType][status].update(testCaseObj)

    def writeReport(self):
        '''
        This function writes a whole report including its css, java script and HTML code.
        '''
        html = HTMLWriter()
        self.getReportHandler()
        self.getFailedReportHandler()
        with self.__reportHandler as handler, self.__failedReportHandler as failedHandler:

            self.writeReportHeader(handler, html)
            self.writeReportHeader(failedHandler, html, failureReport= True)
            
            if self.__SVTotalTestCases >0 :
#                 data = self.__resultTable['SchemaValidation']['Passed'] + self.__resultTable['SchemaValidation']['Failed']
                data1 = self.__resultTable['SchemaValidation']['Passed']
                data2 = self.__resultTable['SchemaValidation']['Failed']
                data1.update(data2)
                data = {}
                data.update(data1)
                self.writeSuiteReport(handler, 'SchemaValidation', data, self.__SVTotalTestCases, self.__SVPassedTestCases, self.__SVFailedTestCases)
            
            if self.__SVFailedTestCases>0:
                self.writeSuiteReport(failedHandler, 'SchemaValidation', self.__resultTable['SchemaValidation']['Failed'], self.__SVTotalTestCases, self.__SVPassedTestCases, self.__SVFailedTestCases)

            if self.__DVTotalTestCases >0 :
                data1 = self.__resultTable['DataValidation']['Passed']
                data2 = self.__resultTable['DataValidation']['Failed']
                data1.update(data2)
                data = {}
                data.update(data1)
                self.writeSuiteReport(handler, 'DataValidation', data, self.__DVTotalTestCases, self.__DVPassedTestCases, self.__DVFailedTestCases )
            
            if self.__DVFailedTestCases>0:
                self.writeSuiteReport(failedHandler, 'DataValidation', self.__resultTable['DataValidation']['Failed'], self.__DVTotalTestCases, self.__DVPassedTestCases, self.__DVFailedTestCases )

            if self.__FVTotalTestCases >0 :
#                 data = self.__resultTable['FlagValidation']['Passed'] + self.__resultTable['FlagValidation']['Failed']
                data1 = self.__resultTable['FlagValidation']['Passed']
                data2 = self.__resultTable['FlagValidation']['Failed']
                data1.update(data2)
                data = {}
                data.update(data1)
                self.writeSuiteReport(handler, 'FlagValidation', data, self.__FVTotalTestCases, self.__FVPassedTestCases, self.__FVFailedTestCases )
            
            if self.__FVFailedTestCases>0:
                self.writeSuiteReport(failedHandler, 'FlagValidation', self.__resultTable['FlagValidation']['Failed'], self.__FVTotalTestCases, self.__FVPassedTestCases, self.__FVFailedTestCases )

            if self.__EVTotalTestCases >0 :
#                 data = self.__resultTable['ErrorValidation']['Passed'] + self.__resultTable['ErrorValidation']['Failed']
                data1 = self.__resultTable['ErrorValidation']['Passed']
                data2 = self.__resultTable['ErrorValidation']['Failed']
                data1.update(data2)
                data = {}
                data.update(data1)
                self.writeSuiteReport(handler, 'ErrorValidation', data, self.__EVTotalTestCases, self.__EVPassedTestCases, self.__EVFailedTestCases )
            
            if self.__EVFailedTestCases>0:
                self.writeSuiteReport( failedHandler, 'ErrorValidation', self.__resultTable['ErrorValidation']['Failed'], self.__EVTotalTestCases, self.__EVPassedTestCases, self.__EVFailedTestCases )

            handler.write(''' <script> function expandCheckBoxes(){
                    classnames = document.getElementsByClassName("popup_window")
                    for (i = 0; i < classnames.length; i++) {
                        this.showTestDetail(classnames[i].id)
                        }

                    }
                </script>''')
            handler.write("\n</body></html>")

            failedHandler.write(''' <script> function expandCheckBoxes(){
                    classnames = document.getElementsByClassName("popup_window")
                    for (i = 0; i < classnames.length; i++) {
                        this.showTestDetail(classnames[i].id)
                        }

                    }
                </script>''')

            failedHandler.write("\n</body></html>")
            



    def writeSuiteReport(self, handler, suitName, data, totalTestCases, passedTestCases, failedTestCases):
        self.writeSuiteHeader(handler,suitName,totalTestCases, passedTestCases, failedTestCases)
        if not data:
            return
        
        sortedKeys = []
        ''' below is the logic for sorting out the test case ids so that report looks in order'''
        try:
            sortedKeys = [int(i) for i in data.keys()]
            sortedKeys = sorted(sortedKeys)
        except:
            sortedKeys = sorted(data.keys())

        headers = []
        tempHeaders = {}
        dataObjectColumns = data.get(str(sortedKeys[0])).keys()  # this will all values, but we need to filter those values where visible is false
        oneSet = data.get(str(sortedKeys[0]))  # it will give dictionary which will be diction having all columns
        '''below logic is to correct the order of the column on basis of order given by component developer'''
        for d in dataObjectColumns:
            if oneSet.get(d).get('visible'):
                tempHeaders.update({oneSet.get(d).get('order'): d})
#         print tempHeaders
        
        ''' tempHeaders should look like {'1': testCaseId, '2': URL, '3': description} etc
            below logic is to sort the keys of tempHeaders and get the correct ordered column names
        '''
        sortKeys = sorted(tempHeaders.keys())
        headers = []
        for k in sortKeys:
            headers.append(tempHeaders.get(k)) 
        
#         print headers
        
        ''' Below logic creates the actual html file '''
        handler.write('<table border=1>')
        handler.write('<tr>')
        for header in headers:
            handler.write('<th>'+header+'</th>')
        handler.write('</tr>\n')
        for index in sortedKeys:
            tuple = data.get(str(index))
            handler.write('<tr>')
            for key in headers:
                if tuple.get(key).get('value') == 'FAIL':
                    failed = self.writeFailedCell(tuple.get('testCaseId').get('value'), tuple.get('description').get('value'))
                    
                    handler.write(failed)
                else:
                    cellValue = tuple.get(key).get('value')
                    if key == 'description':
                        cellValue  = tuple.get('description').get('value').get('message')
                    handler.write('<td>'+str(cellValue)+'</td>')
            handler.write('</tr>\n')
            if failedTestCases>0:
                handler.write('</tr>\n')
        handler.write('</table>')

    
    def writeReportHeader(self, handler, htmlWriter, failureReport = False):
        handler.write("<html><body bgcolor=#E6E6FA>\n")
        if failureReport:
            handler.write("<head> <title>Failed Test Report for API-Automation</title></head>")
        else:
            handler.write("<head> <title>Test Report for API-Automation</title></head>")
        htmlWriter.write_css(handler)
        htmlWriter.startJavaScript(handler)

        htmlWriter.write_show_hide_inHTML(handler)
        htmlWriter.showTestDetail(handler)

        htmlWriter.endJavaScript(handler)
        if failureReport:
            handler.write("\n***********************<b>Failed Test Cases For Build : "+Globals.BUILDNO+"</b>************************</br>")
        else:
            handler.write("\n***********************<b>Results Summary For Build : "+Globals.BUILDNO+"</b>************************</br>")

        handler.write("\n<pre>")
        handler.write("\nTotal Test Cases in All suites  = "  + str(self.__totalTestCases))
        handler.write("\nPassed Test cases in All suites = " + str(self.__passedTestCases))
        handler.write("\nFailed Test cases in All suites = " + str(self.__failedTestCases))
        handler.write("\nNumber of API hit for this run  = " + str(Globals.apiCount))
        handler.write("</pre>")
        temp_list='</br><p>*********************************************************************</p>'
        expandFailedResult = '<b>Expand All Failed Tests </b><input type="checkbox" name="check" value="bar" \
        onclick="javascript:expandCheckBoxes()"/><br/><br/>'
        
        handler.write(temp_list)
        handler.write(expandFailedResult)


    def writeSuiteHeader(self, handler, suitName, totalTestCases, passedTestCases, failedTestCases):
        
        suitName = '<b>Suite Name : '+suitName+'</b>'
        handler.write(suitName)
        handler.write("\n<pre>")
        handler.write("\nTotal Test Cases  = "  + str(totalTestCases))
        handler.write("\nPassed Test cases = " + str(passedTestCases))
        handler.write("\nFailed Test cases = " + str(failedTestCases))
        handler.write('\n</pre>\n')

    def writeFailedCell(self, testCaseId, description ):
        import random
        
        label_id = str(testCaseId) + str(int(time.time())) + str(random.randrange(10,3000))
        fail_reason = str(description['failReason'])
        response = str(description['response'])
        div = '''<div id='''+"'div_"+label_id+'''\' class="popup_window">
        <div style='text-align: right; color:red;cursor:pointer'>
        <a onfocus='this.blur();' onclick="document.getElementById('div_'''+label_id+'''\').style.display = 'none' " >
        [x]</a>
        </div>''' +fail_reason+'''<br/><br/><b>Actual Response</b>: <div style="word-wrap:break-word;">'''+  str(response[0:2000]).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")  + ''' ...
        </div>'''

        failed_cell = "<td align=\"center\" ><b><a class=\"popup_link\" href=\"javascript:showTestDetail("+"'div_"+label_id+"')\" onfocus=\"this.blur();\">FAILED</a></b>" + div+"<label id=\"" + label_id + "\"><label></td>  <input id=input_"+ label_id + " type=hidden value=\""+fail_reason+ "\"""/> "
        return  failed_cell

