import pytest
from classes import Question, Database_of_questions
from supp_functions import get_confirmation, get_data, get_test_results, save_print


import random



# Test Question class
def test_question_creation():
    question = Question(
        id=1,
        status="Enabled",
        question="What is the capital of France?",
        possible_choices=["Paris", "London", "Berlin", "Rome"],
        correct_answer="Paris"
    )
    assert question.id == 1
    assert question.status is "Enabled"
    assert question.question == "What is the capital of France?"
    assert question.possible_choices == ["Paris", "London", "Berlin", "Rome"]
    assert question.correct_answer == "Paris"
    assert question.stat_times_used == 0
    assert question.stat_correct_answ == 0

def test_question_ask_question(monkeypatch):
    question = Question(
        id=1,
        status="Enabled",
        question="What is 2 + 2?",
        possible_choices=["3", "4", "5", "6"],
        correct_answer="4"
    )

    # Mock user input for the correct answer
    monkeypatch.setattr('builtins.input', lambda _: 2)
    assert question.ask_question(type="fix_possition") is True
    assert question.stat_correct_answ == 1
    assert question.stat_times_used == 1

    # Mock user input for the incorrect answer
    monkeypatch.setattr('builtins.input', lambda _: "3")
    assert question.ask_question(type="fix_possition") is False
    assert question.stat_correct_answ == 1
    assert question.stat_times_used == 2


# Test Database_of_questions class
def test_add_question():
    db = Database_of_questions()
    db.questions[1] = Question(
        id=1,
        status="Enabled",
        question="What is the largest planet?",
        possible_choices=["Earth", "Jupiter", "Mars"],
        correct_answer="Jupiter"
    )
    assert 1 in db.questions
    question = db.questions[1]
    assert question.question == "What is the largest planet?"
    assert question.correct_answer == "Jupiter"


def test_active_questions():
    db = Database_of_questions()
    db.questions[1] = Question(
        id=1,
        question="What is the largest desert?",
        possible_choices=["Sahara", "Arctic", "Antarctic"],
        correct_answer="Antarctic",
        status="Enabled"
    )

    db.questions[2] = Question(
        id=2,
        question="What is the longest river?",
        possible_choices=["Nile", "Amazon", "Yangtze"],
        correct_answer="Nile",
        status="Disabled"
    )
    active_questions = db.get_active_questions()
    assert 1 in active_questions
    assert 2 not in active_questions

def test_store_and_load_questions(tmpdir):
    db = Database_of_questions()
    db.questions[1] = Question(
        id=1,
        status="Enabled",
        question="What is the smallest country?",
        possible_choices=["Vatican City", "Monaco", "Nauru"],
        correct_answer="Vatican City"
    )
    
    # Save questions to a temporary file
    temp_file = tmpdir.join("questions.csv")
    db.store_database_in_csv(temp_file)

    # Load questions from the temporary file
    new_db = Database_of_questions()
    new_db.get_database_from_csv(temp_file)

    assert 1 in new_db.questions
    question = new_db.questions[1]
    assert question.question == "What is the smallest country?"
    assert question.correct_answer == "Vatican City"

def test_get_confirmation_yes(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "y")
    assert get_confirmation("Continue?") is True

def test_get_confirmation_no(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "n")
    assert get_confirmation("Continue?") is False

def test_get_data_str(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "test")
    assert get_data("Enter data: ") == "test"

def test_get_data_int(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "42")
    assert get_data("Enter number: ", type="int") == 42

# Test get_test_results
def test_get_test_results():
    report = get_test_results(8, 10)
    assert "Correct anwers: 8" in report
    assert "% of correct answers: 80.00" in report