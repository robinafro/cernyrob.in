from . import scrape
import re

def get_paraphrase(text):
    answers = re.split(r'\d+\. [^\n]+', text)
    paraphrased_answers = []

    for answer in answers:
        if answer:
            result = scrape.open_webpage_and_input_text(answer)

            if result["success"]:
                paraphrased_answers.append(result["result"])
            else:
                paraphrased_answers.append(answer)

    paraphrased_answers_str = "\n".join(paraphrased_answers)

    return paraphrased_answers_str