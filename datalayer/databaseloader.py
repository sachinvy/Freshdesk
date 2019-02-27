import json
import logging
from config import loggerinit
from datalayer import query_config, databaseconnection
import sqlite3


logger = logging.getLogger(__name__)

def load_to_database(file_name):
    """
    Function opens the json file and load all the activities to database.
    :param file_name: input json file to be loaded to database
    :return: NA
    """
    try :
        #create connection
        connection = databaseconnection.databaseConnection()

        #open file
        with open(file_name) as tj:
            logger.info("Opened the input file {}".format(file_name))
            try:
                for activity in tj:
                    for ind, act in enumerate(json.loads(activity)):
                        if ind%1000 == 0 :
                            logger.info("Loaded {} records from file.".format(ind))
                        #adding all the attribute inside dictionary tag activity to one level up so that can be used directly for sql binding.
                        act.update(act['activity'])

                        try:
                            if 'note' not in act.keys():
                                #running queries in sequnetial order with dictionary act having all binding parameters
                                connection.query(query_config.insert_ticket, act)
                                connection.query(query_config.update_ticket, act)
                                connection.query(query_config.insert_ticket_details, act)
                                connection.query(query_config.insert_ticket_history, act)
                        except sqlite3.ProgrammingError as e:
                            logger.error("Got {} for row {}.".format(e,act))
                            raise #we can replace this if we want to ignore error and want to deal with them later.

            except Exception as e:
                logger.error("Not able to load the file to database because of error {}".format(e))

    except FileNotFoundError as e:
        logger.error("File : {} not found on disk caused error {}".format(file_name, e))

if __name__ == "__main__" :
    load_to_database("123")


