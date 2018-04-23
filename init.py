from app.utils.FileManager import fileService
from models.Word import Word
from app.utils.generalUtils import generalUtils

# myList = fileService.getListFromFile('./data/words.txt')

# just making this line for testing
model = Word()

word = {
    'word': 'exampleWord',
    'first_letter': 'a',
    'second_letter': 'b',
    'last_letter': 'h',
    'before_last_letter': 'a',
    'actual_length': 8,
    'min_length': 5,
    'max_length': 11,
}

res = model.create(word)

print(res)
