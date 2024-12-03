from dataclasses import dataclass, field
from supp_functions import get_data

import random
import csv


@dataclass
class Question:
    """Question to be used in quiz"""

    id: int
    status: str
    question: str
    possible_choices: list
    correct_answer: str
    stat_times_used: int = 0
    stat_correct_answ: int = 0

    def ask_question(self, type="fix_position"):
        print(f"Question: {self.question}")
        if len(self.possible_choices) == 1:
            users_answer = get_data("Your answer: ")
        elif len(self.possible_choices) > 1:
            choices = self.possible_choices.copy()
            if type == "random_position":
                random.shuffle(choices)
            displ_choices(choices)
            users_answer = get_from_choices(choices, len(choices), "Your answer: ")
        self.stat_times_used += 1
        if users_answer.strip().lower() == self.correct_answer.lower():
            print("\nCorrect!\n")
            self.stat_correct_answ += 1
            return True
        else:
            print("Incorrect! Correct answer is: ", self.correct_answer, "\n")
            return False

    def set_status(self, value):
        self.status = value

    def show_question_stats(self):
        print("\n", ("=" * 10))
        print(f"Question ID: {self.id}")
        print(f"Question Status: {self.status}")
        print(f"Question: {self.question}\n")
        if len(self.possible_choices) == 1:
            print("Possible choices: None. Free form question")
        elif len(self.possible_choices) > 1:
            print("Possible choices:")
            displ_choices(self.possible_choices)
        print(f"\nCorrect answer: {self.correct_answer}")
        print("-" * 10)
        print(f"Question displayed: {self.stat_times_used}")
        try:
            correct_perc = self.stat_correct_answ * 100 / self.stat_times_used
        except ZeroDivisionError:
            correct_perc = "N/A - not yet used"
        print(f"Correctly answered [%]: {correct_perc} ")
        print("=" * 10)


@dataclass
class Database_of_questions:
    """Database of questions"""

    questions: dict[int, Question] = field(default_factory=dict)

    def add_question(self, id=0):
        print("\nQuestion creation:")
        try:
            if id == 0:
                id = max(self.list_of_ids()) + 1
        except ValueError:
            """if database of questions is empty"""
            id = 1
        status = "Enabled"
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
            status=status,
            question=the_question,
            possible_choices=possible_choices,
            correct_answer=correct_answer,
        )
        self.questions[question.id] = question

    def get_question(self, question_id: int):
        return self.questions.get(question_id)

    def get_database_from_csv(self, file="questions.csv"):
        with open(file, mode="r") as database_file:
            reader = csv.DictReader(database_file)
            for row in reader:
                question = Question(
                    id=int(row["id"]),
                    status=(row["status"]),
                    question=row["question"],
                    possible_choices=row["possible_choices"].split(";"),
                    correct_answer=row["correct_answer"],
                    stat_times_used=int(row["stat_times_used"]),
                    stat_correct_answ=int(row["stat_correct_answ"]),
                )
                self.questions[question.id] = question

    def store_database_in_csv(self,file="questions.csv"):
        try:
            with open(file, "w", newline="") as database_file:
                fieldnames = [
                    "id",
                    "status",
                    "question",
                    "possible_choices",
                    "correct_answer",
                    "stat_times_used",
                    "stat_correct_answ",
                ]
                writer = csv.DictWriter(database_file, fieldnames=fieldnames)
                writer.writeheader()
                for question in self.questions.values():
                    writer.writerow(
                        {
                            "id": question.id,
                            "status": question.status,
                            "question": question.question,
                            "possible_choices": ";".join(question.possible_choices),
                            "correct_answer": question.correct_answer,
                            "stat_times_used": question.stat_times_used,
                            "stat_correct_answ": question.stat_correct_answ,
                        }
                    )
        except Exception as e:
            print(f"Exception {e} occurred!")
        print("Database stored in file.\n")

    def summary(self):
        for question in self.questions.values():
            question.show_question_stats()

    def list_of_ids(self):
        return self.questions.keys()

    def get_weights_active_q(self):
        """Calculate weights for random.choices"""
        weights_active_q = []
        active_question = self.get_active_questions()
        for id in active_question:
            question = self.questions[id]
            weight = question.stat_correct_answ / self.get_total_time_correct()
            weights_active_q.append(weight)
        print(weights_active_q)
        return weights_active_q

    def get_total_time_correct(self):
        """Counts how many times where active question used"""
        total_time_correct = 0
        active_question = self.get_active_questions()
        for id in active_question:
            question = self.questions[id]
            total_time_correct += question.stat_correct_answ
        return total_time_correct

    def get_active_questions(self):
        active_questions = []
        for question in self.questions.values():
            if question.status == "Enabled":
                active_questions.append(question.id)
        return active_questions


def get_possible_choices():
    possible_choices = []
    while True:
        try:
            no_of_choices = int(input("How many possible answers (2 to 5)? "))
            if no_of_choices in range(2, 6):
                break
        except:
            continue
    for i in range(no_of_choices):
        while True:
            answer = input(f"\nPlease input a possible answer no. {i +1}: ")
            if answer:
                possible_choices.append(answer)
                break

    correct_answer = get_from_choices(
        possible_choices, no_of_choices, "The correct answer is:"
    )
    return possible_choices, correct_answer


def get_from_choices(data, no_of_choices, question):
    while True:
        try:
            users_answer = int(input(question)) - 1
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


def displ_choices(possible_choices):
    for i, possible_answer in enumerate(possible_choices, 1):
        print(f"{i}. {possible_answer}")
