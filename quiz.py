from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import random
import datetime
import csv
import sys


# now = datetime.datetime.today()

@dataclass
class Question:
    """Question to be used in quiz"""

    id: int
    enabled: bool
    question: str
    possible_choices: list
    correct_answer: str
    stat_times_used: str = 0
    stat_correct_answ: str = 0

    def ask_question(self, type="fix_possition"):
        print(f"Question: {self.question}")
        if len(self.possible_choices) == 1:
            # change to use of get_data()
            users_answer = input("Your answer: ")
        elif len(self.possible_choices) >1:
            choices = self.possible_choices.copy()
            if type == "random_possition":
                random.shuffle(choices)
            displ_choices(choices)
            users_answer = get_from_choices(choices,
                                            len(choices),
                                            "Your answer: ")
        self.stat_times_used += 1
        if users_answer.strip().lower() == self.correct_answer.lower():
            print("\nCorrect!\n")
            self.stat_correct_answ +=1
            return True
        else:
            print("Incorrect! Correct answer is: ", self.correct_answer, "\n")
            return False
    

    def set_enabled(self, value):
        self.enabled = value

    def show_question_stats(self):
        print("\n", ("=" * 10))
        print(f"Question ID: {self.id}")
        print(f"Question Enabled: {self.enabled}")
        print(f"Question: {self.question}\n")
        if len(self.possible_choices) == 1:
            print("Possible choices: None. Free form question")
        elif len(self.possible_choices) >1:
            print("Possible choices:")
            displ_choices(self.possible_choices)
        print(f"\nCorrect answer: {self.correct_answer}")
        print("-" * 10)
        print(f"Question displayed: {self.stat_times_used}")
        try:
            correct_perc = self.stat_correct_answ * 100/ self.stat_times_used
        except ZeroDivisionError:
            correct_perc = "N/A - not yet used"
        print(f"Correctly answered [%]: {correct_perc} ")
        print("=" * 10)

@dataclass
class Database_of_questions:
    """Database of questions"""

    questions: dict[int, Question] = field(default_factory=dict)

    def add_question(self):
        print("\nQuestion creation:")
        try:
            id = (max(self.list_of_ids()) + 1)
        except ValueError:
            """if database of questions is empty"""
            id = 1
        enabled = True
        the_question = input("Please input the question e.g. '1 + 1 = ?' ")
        print("\nPlease specify the type of quiz question: ")
        print("1 for quiz question with possible choices")
        print("2 for free_form question with direct answer")
        
        while True:
            q_type = input("Type 1 or 2 ? ")
            if q_type == "1":
                possible_choices, correct_answer = get_possible_choices()
                break
            elif q_type == "2":
                possible_choices, correct_answer = get_free_form_choices()
                break
            else:
                print("'1' or '2' is expected")
        question = Question(
                        id=id,
                        enabled=enabled,
                        question=the_question,
                        possible_choices=possible_choices,
                        correct_answer=correct_answer
        )
        self.questions[question.id] = question

    def get_question(self, question_id: int):
        return self.questions.get(question_id)
    
    def get_database_from_csv(self):
        with open("questions.csv", mode='r') as database_file:
            reader = csv.DictReader(database_file)
            for row in reader:
                question = Question(
                    id=int(row["id"]),
                    enabled=bool(row["enabled"]),
                    question=row["question"],
                    possible_choices=row["possible_choices"].split(';'),
                    correct_answer=row["correct_answer"],
                    stat_times_used=int(row["stat_times_used"]),
                    stat_correct_answ=int(row["stat_correct_answ"])
                )
                self.questions[question.id] = question

    def store_database_in_csv(self):
        with open("questions.csv", "w", newline='') as database_file:
            fieldnames = ["id", "enabled", "question",
                          "possible_choices", "correct_answer",
                          "stat_times_used", "stat_correct_answ"]
            writer = csv.DictWriter(database_file, fieldnames=fieldnames)
            writer.writeheader()
            for question in self.questions.values():
                writer.writerow({
                    "id": question.id,
                    "enabled": question.enabled,
                    "question": question.question,
                    "possible_choices": ';'.join(question.possible_choices),
                    "correct_answer": question.correct_answer,
                    "stat_times_used": question.stat_times_used,
                    "stat_correct_answ": question.stat_correct_answ
                })
            
    def summary(self):
        for question in self.questions.values():
            question.show_question_stats()

    def list_of_ids(self):
        return self.questions.keys()
    
    def get_active_questions(self):
        active_questions = []
        for question in self.questions.values():
            if question.enabled == True:
                active_questions.append(question.id)
        return active_questions
    
# ====================================

def get_possible_choices():
    possible_choices = []
    while True:
        try:
            no_of_choices = int(input("How many possible answers (2 to 5)? "))
            if no_of_choices in range(2,6):
                break
        except:
            continue
    for i in range(no_of_choices):
        while True:
            answer = input(f"\nPlease input a possible answer no. {i +1}: ")
            if answer:
                possible_choices.append(answer)
                break
    
    correct_answer = get_from_choices(possible_choices,
                                      no_of_choices,
                                      "The correct answer is:")
    return possible_choices, correct_answer

