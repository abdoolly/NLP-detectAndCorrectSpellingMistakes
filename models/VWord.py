from models.BaseModel import BaseModel


class VWord(BaseModel):
    tableName = 'vwords'
    uniqueKeys = ['word']

    fillables = [
        'word',
        'reverse'
    ]

    def __init__(self):
        BaseModel.__init__(self)


VWord = VWord()
