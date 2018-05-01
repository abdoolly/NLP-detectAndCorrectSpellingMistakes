import inspect
from subprocess import call
import seeders.mainSeeder as seeder

# installing funcy
call(['pip', 'install', 'funcy'])

# installing nltk
call(['pip', 'install', 'nltk'])

print('Packages installed successfully')

"""
run commands to install the main pacakages that we are going to need
"""
allSeeders = inspect.getmembers(seeder, inspect.isfunction)
for key, func in allSeeders:
    func()

print("Packager finished successfully")
