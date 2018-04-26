from app.utils.FileManager import fileService

from models.Word import Word

"""

the words table

what the seeder does

word | first_letter | second_letter | last_letter | before_last_letter | actual_length | length_min | length_max 

word : the word we will search for
first_letter : first letter in the word
second_letter : second letter in the word
last_letter : last_letter in the word
before_last_letter : the letter before the last letter in the word
actual_length : the actual length of the word
min_length : minimum length for the word which will be the actual length -3
max_length : maximum length for the word which will be the actual length +3

"""

"""

seeding the main words table

"""


def seedOurWordsCorpora():
    wordsList = fileService.getListFromFile('./data/words.txt')
    for word in wordsList:
        Word.create({
            "word": word,
            "first_letter": word[0],
            "second_letter": word[1],
            "before_last_letter": word[len(word) - 2],
            "actual_length": len(word),
            "min_length": len(word) - 3,
            "max_length": len(word) + 3
        })
