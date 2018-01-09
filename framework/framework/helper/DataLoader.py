__author__ = 'LT-Mac-Akumar'
__updatedAndCustomizedBy__ = 'mayank kodesia'

import json
import inspect
import Globals as Globals
class dataloader(object):

    ''' Initialize the Test Decorator.
    It will take the following arguments, besides self:
    1. testName : The name of the test. This name is used to find the correct data set for the test case.
    2. testFile: The name of the JSON file to load the data from
    3. converters : The list of classes, if any, that will will be called to convert the test data before it is passed to the actual test.
     '''
    def __init__(self, testFile, testName=None, converters=None):
        self.testFile = testFile
        self.converters = converters
        self.testName = testName
        

    ''' Method that is called once for each Decorator instance.
    This method is responsible for loading the data from the test file,
    converting it if necessary
    and finally passing the test data to the appropriate test method.
    It collects any Assertion failures for the test method and throws
    the list of errors after running each data set in the list for the given test method.
    '''
    def __call__(self, f, *args):
        funcName = f.func_name
        with open(self.testFile) as fh:
#             print self.testFile
            totalData = json.load(fh)
            testName = funcName;
            # if function name is not passed in __init__ then testName == funcName before decorator is mentioned
            if self.testName is not None:
                testName = self.testName
            for testDataKey in totalData.keys():
                if testDataKey == testName : # if the funcName is matching with the jsonData parent key 
                    # Convert the test data in case any converters are registered
                    if self.converters != None:
                        for converter in self.converters:
                            converterInstance = converter()
                            convertedData = []
                            for testData in totalData[testDataKey]:# i.e. all those tests which are going to be validated using this function, call that converter function
                                # now that json block will be returned and appended to convertedData list, which will be again replace old data 
                                convertedData.append(converterInstance.convert(testData))
                            totalData[testDataKey] = convertedData

                    # Get arguments names as a list:
                    args_name = inspect.getargspec(f)[0]

                    dataForFunction = totalData[testName]
                    # filtering function tests if there are TEST_TO_RUN is passed 
                    if Globals.TEST_TO_RUN:
                        #dataForFunction is a list
                        tempData = []
                        for jsonBlock in dataForFunction:
                            for key, value in Globals.TEST_TO_RUN.iteritems():
                                # first we check if the key and value are in jsonBlock or not
                                # if found then we check if same key corresponds to same value or not
                                if key in jsonBlock.keys() and value in jsonBlock.values():
                                    if jsonBlock.get(key) == value:
                                        tempData.append(jsonBlock)
                                        # once that jsonBLock is appended, this should move to next block
                                        # this is done to cover a issue where if -testToRun has same values of single block 
                                        # that test case was running twice
                                        break
                        
                        dataForFunction = tempData
#                         print "dataForFunction: ", dataForFunction
                        
                    errors = []
                    for testDataForFunction in dataForFunction:
                        Globals.TEST_DATA = testDataForFunction
                        kwargs = {}
                        for param_name in args_name:
                            try:
                                kwargs[param_name] = testDataForFunction[param_name] if testDataForFunction.has_key(param_name) else Globals.CLASS_OBJ
                            except Exception as e:
                                print e
                                print kwargs
                        try:
                            f(**kwargs)
                        except AssertionError as e:
                            errors.append(e)
                    if errors:
                        print errors
            
