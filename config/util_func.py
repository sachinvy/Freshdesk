import itertools
import random as ran
import argparse
import logging
from datetime import timedelta
from config import system_config as s

logger = logging.getLogger(__name__)
"""
module containing all the utility functions, used to create random selection for creating a ticket and activity on it.
"""

def get_note_type():
    """

    :return: function return random choice from list containing valid values for note.
    """
    return ran.choice(s.note)


def get_source():
    """

    :return: function return random choice from list containing valid values for source.
    """
    return ran.choice(s.source)



def get_requester_id():
    """

    :return: function return random choice for requestor value between 10000 and 15000.
    """
    return ran.randint(10000,15000)



def get_random_time():
    """

    :return: function return random timedelta value.
    """
    return timedelta(seconds=ran.randint(100,3000))



def get_priority():
    """

    :return: function return random choice from list containing valid values for priority.
    """
    return ran.choice(s.priority)



id = itertools.count(1500,1)

def get_ticket_id():
    """

    :return: return next ticket id value.
    """
    return next(id)



note_id = itertools.count(55555,1)

def get_note_id():
    """

    :return: return next note id value.
    """
    return next(note_id)



def get_work_flow():
    """

    :return: function return random slice as work flow from list containing valid values for status.
    """
    value = ran.randint(1,len(s.status))

    return s.status[:value]



def get_agent_id():
    """

    :return: function return random choice from list containing valid values for agent_id.
    """
    return ran.choice(s.agent_id)



def performer_id():
    """

    :return: function return random choice from list containing valid values for agent_id.
    """
    return ran.choice(s.agent_id)



def get_boolean():
    """

    :return: function return random choice from list containing valid boolean values. need to use this as actual boolean
            True and False give validation error in json.
    """
    return ran.choice(["true", "false"])



def create_note():
    """

    :return: function returns true for a random occurrence of digit 4, used to add notes to the ticket.
    """
    return 4 == ran.randint(1,10)



def get_issue_type():
    """

    :return: function return random choice from list containing valid values for issue_type.
    """
    return ran.choice(s.issue_type)



def get_random_category():
    """

    :return: function return random choice from list containing valid values for category.
    """
    return ran.choice(s.category)



def get_random_group():
    """

    :return: function return random choice from list containing valid values for group.
    """
    return ran.choice(s.group)

def parse_argument():

    try :
        parser = argparse.ArgumentParser(add_help=False)

        parser.add_argument('-n',dest='number_of_ticket', action="store",type=int)
        parser.add_argument('-o',dest='file_name', action="store")
        parser.add_argument('-r',dest='report_file', action="store")

        return parser.parse_args()
    except Exception as e:
        logger.error("Not able to parse the input argument because of error {}".format(e))

#driver program for testing.
if __name__ == "__main__":
    test = (parse_argument())
    print(test.number_of_ticket)


