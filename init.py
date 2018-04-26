from app.desktopInterface.DesktopInitializer import DesktopInitializer
from app.utils.FileManager import fileService
from models.Word import Word
from app.utils.generalUtils import generalUtils

# choose the way you want to treat the application

print('press 1 for desktop')
print('press 2 for command line')
userInput = int(input())

if userInput == 1:
    desktop = DesktopInitializer()

if userInput == 2:
    print('please enter file path which you want to make spell checking for')
