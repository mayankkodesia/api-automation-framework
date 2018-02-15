__author__ = 'LT-CSIN'

'''
Created on 28-Apr-2014
@author: Mayank Kodesia
'''
import os
import datetime

import testlink
import traceback
import framework.helper.Globals as Globals
from framework.helper.Globals import logs


class TestLinkHandler(object):
    '''
    This class is used to update the test cases inside the test link
    While updating API it is assumed that current Test Plan is "API Regression" and
    will add the test cases to this test plan and create a new build everytime when suites run.
    '''

    def __init__(self, planId, projectId, userKey):
        ''' For startup testLink we should have server URL and user keys generated through GUI '''
        os.environ["TESTLINK_API_PYTHON_SERVER_URL"] = "http://<test link server>/lib/api/xmlrpc/v1/xmlrpc.php"
        os.environ["TESTLINK_API_PYTHON_DEVKEY"] = userKey#"e4ba9a9f6e3f8cda0a96a989bd8082b2"  #Automation user on Testlink
        self.tls = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)

        self.projectID = projectId
        self.testPlanID = planId


    def TestLinkUpdate(self, testCaseId ,testCaseStatus,platformID=None, reason=None):
        try:
            if testCaseStatus == "PASS":
                testCaseStatus = 'p'
            else:
                testCaseStatus = 'f'
            ''' We need to mark every test case as Automated, so this need to be exectuted for first few cycles
            later on we can remove this '''
            self.tls.setTestCaseExecutionType(testCaseId,1, self.projectID,2 )
            if reason:
                Notes = str(reason)
            else:
                Notes="Automated Results"

            tcinfo = self.tls.getTestCase(None, testcaseexternalid=testCaseId)
            self.tls.reportTCResult(testcaseid = tcinfo[0]['testcase_id'],testplanid = self.testPlanID, buildname=Globals.BUILDNO, status=testCaseStatus, notes=Notes)
        except Exception as e:
            logs.error("Perhaps test case Id not found in test Link, Exception is :{}".format(e))
            # logs.error(traceback.print_exc())

    def addTestCaseToTestPlan(self, testCaseId):
        try:
            ''' Add the executing test case in test plan, if already exists throws a exception '''
            self.tls.addTestCaseToTestPlan(self.projectID, self.testPlanID, testCaseId, 1)
        except Exception:
            pass
#             print "Could not add test case to test plan id {}".format(self.testPlanID)
#             print traceback.format_exc()


    def createBuild(self):
        ''' Create a Build in testLink which is passed in command line '''
        try:
            self.tls.createBuild(self.testPlanID, Globals.BUILDNO, str(datetime.datetime.now().strftime("%I:%M%p %d %B %Y")))
        except Exception:
            logs.error("Build already exist under test Plan {} and build No {}".format(self.testPlanID, Globals.BUILDNO))




