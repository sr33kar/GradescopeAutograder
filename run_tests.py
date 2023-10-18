import unittest
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner
from test_generator import find_data_directories, build_test_class, TestMetaclass, list_files_starting_with

if __name__ == '__main__':
    suite = unittest.TestSuite()

    for name in find_data_directories():
        print(name)
        tests = list_files_starting_with(name, "input")
        klass = build_test_class(name, tests)
        print(tests)
        for test in tests:
            suite.addTest(klass(TestMetaclass.test_name(test[:-4])))

    with open('/autograder/results/results.json', 'w') as f:
        JSONTestRunner(visibility='visible', stream=f).run(suite)