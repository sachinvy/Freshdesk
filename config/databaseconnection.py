import sqlite3
import logging

logger = logging.getLogger(__name__)

class databaseConnection(object):
    """
    Class to create connection to the postgres database
    """
    _instance = None
    def __new__(cls):
        """
        function to initialize the database connection
        :param db_config: db parameter read from config.txt
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

        return cls._instance

    def __init__(self):
        """
        Initialize the parameter with the class variable
        :param db_config: not used
        """
        self._db_connection =  self._instance.connection
        self._db_cur = self._instance.cursor

    def query(self,query,params=(False,)):
        """

        :param query: query to be executed on database
        :param params: dictionary containing bind parameters.
        :return: result of execute.
        """
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