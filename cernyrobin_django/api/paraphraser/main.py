from api.paraphraser import scrape
import re

def concatenate_strings(strings):
    concatenated_strings = []
    counter = 0

    for i, string in enumerate(strings):
        if counter < 6:
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
    answers = re.findall(r"(?:\A|\n)\d+\. [^\n]+", text.strip())
    
    paraphrased_answers = []

    for answer in answers:
        if answer:
            num = answer.split(".")[0]
            answer = "".join(answer.split(".")[1:]).strip()

            result = scrape.send_request(answer)

            try:
                paraphrased_answers.append(num + ". " + result["output"]["standard"]["text"])
            except Exception as e:
                paraphrased_answers.append(num + ". " + e)

    paraphrased_answers_str = "\n".join(paraphrased_answers)
    
    return paraphrased_answers_str