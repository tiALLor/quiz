from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import random
import datetime

# now = datetime.datetime.today()

@dataclass
class Question:
    """Question to be used in quiz"""

    id: int
    active: bool
    question: str
    possible_answers: list
    correct_answer: str
    stat_times_used: str = 0
    stat_correctly_answ: str = 0

    def ask_question(self):
        if len(self.possible_answers) == 1:
            pass
        else:
            pass
            
        pass

    def set_is_active(self):
        pass

    def question_stats(self):
        pass


@dataclass
class Database_of_questions:
    """Database of questions"""

    questions: dict[int, Question] = field(default_factory=dict)

    def add_question(self):
        print("Question creation:")   
        try:
            id = max(self.list_of_ids) + 1
        except:
            id = 0
        active = True
        the_question = input("Please input the question e.g. '1 + 1 = ?' ")
        while True:
            print("\nPlease specify the type of quiz question: ")
            print("1 for quiz question with possible answers")
            print("2 for free_form question with direct answer")
            q_type = input("Type 1 or 2 ? ")
            if q_type == "1":
                possible_answers, correct_answer = get_possible_answers()
                break
            elif q_type == "2":
                possible_answers, correct_answer = get_free_form_answers()
                break
            else:
                print("'1' or '2' is expected")
        question = Question(
                        id=id,
                        active=active,
                        question=the_question,
                        possible_answers=possible_answers,
                        correct_answer=correct_answer
        )
        self.questions[id] = question

    def get_question(self, question_id: int):
        return self.question.get(question_id)
    
    def get_database_from_csv(self, file):
        pass

    def store_database_in_csv(self):
        pass

    def list_of_ids(self):
        return self.questions.keys()
    

    

def get_possible_answers(no_of_answers=3):
    possible_answers = []
    for i in range(no_of_answers):
        while True:
            answer = input(f"\nPlease input a possible answer no. {i +1}: ")
            if answer:
                possible_answers.append(answer)
                break
    while True:
        correct_answer = int(input("Which answer is correct?"))
        if correct_answer in range(1, (no_of_answers + 1)):
            correct_answer = possible_answers[correct_answer-1]
            break
        else:
            print(f"Please provide an answer in range 1-{no_of_answers})")
    return possible_answers, correct_answer

def get_free_form_answers():
    possible_answers = []
    correct_answer = get_data("Please input the correct answer?")
    return possible_answers, correct_answer

def get_data(question):
    while True:
        answer = input(question)
        if answer:
            break
        else:
            print(f"Please provide a correct answer!")
    return answer

if __name__=="__main__":


    database = Database_of_questions()
    database.add_question()
    database.store_database_in_csv()
