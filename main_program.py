#!/usr/bin/env python
import logging
from config import util_func as uf
from config import loggerinit,ticket_creator
from datalayer import databaseloader as dbloader, report_generator as rg

loggerinit.initialize_logger()
logger = logging.getLogger(__name__)



def main():
    """

    :return:

    """
    try:
        logger.info("Job started.")
        #parse the argument

        argument = uf.parse_argument()

        if not argument.file_name or not argument.number_of_ticket or not argument.report_file:
            logger.error("Invalid command line argument passed")
            raise FileNotFoundError

        #create the tickets

        ticket_creator.create_multiple_tickets(argument.number_of_ticket, argument.file_name)

        #load the ticket to database
        dbloader.load_to_database(argument.file_name)

        # generate the report.
        rg.create_report(argument.report_file)

    except Exception as e:
        logger.error("Got error {}".format(e))
        raise
    else :
        logger.info("Job Completed successfully.")



if __name__ == "__main__":
    main()



