import unittest
import os
import os.path
import subprocess32 as subprocess
from subprocess32 import PIPE
from gradescope_utils.autograder_utils.decorators import weight, visibility
import yaml

BASE_DIR = './test_data'


class TestMetaclass(type):
    """
    Generates exercises and checks them against test cases
    """
    def __new__(self, name, bases, attrs):
        data_dir = attrs['data_dir']
        tests = attrs['tests']
        for test in tests:
            attrs[self.test_name(test[:-4])] = self.generate_test(data_dir, test[:-4])
        #print(name, bases, attrs)
        return super(TestMetaclass, self).__new__(self, name, bases, attrs)

    @classmethod
    def generate_test(self, dir_name, test):
        """ Returns a testcase for the given directory """
        def load_file(path):
            full_path = os.path.join(BASE_DIR, dir_name, path)
            #print(full_path)
            if os.path.isfile(full_path):
                with open(full_path, 'rb') as f:
                    return f.read()
            return None

        def load_settings():
            settings_yml = load_file('settings.yml')

            if settings_yml is not None:
                return yaml.safe_load(settings_yml) or {}
            else:
                return {}

        settings = load_settings()

        def compare_output(student_output, expected_output):
            # actual_student_output = student_output
            # actual_expected_output = expected_output
            # line = 0
            # word = 0
            # student_output = student_output.strip()
            # expected_output = expected_output.strip()
            # student_output = student_output.split('\n')
            # expected_output = expected_output.split('\n')

            # min_len = min(len(student_output), len(expected_output))
            # for i in range(min_len):
            #     line+=1
            #     word = 0
            #     student_words = student_output[i].split(" ")
            #     expected_words = expected_output[i].split(" ")
            #     min_len_words = min(len(student_words), len(expected_words))
            #     for j in range(min_len_words):
            #         word+=1
            #         if student_words[j]!=expected_words[j]:
            #             print(f"First mismatch found at: Line - {line} and Word - {word}")

            return student_output == expected_output
            #return student_output.strip().replace('\r','').replace('\n','') == expected_output.decode().strip().replace('\r','').replace('\n','')

        @weight(settings.get('weight', 2))
        @visibility(settings.get('visibility', 'visible'))

        def compile_and_run(self):
            
            # Get path to exercise file
            #exercise_number = dir_name.split("_")[1]
            path = os.path.join(BASE_DIR, dir_name, dir_name +'.cpp')
            

            #Compile code
            path_to_Exercise1 = BASE_DIR + "/Exercise1/"
            compile_cmd = f"g++ -o {path_to_Exercise1}Exercise1 {path_to_Exercise1}Exercise1.cpp {path_to_Exercise1}Fraction.h {path_to_Exercise1}Fraction.cpp"
            compile_result = subprocess.run(compile_cmd, shell=True)
            #print(compile_cmd)
            #Check for Compilation error
            if compile_result.returncode != 0:  
                print(f"Exercise - Compilation error")
                # Note to Graders - we can add reason for the compilation fail here
                self.assertEqual(compile_result.returncode, 0, 'Compilation error')
                return 
            
            
            executable_name = './'+path[:-4]  # Get the name without .cpp
            # Note to Graders - we can add a loop here for running the code against multiple test cases
            input_data = load_file(test +'.txt')
            
            print("------------------------------>>   input <<----------------------------- \n", input_data.decode())

            # Run the compiled executable
            process = subprocess.Popen([executable_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate(input=input_data) 
            
            stdout_str = stdout.decode()  # Decode stdout from bytes to string
            stderr_str = stderr.decode()  # Decode stderr from bytes to string
            temp_student_output = stdout_str
            # Check for runtime errors
            if process.returncode != 0:
                print(f"Exercise - Compilation or runtime error:", stderr_str)
                self.assertEqual(process.returncode, 0, 'Compilation or runtime error')
                return

            # Read expected output
            last_second_digit = test[-2] if test[-2]!='t' else ''
            expected_output = load_file('output'+ last_second_digit + test[-1] +'.txt')
            temp_expected_output = expected_output.decode()
            escapeChars = ''.join([chr(char) for char in range(1, 32)]);
            translator = str.maketrans('', '', escapeChars);
            stdout_str = stdout_str.strip().translate(translator);
            expected_output = expected_output.decode().strip().translate(translator);
                

            # Compare student's output with expected output
            # if compare_output(stdout_str, expected_output):
            #     print(f"Exercise - Passed")
            # else:
            #     print(f"Exercise - Failed")
            print("------------------------------>>   Student's output <<----------------------------- \n",temp_student_output)
            print("------------------------------>>   Expected output <<-------------------------------\n",temp_expected_output)
            #print("---", self.assertEqual(stdout_str,expected_output))
            self.assertEquals(stdout_str, expected_output)
                
        return compile_and_run

    @staticmethod
    def klass_name(dir_name):
        return '{0}'.format(''.join([x.capitalize() for x in dir_name.split('_')]))

    @staticmethod
    def test_name(dir_name):
        return '{0} of'.format(dir_name)


def build_test_class(data_dir, tests):
    klass = TestMetaclass(
        TestMetaclass.klass_name(data_dir),
        (unittest.TestCase,),
        {
            'data_dir': data_dir,
            'tests': tests
        }
    )
    return klass


def find_data_directories():
    return filter(
        lambda x: os.path.isdir(os.path.join(BASE_DIR, x)),
        os.listdir(BASE_DIR)
    )
def list_files_starting_with(name, prefix):
    try:
        # List all files in the specified directory
        directory = BASE_DIR + "/" + name
        files = os.listdir(directory)
        
        # Filter files that start with the specified prefix
        matching_files = [file for file in files if file.startswith(prefix)]
        
        return matching_files
    except OSError as e:
        print(f"Error reading directory {directory}: {e}")
        return []
