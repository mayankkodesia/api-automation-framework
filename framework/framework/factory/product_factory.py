from framework.helper import Report, productException
from framework.helper.Globals import logs


__author__ = 'LT-CSIN'


class ProductFactory(object):
    """
    """
    def __init__(self):
        pass

    def run(self, endpoints, validations, componentObj, testCaseMatchedWith=None):
         
        self.test_suite = componentObj
        for ep in endpoints:
            logs.info("*************Running automation for " + str(ep)+ "*************")
            obj = self.test_suite.getObject(ep)
            obj.run(validations, testCaseMatchedWith)
            logs.info("*************Completed automation for " + str(ep)+ "*************")
        logs.info("************* Started Writing report *************")
        componentObj.getReport().writeReport()
        import framework.helper.writeSummary as summ
        summ.main()
        logs.info("************* Finished Writing report *************")

