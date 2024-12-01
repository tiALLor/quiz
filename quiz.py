from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import random
import datetime
import csv


# now = datetime.datetime.today()

@dataclass
class Question:
    """Question to be used in quiz"""

    id: int
    active: bool
    question: str
    possible_choices: list
    correct_answer: str
    stat_times_used: str = 0
    stat_correct_answ: str = 0

    def ask_question(self):
        print(f"Question: {self.question}")
        if len(self.possible_choices) == 1:
            users_answer = input("Your answer: ")
        elif len(self.possible_choices) >1:
            choices = self.possible_choices.copy()
            random.shuffle(choices)
            displ_choices(choices)
            users_answer = get_from_choices(choices, len(choices))

            # while True:
            #     users_answer = int(input("Your answer: "))
            #     if users_answer in range(1, (len(choices))):
            #         users_answer = choices[users_answer]
            #         break
            #     else:
            #         print(f"Answer in range 1-{len(choices)})")
        
        if users_answer.strip().lower() == self.correct_answer.lower():
            print("\nCorrect!")
            self.stat_correct_answ +=1
        else:
            print("Incorrect! Correct answer is: ", self.correct_answer)
        self.stat_time_used += 1

    def set_is_active(self, active):
        self.active = active

    def question_stats(self):
        print("=" * 10)
        print(f"Question ID: {self.id}")
        print(f"Question Status: {
            "Enabled" if self.active == True else "Disabled"}")
        print(f"Question: {self.question}\n")
        if len(self.possible_choices) == 1:
            print("\nPossible choices: None. Free form question")
        elif len(self.possible_choices) >1:
            print("\nPossible choices:")
            displ_choices(self.possible_choices)
        print(f"\nCorrect answer: {self.correct_answer}\n")
        print("=" * 10)
        print(f"Question displayed: {self.stat_times_used}")
        correct_perc = self.stat_correct_answ * 100/ self.stat_times_used
        print(f"Correctly answered: {correct_perc} %")
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
        active = True
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
                        active=active,
                        question=the_question,
                        possible_choices=possible_choices,
                        correct_answer=correct_answer
        )
        self.questions[question.id] = question

    def get_question(self, question_id: int):
        return self.question.get(question_id)
    
    def get_database_from_csv(self, file):
        with open("questions.csv", mode='r') as database_file:
            reader = csv.DictReader(database_file)
            for row in reader:
                question = Question(
                    id=int(row["id"]),
                    active=row["active"],
                    question=row["question"],
                    possible_choices=row["possible_choices"].split(';'),
                    correct_answer=row["correct_answer"],
                    stat_times_used=int(row["stat_times_used"]),
                    stat_correct_answ=int(row["stat_correct_answ"])
                )
                self.questions[question.id] = question

    def store_database_in_csv(self):
        with open("questions.csv", "w", newline='') as database_file:
            fieldnames = ["id", "active", "question",
                          "possible_choices", "correct_answer",
                          "stat_times_used", "stat_correct_answ"]
            writer = csv.DictWriter(database_file, fieldnames=fieldnames)
            writer.writeheader()
            for question in self.questions.values():
                writer.writerow({
                    "id": question.id,
                    "active": question.active,
                    "question": question.question,
                    "possible_choices": ';'.join(question.possible_choices),
                    "correct_answer": question.correct_answer,
                    "stat_times_used": question.stat_times_used,
                    "stat_correct_answ": question.stat_correct_answ
                })
            
    def Summary(self):
        for question in self.questions.values():
            question.question_stats()

    def list_of_ids(self):
        return self.questions.keys()
    

    

def get_possible_choices(no_of_choices=3):
    possible_choices = []
    for i in range(no_of_choices):
        while True:
            answer = input(f"\nPlease input a possible answer no. {i +1}: ")
            if answer:
                possible_choices.append(answer)
                break
    
    correct_answer = get_from_choices(possible_choices, no_of_choices)
    
    # while True:
    #     try:
    #         correct_answer = int(input("Which answer is correct? "))
    #         if correct_answer in range(1, (no_of_choices + 1)):
    #             correct_answer = possible_choices[correct_answer-1]
    #             break
    #         else:
    #             raise ValueError
    #     except ValueError | TypeError:
    #         print(f"Please provide an answer in range 1-{no_of_choices})")

    return possible_choices, correct_answer

def get_from_choices(data, no_of_choices):
    while True:
        try:
            users_answer = int(input("Your answer: ")) -1
            if users_answer in range(0, no_of_choices):
                users_answer = data[users_answer]
                break
            else:
                raise ValueError
        except ValueError or TypeError:
            print(f"Please provide an answer in range 1-{no_of_choices})")
    return users_answer

def get_free_form_choices():
    possible_choices = []
    correct_answer = get_data("Please input the correct answer? ")
    return possible_choices, correct_answer

def get_data(question):
    while True:
        answer = input(question)
        if answer:
            break
        else:
            print(f"Please provide a correct answer!")
    return answer

def displ_choices(possible_choices):
    for i, possible_answer in enumerate(possible_choices, 1):
                print(f"{i}. {possible_answer}")

if __name__=="__main__":
    
    database = Database_of_questions()
    database.add_question()
    # database.store_database_in_csv()
    database.add_question()
    print(database)