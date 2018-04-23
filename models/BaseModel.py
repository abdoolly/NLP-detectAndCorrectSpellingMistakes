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
    fillables = []

    def __init__(self):
        self.initConnection()

    """
    initializing the connection variables in the class
    """

    def initConnection(self):
        self.cursor = conn.cursor()
        self.connection = conn

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
    function to create items in a table according to this model fillables 
    :param object is a dictionary 
    :return created object
    """

    def create(self, object):
        # make the query string
        query = 'INSERT INTO ' + \
                self.tableName + \
                generalUtils.listToStringBrackets(self.fillables) + \
                ' VALUES ' + \
                generalUtils.makeBracketsOf('?', len(self.fillables))

        # executing the query
        self.executeQuery(query, generalUtils.dicToTuple(object))

        # adding the auto generated id of the create row
        object['id'] = self.cursor.lastrowid

        # then returning the row after creation
        return object

    def select(self, object):
        self.isInstanceOfBaseModel()
        return
