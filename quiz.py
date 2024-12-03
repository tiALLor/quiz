from classes import Question, Database_of_questions
from supp_functions import get_confirmation, get_test_results, save_print, get_data
import random
import sys


def primary_screen():
    while True:
        print(
            """
            -------------------------------------------
            Please choose what you would like to do:
            -------------------------------------------
            1. Add a question
            2. Question statistics / Show questions in database
            3. Activate or disable a question from testing
            4. Practice
            5. Testing
            6. Change a question
            7. End
            -------------------------------------------
            """
        )
        mode = input("Please make a choose! ")
        if mode == "1":
            database.add_question()
            database.store_database_in_csv()
            print("Question was successfully added.\n")
        elif mode == "2":
            database.summary()
        elif mode == "3":
            question_deactivation()
        elif mode == "4":
            if can_be_run() == True:
                mode_practice()
        elif mode == "5":
            if can_be_run() == True:
                mode_testing()
        elif mode == "6":
            change_question()
            database.store_database_in_csv()
            print("Question was successfully added.\n")
        elif mode == "7":
            print("Bye.")
            sys.exit()
        else:
            print("Please make a valid choice.")
    return


def question_deactivation():
    database.summary()
    print(
        """
          Please provide ID for question,
          which should be Enabled/ Disabled,
          from use in tests and practice mode.
          """
    )
    while True:
        question_id = input("ID /'None' for leave: ").lower()
        try:
            if question_id == "none":
                return
            elif int(question_id) not in database.list_of_ids():
                raise ValueError("ID is not valid")
        except Exception as e:
            print(f"Error {e} occurred")
        question = database.questions[int(question_id)]
        question.show_question_stats()
        if get_confirmation("You are to change the question status.") == True:
            if question.status == "Disabled":
                question.set_status("Enabled")
                print("Question was Enabled")
            elif question.status == "Enabled":
                question.set_status("Disabled")
                print("Question was Disabled")
        else:
            print("A problem occurred")
            return
        question.show_question_stats()
        database.store_database_in_csv()
        return


def mode_practice():
    print("Testing mode initialized!\n")
    active_questions = database.get_active_questions()
    test_stat_correct = 0
    test_run_total = 0
    while True:
        weights = database.get_weights_active_q()
        test_question_ids = random.choices(active_questions, weights=weights, k=1)
        for id in test_question_ids:
            question = database.questions[id]
            answ_is_correct = question.ask_question(type="random_position")
            if answ_is_correct == True:
                test_stat_correct += 1
            test_run_total += 1
        database.store_database_in_csv()
        if get_confirmation() == False:
            break
    test_results = get_test_results(test_stat_correct, test_run_total)
    save_print(test_results, save=False)


def mode_testing():
    print("Testing mode initialized!\n")
    active_questions = database.get_active_questions()
    while True:
        numb_of_questions = get_data("How many question shall be in test? ", "int")
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
    test_run_total = 0
    for id in test_question_ids:
        question = database.questions[id]
        answ_is_correct = question.ask_question(type="random_position")
        if answ_is_correct == True:
            test_stat_correct += 1
        test_run_total += 1
    database.store_database_in_csv()
    test_results = get_test_results(test_stat_correct, test_run_total)
    save_print(test_results, save=True)


def change_question():
    id_to_change = get_data("Question ID to be changed: ", "int")
    if id_to_change not in database.list_of_ids():
        raise ValueError("ID is not valid")
        return
    database.add_question(id_to_change)
    database.store_database_in_csv()
    return


def can_be_run():
    active_questions = database.get_active_questions()
    if len(database.list_of_ids()) < 5 or len(active_questions) < 3:
        print(
            """
        Minimal 5 questions in database (from which are at least 3 active) 
        are required to run a practice or test mode.
              """
        )
        return False
    else:
        return True


if __name__ == "__main__":

    database = Database_of_questions()
    try:
        database.get_database_from_csv()
        print("Database from file was loaded")
    except Exception as e:
        print("Database from file could't be loaded")
        print(f"Exception: {e} occurred!")
        print("You can continue and create new database!")
    primary_screen()
