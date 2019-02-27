import logging
from datalayer import databaseconnection,query_config


logger = logging.getLogger(__name__)

def create_report(report_file=None):


    try:
        logger.info("Started Creating Report.")

        conn = databaseconnection.databaseConnection()
        report_query  = query_config.report_query

        exe_query = conn.query(report_query)

        with open(report_file,'w') as rf:
            rf.write("TICKET_ID|TIME_SPEND_OPEN|TIME_SPEND_WAITING_CUSTOMER|TIME_SPEND_PENDING|TIME_TILL_RESOLUTION\n")
            for line in exe_query.fetchall():
                rf.write("|".join(map(str,line)))
                rf.write("\n")

    except FileNotFoundError:
        logger.error("file not found")
        raise
    except Exception as e:
        logger.error("Got error in creating report {}".format(e))
        raise
    else:
        logger.info("Successfully created the report file {}".format(report_file))


#driver for test

if __name__ == "__main__" :
    create_report("sachin.text")