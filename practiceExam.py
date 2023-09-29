import sys
import json
import random


def parse_json(filename):
    json_data = None
    try:
        with open(filename, 'r') as f:
            json_data = json.load(f)
    except FileNotFoundError as e:
        print(" (!) Couldn't locate the questions json file, make sure it is in the same directory as this script")
    return json_data


def get_question(question_id, question_l):
    question = None
    for arr in question_l:
        if arr['qid'] == question_id:
            question = arr
            break
    return question


def count_questions(questions):
    question_count = len(questions)
    return question_count


def select_random_question(question_count):
    selected_id = random.randint(1, question_count)
    return selected_id


def run_test(test_qs):
    answer_result = None
    user_questions_count = input("\nThere are currently " + str(
        len(test_qs)) + " questions in the database, how many questions would you like to run?\n")
    results_for_test = []
    custom_test_qs = []
    while int(user_questions_count) > len(test_qs):
        user_questions_count = input("\nThere are currently " + str(len(
            test_qs)) + " questions in the database, how many questions would you like to run? (Cannot exceed the total questions contained in the database)\n")
    for x in range(0, int(user_questions_count)):
        if test_qs[x] not in custom_test_qs:
            custom_test_qs.append(test_qs[x])
    if len(custom_test_qs) > 0:
        test_qs = custom_test_qs
    q_number = 0
    for q in test_qs:
        q_number += 1
        print("\nQuestion number: " + str(q_number) + " of " + str(len(test_qs)) + "\n")
        correct_answer_needed = None
        if q['qid']:
            print("\nQuestion ID (qid) is: " + str(q['qid']) + "\n")
        else:
            print("this question doesn't have a qid!!")
        print(q['question'])
        print("A./ " + (q['answers'][0]['text']))
        print("B./ " + (q['answers'][1]['text']))
        if len(q['answers']) > 2:
            print("C./ " + (q['answers'][2]['text']))
        if len(q['answers']) > 3:
            print("D./ " + (q['answers'][3]['text']))
        user_answer = input("\nPlease select an option\n")
        print("Selected answer: " + user_answer)
        if user_answer == "A" or user_answer == "a" or user_answer == "B" or user_answer == "b" or user_answer == "C" or user_answer == "c" or user_answer == "D" or user_answer == "d":
            # DO nothing
            None
        else:
            while user_answer != "A" or user_answer != "a" or user_answer != "B" or user_answer != "b" or user_answer != "C" or user_answer != "c" or user_answer != "D" or user_answer != "d":
                user_answer = input("\nPlease enter a valid choice\n")
                if user_answer == "A" or user_answer == "a" or user_answer == "B" or user_answer == "b" or user_answer == "C" or user_answer == "c" or user_answer == "D" or user_answer == "d":
                    break
            print("\nSelected answer: " + user_answer + "\n")
        answer_text = None
        for x in q['answers']:
            if x['correctAnswer'] == True:
                answer_text = x['text']
                if x['aid'] == 1:
                    correct_answer_needed = "A"
                elif x['aid'] == 2:
                    correct_answer_needed = "B"
                elif x['aid'] == 3:
                    correct_answer_needed = "C"
                elif x['aid'] == 4:
                    correct_answer_needed = "D"
        if user_answer == "A" or user_answer == "a":
            results_for_test.append(
                [q['question'], ['your_answer', user_answer], ['correct_answer', correct_answer_needed, answer_text],
                 q['qid']])
        elif user_answer == "B" or user_answer == "b":
            results_for_test.append(
                [q['question'], ['your_answer', user_answer], ['correct_answer', correct_answer_needed, answer_text],
                 q['qid']])
        elif user_answer == "C" or user_answer == "c":
            results_for_test.append(
                [q['question'], ['your_answer', user_answer], ['correct_answer', correct_answer_needed, answer_text],
                 q['qid']])
        elif user_answer == "D" or user_answer == "d":
            results_for_test.append(
                [q['question'], ['your_answer', user_answer], ['correct_answer', correct_answer_needed, answer_text],
                 q['qid']])

    return results_for_test


def get_statistics(res):
    total_questions_answered = len(res)
    correct_questions = 0
    incorrect_questions = 0
    for result in res:
        if result[1][1].lower() == result[2][1].lower():
            correct_questions += 1
        else:
            incorrect_questions += 1
    print("Total questions answered: " + str(total_questions_answered))
    print("Correct answers: " + str(correct_questions))
    print("Incorrect answers: " + str(incorrect_questions))
    print("Percentage: " + str(int(correct_questions / (total_questions_answered / 100))) + "%")
    passed = None
    if int(correct_questions / (total_questions_answered / 100)) > 60:
        print("Test completed, you passed! Well done!")
    else:
        print("Test completed, you failed! Keep on revising!")
    return int(correct_questions / (total_questions_answered / 100))


if __name__ == "__main__":
    print("CTM Practice Script")
    print("To add questions to the questions.json file, see the question_template.json file.")
    selected_questions = []
    test_questions = []
    results = []
    selected_q_id = None
    question_list = parse_json("questions.json")
    q_count = count_questions(question_list)
    for x in range(q_count):
        selected_q_id = select_random_question(q_count)
        if selected_q_id not in selected_questions:
            selected_questions.append(selected_q_id)
            x = x + 1
        else:
            while selected_q_id in selected_questions:
                selected_q_id = select_random_question(q_count)
            selected_questions.append(selected_q_id)
    prev_qids = []
    for x in (range(q_count)):
        random_qid = random.randint(1, q_count)
        while random_qid in prev_qids:
            random_qid = random.randint(1, q_count)
        else:
            prev_qids.append(random_qid)
            test_questions.append(get_question(random_qid, question_list))
    test_results = run_test(test_questions)
    if get_statistics(test_results) < 100:
        list_prev_questions = input("\nWould you like to view your incorrect questions? (y/n)\n")
        if list_prev_questions == "y":
            for record in test_results:
                if record[1][1].capitalize() != record[2][1].capitalize():
                    print("\n" + record[0])
                    print("You incorrectly answered: " + record[1][1].capitalize())
                    print("The correct answer was: " + record[2][1].capitalize() + " - " + record[2][2])
