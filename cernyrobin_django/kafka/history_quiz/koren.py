import pymorphy2
from nltk.stem.snowball import CzechStemmer

def ziskej_koren_slova(slovo):
    stemmer = CzechStemmer()
    koren_slova = stemmer.stem(slovo)
    return koren_slova

    # morph = pymorphy2.MorphAnalyzer(lang='cs')
    # lemmatizovane_slovo = morph.parse(slovo)[0].normal_form
    # return lemmatizovane_slovo

# Příklad použití
slovo = "programátor"
koren_slova = ziskej_koren_slova(slovo)

print(f"Původní slovo: {slovo}")
print(f"Kořen slova: {koren_slova}")