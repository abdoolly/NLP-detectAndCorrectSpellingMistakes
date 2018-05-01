from typing import Union

from config.connection import connection as conn
from funcy import compose
from app.utils.generalUtils import generalUtils

"""
Base models class which all models will extend it to make creations easily
"""


class BaseModel:
    # this is the main connection
    connection = None

    # this is the cursor object of the sqlite
    cursor = None

    tableName = ''
    fillables: str = []
    _fastAccessFillable: str = []
    uniqueKeys = []

    _whereObject = {}

    def __init__(self):
        self.initConnection()
        self.uniqueKeys = self.setUniqueKeysArray()
        self._fastAccessFillable = dict(zip(self.fillables, self.fillables))

    """
    initializing the connection variables in the class
    """

    def initConnection(self):
        self.cursor = conn.cursor()
        self.connection = conn

    def setUniqueKeysArray(self):
        self.uniqueKeys.append('id')
        return self.uniqueKeys

    """
    execute the query using composition between the doQuery and the commit function
    """

    def executeQuery(self, query, data=None, debug=False, commit=True):

        basicCompose = compose(self._doQuery)

        if debug:
            basicCompose = compose(self._debug, basicCompose)

        if commit:
            basicCompose = compose(self.commitChanges, basicCompose)

        return basicCompose(query, data)

    """
    function to execute a query
    """

    def _doQuery(self, query, data):
        if data is None:
            self.cursor.execute(query)
            return query

        self.cursor.execute(query, data)
        return query

    """
    function to work when debug flag is True
    """

    def _debug(self, text):
        print(text)

    """
    commit changes in sqlite
    """

    def commitChanges(self, options):
        self.connection.commit()

    """
    check if the current instance is an instance of basemodel or not
    """

    def isInstanceOfBaseModel(self):
        if isinstance(self, BaseModel):
            raise Exception('Please do not use BaseModel class to make any database operations')

    """
    get the unique key if exist in the model by comparing both the unique keys array and the modelObject given
    :return string | False
    """

    def _getUniqueKeyInModelObject(self, modelObject: dict) -> str:
        return generalUtils.findKeyInDictionary(self.uniqueKeys, modelObject)

    """
    function to create items in a table according to this model fillables 
    :param object is a dictionary 
    :return created object
    """

    def create(self, modelObject):
        # make the query string
        query = 'INSERT INTO ' + \
                self.tableName + \
                generalUtils.listToStringBrackets(self.fillables) + \
                ' VALUES ' + \
                generalUtils.makeBracketsOf('?', len(self.fillables))

        # executing the query
        self.executeQuery(query, generalUtils.dicToTuple(modelObject))

        # adding the auto generated id of the create row
        modelObject['id'] = self.cursor.lastrowid

        # then returning the row after creation
        return modelObject

    def createIfNotExist(self, modelObject: dict, options=None):
        query = 'INSERT OR IGNORE INTO ' + \
                self.tableName + \
                generalUtils.listToStringBrackets(self.fillables) + \
                ' VALUES ' + \
                generalUtils.makeBracketsOf('?', len(self.fillables))

        self.executeQuery(query, generalUtils.dicToTuple(modelObject))

        uniqueKey = self._getUniqueKeyInModelObject(modelObject)

        if uniqueKey:
            return self.findOne({
                uniqueKey: modelObject[uniqueKey]
            })

        return modelObject

    def createBulk(self, modelObjects: list, options=None):
        for modelObject in modelObjects:
            query = 'INSERT OR IGNORE INTO ' + \
                    self.tableName + \
                    generalUtils.listToStringBrackets(self.fillables) + \
                    ' VALUES ' + \
                    generalUtils.makeBracketsOf('?', len(self.fillables))

            self.executeQuery(query, generalUtils.dicToTuple(modelObject), commit=False)

        self.commitChanges(options)

    def where(self, column: str, operator='=', value=None):
        if not value:
            raise Exception('Invalid value given')
        # adding the new value in the whereObject
        self._whereObject[column] = {'value': value, 'operator': operator}

        return self

    def get(self):
        result = self.findAll(self._whereObject)
        self._whereObject = {}
        return result

    def first(self):
        result = self.findOne(self._whereObject)
        self._whereObject = {}
        return result

    def _makeSelectQuery(self, modelObject: dict):
        query = 'SELECT * from ' + \
                self.tableName + \
                ' WHERE '

        selectorsString = ''
        dictKeys = list(modelObject.keys())

        for index in range(0, len(dictKeys)):

            key = dictKeys[index]
            modelObjectValue = modelObject[key]

            if dictKeys[index] not in self._fastAccessFillable:
                continue

            suffix = ''

            if index != (len(dictKeys) - 1):
                suffix = ' AND '

            if index == (len(dictKeys) - 1):
                suffix = ''

            if 'operator' in modelObject[key]:
                selectorsString += key + ' ' + modelObjectValue['operator'] + ' ? ' + suffix
                modelObject[key] = modelObjectValue['value']
                continue

            if 'operator' not in modelObject[key]:
                selectorsString += key + ' = ' + ' ' + '? ' + suffix
                continue

        query += selectorsString

        # converting the selection object to tuple for querying
        myValueTuple = generalUtils.dicToTuple(modelObject)

        # executing the query
        self.executeQuery(query, myValueTuple)

    # not completed yet
    def findOne(self, modelObject: dict, options: dict = None) -> Union[dict, None]:
        # making the select query and execute it
        self._makeSelectQuery(modelObject)

        # getting the selection result values
        values = self.cursor.fetchone()

        if not values:
            return None

        # converting result from tuple to a proper dictionary
        return self._valueToObject(self.cursor, values)

    def findAll(self, modelObject: dict, options: dict = None) -> list:
        # making the select query and execute it
        self._makeSelectQuery(modelObject)

        # getting the selection result values
        values = self.cursor.fetchall()

        resultList = []
        # for value in values:
        for value in values:
            # converting each value to an object
            objectDict = self._valueToObject(self.cursor, value)

            # appending in the list
            resultList.append(objectDict)

        # converting result from tuple to a proper dictionary
        return resultList

    def _valueToObject(self, cursor, data) -> dict:
        Object = {}
        for idx, col in enumerate(cursor.description):
            Object[col[0]] = data[idx]
        return Object
