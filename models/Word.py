from models.BaseModel import BaseModel


class Word(BaseModel):
    tableName = 'words'
    uniqueKeys = ['word']

    fillables = [
        'word',
        'first_letter',
        'second_letter',
        'last_letter',
        'before_last_letter',
        'actual_length',
        'min_length',
        'max_length'
    ]

    def __init__(self):
        BaseModel.__init__(self)


Word = Word()
