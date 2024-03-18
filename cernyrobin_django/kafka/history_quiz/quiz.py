import json
import os
import random
import similarity

NUM_QUESTIONS = 25
SIMILARITY_THRESHOLD = 0.26

courses_file = open(os.path.join(os.path.dirname(__file__), 'courses.json'), 'r')
courses = json.load(courses_file)

def get_courses(id=None):
    if id != None:
        for course, data in courses.items():
            if data.get("id", "0"):
                return course
    else:
        all_courses = {}

        for course, data in courses.items():
            all_courses[course] = data.get("id", "0")

        return all_courses

def get_questions(id):
    for course, data in courses.items():
        if data.get("id", "0"):
            return data.get("Questions", {})

def get_qa_pair(course):
    question_answer_pairs = courses[course]["Questions"]

    question, answer = random.choice(list(question_answer_pairs.items()))

    return question, answer

def get_similarity(course, question, answer):
    correct_answer = courses[course]["Questions"][question]

    return similarity.compare(correct_answer, answer)

def main(course):
    questions = []
    answers = []

    for i in range(NUM_QUESTIONS):
        question, answer = get_qa_pair(course)
        questions.append(question)
        answers.append(answer)

    for i in range(NUM_QUESTIONS):
        print(questions[i])
        answer = input("Answer: ")
        similarity = get_similarity(course, questions[i], answer)

        if similarity > SIMILARITY_THRESHOLD:
            print("Correct!")
        else:
            print("Incorrect!")

        print("similarity:", similarity * 100, "%")

if __name__ == "__main__":
    main("Úvod do výuky dějepisu")