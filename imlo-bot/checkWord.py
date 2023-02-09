from uzwords import words
from difflib import get_close_matches

def checkWord(word, words=words):
    word = word.lower()
    matches = set(get_close_matches(word, words))
    available = False


    if word in matches:
        available = True
        matches = word
    elif 'к' in word:
        word = word.replace('к', 'қ')
        matches.update(get_close_matches(word, words))
    elif 'қ' in word:
        word = word.replace('қ', 'к')
        matches.update(get_close_matches(word, words))


    return {'available':available, 'matches':matches}



if __name__=='__main__':
    print(checkWord('сингмоқ'))
    print(checkWord('сингмок'))
    print(checkWord('синиш'))
    print(checkWord('синиқ-мертиқ'))
    print(checkWord('сингмо'))