def get_from_choices(data, no_of_choices, question):
    while True:
        try:
            users_answer = int(input(question)) -1
            if users_answer in range(0, no_of_choices):
                users_answer = data[users_answer]
                break
            else:
                raise ValueError
        except ValueError or TypeError:
            print(f"Please provide an answer in range 1-{no_of_choices}.")
    return users_answer

def get_free_form_choices():
    possible_choices = []
    correct_answer = get_data("Please input the correct answer? ")
    return possible_choices, correct_answer

def get_data(question, type="str"):
    while True:
        try:
            answer = input(question)
            if type == "int":
                answer = int(answer)
            if type == "foat":
                answer = float(answer)
            if answer:
                return answer
            else:
                print(f"Please provide a answer!")
        except ValueError:
            print("Please provide valud number (float or int).")
    

def displ_choices(possible_choices):
    for i, possible_answer in enumerate(possible_choices, 1):
                print(f"{i}. {possible_answer}")

def primary_screen():  
    while True:
        print("""
            -------------------------------------------
            Please choose what you would like to do:
            -------------------------------------------
            1. Add a question
            2. Question statistics / Show question in database
            3. Activate or disable a question from testing
            4. Practice
            5. Testing
            6. End
            -------------------------------------------
            """)
        mode = input("Please make a choose! ")
        if mode == "1":
            database.add_question()
            database.store_database_in_csv()
            print("Question was succesfully added.\n")
        elif mode == "2":
            database.summary()
        elif mode == "3":
            queston_deactivation()
        elif mode == "4":
            pass
        elif mode == "5":
            if can_be_run() == True:
                mode_testing()
        elif mode == "6":
            print("Bye.")
            sys.exit()
        else:
            print("Please make a valid choice.")
    return


def queston_deactivation():
    database.summary()
    print("""
          Please provide ID for question,
          which should be enabled/dissabled,
          from use in tests and practice mode.
          """)
    while True:
        question_id = input("ID /'None' for leave: ").lower()
        try:
            if question_id == "none":
                return
            elif int(question_id) not in database.list_of_ids():
                raise ValueError("ID is not valid")
        except Exception as e:
            print(f"Error {e} occured")
        question = database.questions[int(question_id)]
        question.show_question_stats()
        if get_confirmation("You are to change the question status.") == True:
            if question.enabled == False:
                question.set_enabled(True)
                print("Question was Enabled")
            elif question.enabled == True:
                question.set_enabled(False)
                print("Question was Dissabled")
        else:
            return
        question.show_question_stats()
        database.store_database_in_csv()
        return
        

def get_confirmation(question):
    print(question)
    while True:
        confirmation = input("Continue? Y/ N ").lower()
        if confirmation == "y":
            print("Confirmed")
            return True
        elif confirmation == "n":
            print("Canceled")
            return False
        else:
            print("Please answer Y/ N")


def mode_testing():
    print("Testing mode initialized!\n")
    active_questions = database.get_active_questions()
    while True:
        numb_of_questions = get_data("How many question shall be in test? ","int")
        if numb_of_questions <= len(active_questions):
            break
        print(f"Only {len(active_questions)} are active.")
    
    test_question_ids = []
    while len(test_question_ids) < numb_of_questions:
        value = random.choice(active_questions)
        if value not in test_question_ids:
            test_question_ids.append(value)
    random.shuffle(test_question_ids)

    test_stat_correct = 0
    test_stat_incorrect = 0
    for test_question_id in test_question_ids:
        question = database.questions[test_question_id]
        answ_is_correct = question.ask_question(type="random_possition")
        if answ_is_correct == True:
            test_stat_correct += 1
        elif answ_is_correct == False:
            test_stat_incorrect += 1

    save_print(test_results(test_stat_correct, test_stat_incorrect))

def can_be_run():
    active_questions = database.get_active_questions()
    if len(database.list_of_ids()) < 5 or len(active_questions) < 3:
        print("""
        Minimal 5 questions in database (from which are at least 3 active) 
        are required to run a practice or test mode.
              """)
        return False
    else:
        return True

def test_results(test_stat_correct, test_stat_incorrect):
    total_questions = test_stat_correct + test_stat_incorrect
    now = datetime.datetime.today()
    test_report = [
        "=================",
        f"Test results from testting on: {now}",
        f"Correct anwers: {test_stat_correct}",
        f"from {total_questions} questions",
        f"% of correct answers: {(test_stat_correct * 100 / total_questions):.2f}",
        "=================",
        "\n",
        ]
    return test_report

    

def save_print(test_results):
    try:
        with open("results.txt", "a") as file:
            for line in test_results:
                print(line)
                file.write(f"{line}\n")

    except Exception as e:
        print(f"Results were not saved. Error: {e}")




if __name__=="__main__":
    
    database = Database_of_questions()
    try:
        database.get_database_from_csv()
        print("Database from file was loaded")
    except Exception as e:
        print("Database from file could't be loaded")
        print(f"Exception: {e} occured!")
        print("You can continue and create new database!")
    primary_screen()