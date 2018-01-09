__author__ = 'LT-Mac-Akumar'
'''
import json
import inspect

class dataProvider(object):

    def method_decorator(self, fn, dataForFunction):
        "Example of a method decorator"
        def decorator(*args, **kwargs):
            # Get the arguments of the function
            args_name = inspect.getargspec(fn)[0]
            errors = []
            for testDataForFunction in dataForFunction:
                kwargs = {}
                for param_name in args_name:
                    kwargs[param_name] = testDataForFunction[param_name]

                try:
                    fn(**kwargs)
                except AssertionError as e:
                    errors.append(e)
            if errors:
                print errors

            # return fn(*args, **kwargs)

        return decorator


    def __init__(self, testClass=None, testFile=None, converters=None):
            self.testFile = testFile
            self.converters = converters
            self.testClass = testClass

    def __call__(self, cls, *args):

        # def class_rebuilder
        testClass = self.testClass
        # testClassInstance = testClass()
        with open(self.testFile) as fh:

            totalData = json.load(fh)
            for testDataKey in totalData.keys():
                    # Convert the test data in case any converters are registered
                    if self.converters != None:
                        for converter in self.converters:
                            converterInstance = converter()
                            convertedData = []
                            for testData in totalData[testDataKey]:
                                convertedData.append(converterInstance.convert(testData))
                            totalData[testDataKey] = convertedData
        print inspect.getmembers(testClass, predicate=inspect.ismethod)
        # def class_rebuilder(cls):
        #     "The class decorator example"
        class NewClass(cls):
                def __init__(self, obj):
                    objInstance = getattr(self, obj)

                    setattr(self,obj , objInstance)
                    print obj


        return NewClass
        # return class_rebuilder
        
'''
        