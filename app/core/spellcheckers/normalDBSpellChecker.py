from typing import Union

from app.core.Matcher import Matcher
from app.utils.generalUtils import generalUtils
from funcy import compose

# noinspection PyMethodMayBeStatic
from models.Word import Word


class normalDBSpellChecker:
    # a dictionary that will hold the wrong words and their correction everytime they are corrected
    # so we do not need to re correct them another time it's like a cache
    WrongWords: dict = {}

    wordIndex = 1

    def __init__(self):
        # this is an array in which the new document after correction will be put in
        self.correctedTextList = []

    def debug(self, x):
        print(x)
        return x

    @classmethod
    def spellCheckDocument(cls, text: str) -> str:
        this = cls()
        """
        - document to list of words -- checked
        - loop on words select their matchers from db 
        - if found then go to next word if not then do the following
        - send word and matchers list to spell check matcher 
        - replace word in list after correction
        - then go to the next word 
        - at the end join list with space
        - return the new corrected text
        - and return the array of mistaken words and their corrections
        """
        # textList = this.textToList(text)

        # compose function run the functions give inside it from right to left
        applierFunc = compose(
            lambda textList: [this.correctWord(word) for word in textList],  # one line function to run on each word
            this.textToList
        )

        # correct the words
        applierFunc(text)

        return this.listToDocument(this.correctedTextList)

    def textToList(self, text: str):
        textList = text.split(' ')

        for index, word in enumerate(textList):
            splitted = word.split('\n')
            if len(splitted) > 1:
                textList[index] = splitted[0]

                counter = 1

                # putting the splitted word inside the array
                for index_2, splW in enumerate(splitted):
                    if splW and index_2:
                        textList.insert(index + counter, splW)
                        counter = counter + 1
        return textList

    def correctWord(self, word):
        return compose(self.getCorrectWord, self.selectWordMatchers)(word)

    def selectWordMatchers(self, word: str):
        # converting word to lower case
        word = str(word).lower()
        word = generalUtils.cleanWord(word)

        # seeing if word exist in the dataset
        found = Word.where('word', value=word).first()

        # if the word was found then just return it as it is
        if found:
            return word, None

        checkResult = self.checkAndSaveInWrongWords(word)

        # this word was found wrong before and already corrected
        if checkResult is not None:
            return checkResult, None

        if len(word) > 3:
            first_letter = word[0]
            second_letter = word[1]
            last_letter = word[len(word) - 1]
            before_last = word[len(word) - 2]
            min_length = (len(word) - 3)
            max_length = (len(word) + 3)

            Word.executeQuery(
                '''
                select * from words where 
                (first_letter = ? and second_letter = ?) or
                 (last_letter = ? and before_last_letter = ?) 
                ''',
                (first_letter, second_letter, last_letter, before_last))

        if len(word) <= 3:
            first_letter = word[0]
            min_length = 1
            max_length = (len(word) + 3)

            Word.executeQuery(
                '''
                select * from words where 
                first_letter = ?
                and
                (actual_length between ? and ?)
                ''',
                (first_letter, min_length, max_length))

        return word, Word.cursor.fetchall()

    def getCorrectWord(self, wordAndList: tuple):
        word, wordList = wordAndList

        if wordList is None:
            self.correctedTextList.append(word)
            return word

        # call the matcher here
        correctWord = Matcher.matchWord(word, wordList, self.wordIndex)

        # save the word in the wrong words dictionary to get correction faster next time
        self.WrongWords[word]['correction'] = correctWord

        # append corrected word to the correctedTextList
        self.correctedTextList.append(correctWord)

        return correctWord

    def checkAndSaveInWrongWords(self, word):
        # check if word was wrong and saved before
        if word in self.WrongWords:
            self.WrongWords[word]['count'] += 1
            return self.WrongWords[word]['correction']

        self.WrongWords[word] = {
            'count': 1
        }

        return None

    def listToDocument(self, wordsList: list):
        return ' '.join(wordsList)
