import datetime


def get_confirmation(question=""):
    print(question)
    while True:
        confirmation = input("Continue? Y/ N ").lower()
        if confirmation == "y":
            print("Confirmed")
            return True
        elif confirmation == "n":
            print("Cancelled")
            return False
        else:
            print("Please answer Y/ N")


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
            print("Please provide valid number (float or int).")


def get_test_results(test_stat_correct, test_run_total):
    test_correct_perc = test_stat_correct * 100 / test_run_total
    now = datetime.datetime.today()
    test_report = [
        "=================",
        f"Test results from testting on: {now}",
        f"Correct anwers: {test_stat_correct}",
        f"from {test_run_total} questions",
        f"% of correct answers: {test_correct_perc:.2f}",
        "=================",
        "\n",
    ]
    return test_report


def save_print(test_results, save=True):
    try:
        with open("results.txt", "a") as file:
            for line in test_results:
                print(line)
                if save == True:
                    file.write(f"{line}\n")

    except Exception as e:
        print(f"Results were not saved. Error: {e}")
