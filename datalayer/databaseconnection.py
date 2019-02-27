import sqlite3
import logging
from datalayer import query_config as qc

logger = logging.getLogger(__name__)

class databaseConnection(object):
    """
    Class to create connection to the sqlite database
    """
    _instance = None
    def __new__(cls):
        """
        function to initialize the database connection
        :return: returns singleton instance of the class
        """
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            try:
                logger.info('Connecting to database.')
                databaseConnection._instance.connection = sqlite3.connect("database.freshdesk")
                databaseConnection._instance.cursor = databaseConnection._instance.connection.cursor()

            except Exception as e:
                logger.error('Connection not established {}'.format(e))
                databaseConnection._instance = None
                raise
            else:
                logger.info('connection established')
                databaseConnection._instance.connection.executescript(qc.create_table)
                logger.info('Table_created.')

        return cls._instance

    def __init__(self):
        """
        Initialize the parameter with the class variable
        :param db_config: not used
        """
        self._db_connection =  self._instance.connection
        self._db_cur = self._instance.cursor

    def query(self,query,params=None):
        """

        :param query: query to be executed on database
        :param params: dictionary containing bind parameters.
        :return: result of execute.
        """
        if params is None:
            return self._db_cur.execute(query)
        else:
            return self._db_cur.execute(query,params)

    def __del__(self):
        logger.info("Closing the connection")
        self._db_connection.commit()
        self._db_connection.close()



if __name__ == "__main__":
    connection = databaseConnection()

    insertStatement = "INSERT INTO ticket values(:ticket_id, 54321, 100, 90, 'Sell', 'MSFT', 'Order Received')"
    connection.query(insertStatement,{'ticket_id' : 1234})

    # Query the orders table
    selectStatement = "SELECT * FROM ticket where ticket_id = :ticket_id"

    rows = connection.query(selectStatement,{'ticket_id' : 1234}).fetchall()

    # Print the rows returned by the SELECT Query
    print(rows)