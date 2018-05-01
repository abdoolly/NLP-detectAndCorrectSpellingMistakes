from models.BaseModel import BaseModel

"""

the words table

what the seeder does

word | first_letter | second_letter | last_letter | before_last_letter | actual_length | length_min | length_max 

word : the word we will search for
first_letter : first letter in the word
second_letter : second letter in the word
last_letter : last_letter in the word
before_last_letter : the letter before the last letter in the word
actual_length : the actual length of the word
length_min : minimum length for the word which will be the actual length -3
length_max : maximum length for the word which will be the actual length +3

"""


# use the base model here to create main database tables that we are going to need in our application
def createTableWords():
    baseModel = BaseModel()
    baseModel.executeQuery(
        '''
            CREATE TABLE IF NOT EXISTS words  
            (
                id INTEGER PRIMARY KEY,
                word VARCHAR(255) ,
                first_letter CHARACTER(1),
                second_letter CHARACTER(1),
                last_letter CHARACTER(1),
                before_last_letter CHARACTER(1),
                actual_length INTEGER,
                min_length INTEGER,
                max_length INTEGER,
                CONSTRAINT unique_word_constraint UNIQUE (word)
            )
            
        ''')

    # making the full text search table
    baseModel.executeQuery(
        '''
           CREATE VIRTUAL TABLE IF NOT EXISTS vwords
           USING FTS5(
             word,
             reverse
           );
        '''
    )
