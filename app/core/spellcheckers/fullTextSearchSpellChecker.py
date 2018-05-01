from typing import Union

from app.core.Matcher import Matcher
from app.utils.generalUtils import generalUtils
from funcy import compose

# noinspection PyMethodMayBeStatic
from models.VWord import VWord
from models.Word import Word
from app.core.spellcheckers.normalDBSpellChecker import normalDBSpellChecker


class fullTextSearchSpellChecker(normalDBSpellChecker):
    wordIndex = 0

    def selectWordMatchers(self, word: str):
        fixedWord = generalUtils.cleanWord(word)

        if not fixedWord:
            return word, None

        word = fixedWord

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
            firstTwo = word[:2] + '*'
            lastThree = word[(len(word) - 3):] + '*'
            VWord.executeQuery('select * from vwords where vwords MATCH ?', (firstTwo,))

        if len(word) <= 3:
            VWord.executeQuery(
                '''
                   select * from words where first_letter = ? and actual_length between 2 and 4 
                ''',
                (word[0])
            )

        result = VWord.cursor.fetchall()
        return word, result
