# C++ Assignment Autograding

This is an example of using Python and the autograding-utils library to implement autograding for a C++ assignment. In this assignment, you can have multiple exercises within a single assignment file, and the communication with the student's code is done exclusively through standard input (std::cin). The student's code will be compiled and executed, and the results will be compared with reference solutions to determine the test case outcomes.

## Building and Executing Code

Clone the project and upload its zip file on Gradescope's Programming assignment section.

## Behind the Scenes Workflow

### 1. Code Submission Handling

- When students submit their code on Gradescope, the system utilizes a `run_autograder` file, which is a shell script responsible for handling code submissions.

- The `run_autograder` script performs several tasks, including the organization of submitted code. It relocates the student's code to a designated folder within the `test_data` directory. This folder structure is organized to separate exercises, with each exercise having its own folder.

- Following code organization, the script changes the working directory to the source folder where the autograding process will occur.

### 2. Running Tests

- Within the source folder, a Python script named `run_tests.py` is executed. This script contains the logic to initiate the testing process.

- `run_tests.py` calls methods from the `test_generator` file. These methods are designed to loop through each exercise, compile the student's code, and run the tests individually for each exercise.

- During this phase, test cases are executed, and the results are collected.

### 3. Result Generation

- After running all the tests, `run_tests.py` opens a `result.json` file. This JSON file serves as a structured container for storing the information required by Gradescope to display the final results.

- The `result.json` file is populated with relevant data, including test outcomes, scores, and any additional information needed for grading.

## Adding Test Cases

To add test cases for this assignment, follow these guidelines:

- Create a new directory within the `test_data` directory for each test case.
- For each test case, include the following files:
  - **input**: This file contains the input data that will be provided to the student's program via standard input (std::cin).
  - **output**: This file serves as the reference output for the test case. The student's program's output will be compared against this file to determine if the test case passed or failed.
  - **settings.yml**: This file can hold various settings for the test case. You can specify the weight assigned to the test case in this file, or any other relevant configuration.

Please note that the 'settings.yml' file mentioned above can be used for future enhancements or additional configurations but is currently not implemented in this example.

## Example Program

An example C++ program is provided as a reference for this assignment. You can find it here: [`exercise_1.cpp`](https://github.com/Divyashree-iyer/autograder/blob/main/test_data/exercise_1/exercise_1.cpp). This program demonstrates a simple scenario for illustration purposes.

## Providing Input to the Program

You can provide input to the student's program by:
- Include the input data within the 'input' file for each test case, which will be fed to the program via standard input (std::cin).

## Generated Output

This program generates a `result.json` file, which is stored inside the `results` folder. The `result.json` file is used by the autograder to show results to students who have uploaded their code.

Feel free to customize this structure and adapt the language to suit your specific assignment and requirements. Good luck with your C++ assignment autograding!
