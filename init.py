from app.core.spellcheckers.fullTextSearchSpellChecker import fullTextSearchSpellChecker
from app.core.spellcheckers.normalDBSpellChecker import normalDBSpellChecker
from app.desktopInterface.DesktopInitializer import DesktopInitializer
from app.utils.FileManager import fileService
from models.VWord import VWord
from models.Word import Word
from app.utils.generalUtils import generalUtils
import re

# from funcy import map

# choose the way you want to treat the application

print('press 1 for desktop')
print('press 2 for command line')
userInput = int(input())

if userInput == 1:
    desktop = DesktopInitializer()

if userInput == 2:
    print('please enter full file path which you want to make spell checking for')
    filePath = str(input())
    text = fileService.getFileData(filePath)
    print('processing please wait...')
    resultText = fullTextSearchSpellChecker.spellCheckDocument(text)
    print(resultText)
    path = fileService.putDataInFile('outputs/spellChecked.txt', resultText)
    print('result file path : ', path)