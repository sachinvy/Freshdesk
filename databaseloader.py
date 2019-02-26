import json
import logging
from config import databaseconnection,query_config,loggerinit
import sqlite3

loggerinit.initialize_logger()
logger = logging.getLogger(__name__)

def main():
    file_name = "test.json"
    connection = databaseconnection.databaseConnection()
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
                            connection.query(query_config.insert_ticket,act)
                            connection.query(query_config.update_ticket,act)
                            connection.query(query_config.insert_ticket_details,act)
                            connection.query(query_config.insert_ticket_history,act)
                    except sqlite3.ProgrammingError as e:
                        logger.error("Got {} for row {}.".format(e,act))
                        assert() #we can replace this if we want to ignore error and want to deal with them later.
        except KeyError:
            pass

if __name__ == "__main__" :
    main()


