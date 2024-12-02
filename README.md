# quiz
quiz - interactive learning tool


# Project's Title
Quiz

# Project Description
Quiz - interactive learning tool with modes:
- mode for adding question
- question statistics
- active/ disabled questions - management of questions
- practice mode
- test mode
- history of test results
- user profile mode ()

Mode for adding question:
The questions are stored in a file (file questions.csv).
Quiz support 2 type of questions:
- quiz = user is choosing answer from several options
- free-form = user need provide an answer as input, which will be compared with awaited answer (string input vs awaited string)

Question statistics:
- unique ID number
- status (question is active or not)
- question text
- number of times used
- percentage of times it was answered correctly

Minimal 5 questions in database (from which are at least 3 active) are necessary to run a practice or test mode.

Practice mode:
- questions are shown in endless loop until interrupted by user
- questions are shown randomly but success history is taken in account

Test mode:
- user is specifying number of questions in quiz (number can not be larger as number of active questions)
- Questions are chosen fully randomly and appear only once at most in test
- on the test and score is shown

History of test results:
- is stored in separate file - results.txt
- date and time are stored also



# Table of content (optional)
- file quiz.py
- file questions.csv
- file test_stats.csv
- results.txt
- tests (3 unit tests)


# How to Install and Run the Project
The program will be run with quiz.py


# How to Use the Project



# License
MIT