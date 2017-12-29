
import unittest
import csv

from DB import mongodb_engine



TESTMODULES = __import__('TestCase').__all__


def getTestObject():
    
    """
     GET TEST OBJECT...
    """
    test_object = []
    for testmodule in TESTMODULES:
        for testclass in dir(testmodule):
            if "Test" in testclass:
                test_object.append(getattr(testmodule,testclass))
    return test_object


# print(getTestObject())

testCaseName  = []

def execute_test():
    test_suit = getTestObject()
    result = []
    for test_class in test_suit:
        loader = unittest.TestLoader()
        suite= loader.loadTestsFromTestCase(test_class)
        # testCaseName += unittest.getTestCaseNames(test_class,prefix='test')
        global testCaseName
        testCaseName += loader.getTestCaseNames(test_class)
        # for case in suite:
        #     testCaseName.append(case._testMethodName)
        test_result = unittest.TextTestRunner(verbosity=2).run(suite)
        result.append(test_result)
    return result


def output():
    test_results = execute_test()
    errors = []
    failures = []
    error_count = 0
    failures_count = 0
    total_case = 0
    for test_result in test_results:
        errors += test_result.errors
        failures += test_result.failures
        error_count += len(errors)
        failures_count += len(failures)
        total_case +=test_result.testsRun
    pass_count = total_case -(failures_count+error_count)
    if total_case != 0:
            pass_rate = str(round(pass_count*100/total_case,2)) + "%"
    with open('D:\case.csv',"w+",newline="") as cvs_file:
        header=["case_name","error_reason","failed_reason","status"]
        writer= csv.DictWriter(cvs_file,fieldnames=header)
        writer.writeheader()        
        if errors:
            for case,reason in errors:
                _id ="".join(case.id().split('.')[-1:])
                testCaseName.remove(_id)
                error_row={"case_name":_id,'error_reason':reason,"failed_reason":"--","status":"Error"}
                writer.writerow(error_row)
        if failures:
            for case,reason in failures:
                _id ="".join(case.id().split('.')[-1:])
                testCaseName.remove(_id)
                failed_row={"case_name":_id,'error_reason':"--","failed_reason":reason,"status":"Failed"}
                writer.writerow(failed_row)
        for case in testCaseName:
            pass_row={"case_name":case,'error_reason':"--","failed_reason":"--","status":"Pass"}
            writer.writerow(pass_row)
            
        
if __name__ == "__main__":
    print(output())