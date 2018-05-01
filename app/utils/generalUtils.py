from typing import Union

from funcy import compose
import re


class generalUtils:
    """
     convert [name,address] -> '(name,address)'
    """

    @staticmethod
    def listToStringBrackets(theList):
        result = '('
        for index in range(0, len(theList)):

            if index == len(theList) - 1:
                result += str(theList[index]) + ')'
                break

            result += str(theList[index]) + ','

        return result

    """
    make a list of something 
    ex : something = '?' length = 3
    output = ['?','?','?']
    """

    @staticmethod
    def makeListOf(something, length):
        resultList = []
        for i in range(0, length):
            resultList.append(str(something))

        return resultList

    """
    using the above functions it makes a list and convert it to brackets
    """

    @staticmethod
    def makeBracketsOf(something, length):
        return compose(generalUtils.listToStringBrackets, generalUtils.makeListOf)(something, length)

    """
    convert dictionary to tuple
    {word:'exmaple' , word2 : 'example2'} -> ('example','example2')
    """

    @staticmethod
    def dicToTuple(dictionary):
        return tuple(dictionary.values())

    """
    search if any key in a list exist in a dictionary and return the first one it find 
    """

    @staticmethod
    def findKeyInDictionary(array: list, modelObject: dict) -> Union[bool, str]:
        for key in array:
            if key in modelObject:
                return key

        return False

    @staticmethod
    def symbolsRemover(word: str):
        return re.sub('[^A-Za-z0-9]+', '', word)

    @classmethod
    def cleanWord(cls, word: str):
        word = word.strip()
        word = cls.symbolsRemover(word)
        return word
