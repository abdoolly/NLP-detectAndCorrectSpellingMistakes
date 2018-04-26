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

    def executeQuery(self, query, data=None, debug=False):
        if debug:
            return compose(self._commitChanges, self._debug, self._doQuery)(query, data)

        if not debug:
            return compose(self._commitChanges, self._doQuery)(query, data)

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

    def _commitChanges(self, options):
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

    def createIfNotExist(self, modelObject: dict):
        query = 'INSERT OR IGNORE INTO ' + \
                self.tableName + \
                generalUtils.listToStringBrackets(self.fillables) + \
                ' VALUES ' + \
                generalUtils.makeBracketsOf('?', len(self.fillables))

        self.executeQuery(query, generalUtils.dicToTuple(modelObject))

        uniqueKey = self._getUniqueKeyInModelObject(modelObject)

        if uniqueKey:
            return self.select({
                uniqueKey: modelObject[uniqueKey]
            })

        return modelObject

    # not completed yet
    def select(self, modelObject: dict, options: dict = None):
        selectorsList = []
        dictKeys = modelObject.keys()

        for item in dictKeys:
            if item in self._fastAccessFillable:
                selectorsList.append(item)


        # return
