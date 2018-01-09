'''
Created on 23-Dec-2014
@author: Satish Mishra
'''

import unittest
import framework.helper.Globals as Globals

class iSightAutomationTestCase(unittest.TestCase):
    """All the test cases should inherit this class!"""
    def runTest(self, validations, testMatchedWith=None):
        if testMatchedWith is None:
            self.testMatchedWith = ""
        else:
            self.testMatchedWith = testMatchedWith
        try:
            loader = unittest.TestLoader()
            total_test_list = loader.getTestCaseNames(self)
            if "ALL" in validations:
                suite = loader.loadTestsFromNames(total_test_list, self.__class__)
            else:
                test_list  = []
                if 'SV' in validations:
                    test_list += (list(filter(self.svTestList, total_test_list)))
                if 'DV' in validations:
                    test_list += (list(filter(self.dvTestList, total_test_list)))
                if 'EV' in validations:
                    test_list += (list(filter(self.evTestList, total_test_list)))
                if 'FV' in validations:
                    test_list += (list(filter(self.fvTestList, total_test_list)))
                if 'sanity' in validations:
                    test_list += (list(filter(self.sanityTestList, total_test_list)))
                suite = loader.loadTestsFromNames(test_list, self.__class__)
            unittest.TextTestRunner(verbosity=2).run(suite)
        except Exception as e:
            print str(e)

    def svTestList(self, str):
        return  "test_SV" in str and self.testMatchedWith in str

    def dvTestList(self, str):
        return  "test_DV" in str and self.testMatchedWith in str

    def evTestList(self, str):
        return  "test_EV" in str and self.testMatchedWith in str

    def fvTestList(self, str):
        return  "test_FV" in str and self.testMatchedWith in str

    def sanityTestList(self, str):
        return  "test_sanity" in str and self.testMatchedWith in str

    def getReportObj(self):
        return  self.report
