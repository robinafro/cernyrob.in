from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from collections import Counter
import math
from kafka.history_quiz import czech_stemmer

def preprocess(text):
    # Tokenize the text
    tokens = word_tokenize(text, language='czech')
    # Remove punctuation and convert to lowercase
    tokens = [token.lower() for token in tokens if token.isalnum()]
    # Remove stopwords
    stop_words = set(stopwords.words("czech"))
    tokens = [token for token in tokens if token not in stop_words]
    # Stemming (optional)
    tokens = czech_stemmer.stem(" ".join(tokens)).split(" ")

    for token in tokens:
        if token == "":
            tokens.remove(token)
    
    
    # stemmer = SnowballStemmer("czech")
    # tokens = [stemmer.stem(token) for token in tokens]
    return tokens

def cosine_similarity(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    # sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    sum2 = sum1
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
    words = preprocess(text)
    return Counter(words)

def compare(text1="", text2=""):
    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)

    similarity = cosine_similarity(vector1, vector2)
    
    return similarity

if __name__ == "__main__":
    text1 = "The second world war was bad"
    text2 = "it was very bad"

    print(compare(text1, text2))
