from nltk.metrics.distance import edit_distance


class Matcher:
    def __init__(self):
        pass

    @staticmethod
    def matchWord(word: str, wordsList: list, wordIndex=1):
        # this is an initialization of the current class so you can create other functions in the class and use it as
        #  you wish

        this = Matcher()

        """
        matching implementation should be done here
        """
        return this.getCorrectWord(word, wordsList, wordIndex)

    def getCorrectWord(self, word: str, wordsList: list, wordIndex=1):

        # if the wordsList was empty then just return the word as it is
        if len(wordsList) == 0:
            return word

        # array in which the index and the distance of the minimum distance will be kept
        minimumDistance = {
            'index': None,
            'distance': None
        }

        for index, correctWord in enumerate(wordsList):
            distance = edit_distance(word, correctWord[wordIndex], substitution_cost=2)

            # if this was not the first time and the distance inside the dict was bigger than the distance that
            # was just calculated
            if minimumDistance['index'] is not None and distance < minimumDistance['distance']:
                minimumDistance['index'] = index
                minimumDistance['distance'] = distance

            # if this was the first time then just put the first index and distance inside
            if minimumDistance['index'] is None:
                minimumDistance['index'] = index
                minimumDistance['distance'] = distance

        if minimumDistance['distance'] > 10:
            return word

        return wordsList[minimumDistance['index']][wordIndex]
