from api.paraphraser import scrape
import re

def concatenate_strings(strings):
    concatenated_strings = []
    counter = 0

    for i, string in enumerate(strings):
        if counter < 4:
            last_str = concatenated_strings[-1] if len(concatenated_strings) > 0 else ""
            if len(concatenated_strings) > 0:
                concatenated_strings[-1] = last_str + string
            else:
                concatenated_strings.append(string)
            counter += 1
        else:
            concatenated_strings.append(string)
            counter = 0

    return concatenated_strings

def get_paraphrase(text):
    answers = re.findall(r'(?:\A|\n)\d+\. [^\n]+', text)
    paraphrased_answers = []

    for answer in concatenate_strings(answers):
        if answer:
            result = scrape.open_webpage_and_input_text(answer)

            if result["success"]:
                paraphrased_answers.append(result["result"])
            else:
                paraphrased_answers.append(answer)

    paraphrased_answers_str = "\n".join(paraphrased_answers)

    return paraphrased_answers_str