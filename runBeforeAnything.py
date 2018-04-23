from subprocess import call
import seeders.mainSeeder as seeder

"""
run commands to install the main pacakages that we are going to need
"""

# installing funcy
call(['pip', 'install', 'funcy'])

# run table creation seeder
seeder.createTableWords()

print("packages and tables have been installed and created successfully")
