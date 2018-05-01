from app.utils.FileManager import fileService
from models.VWord import VWord

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
    creationList = []
    smallList = []
    for index, word in enumerate(wordsList):
        smallList.append({
            "word": str(word),
            'reverse': word[::-1]
        })

        if len(word) > 3:
            creationList.append({
                "word": str(word).lower(),
                "first_letter": str(word[0]).lower(),
                "second_letter": str(word[1]).lower(),
                'last_letter': str(word[len(word) - 1]).lower(),
                "before_last_letter": str(word[len(word) - 2]).lower(),
                "actual_length": len(word),
                "min_length": (len(word) - 3),
                "max_length": (len(word) + 3)
            })

        if len(word) <= 3:
            creationList.append({
                "word": str(word).lower(),
                "first_letter": str(word[0]).lower(),
                "second_letter": None,
                'last_letter': None,
                "before_last_letter": None,
                "actual_length": len(word),
                "min_length": len(word),
                "max_length": len(word)
            })

    Word.createBulk(creationList)
    VWord.createBulk(smallList)

    VWord.executeQuery('INSERT INTO vwords(vwords) VALUES(?)', ('optimize',))

    print('Word Seeder finished successfully')
