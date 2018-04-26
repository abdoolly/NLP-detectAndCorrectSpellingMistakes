from app.utils.FileManager import fileService
from models.Word import Word
from app.utils.generalUtils import generalUtils


# those things underneath this line are just for testing but, in the future
# this page will actually start our app

# myList = fileService.getListFromFile('./data/words.txt')

# just making this line for testing

# word = {
#     'word': 'exampleWord',
#     'first_letter': 'a',
#     'second_letter': 'b',
#     'last_letter': 'h',
#     'before_last_letter': 'a',
#     'actual_length': 8,
#     'min_length': 5,
#     'max_length': 11,
# }
#
# res = Word.createIfNotExist(word)

mylist = ['a', 'b', 'c']
mydict = {
    "a": 'asdasd',
    'asasd': 'asdasdasd'
}

res = generalUtils.findKeyInDictionary(mylist, mydict)

print(res)
