import itertools
import random as ran
from datetime import timedelta
from config import system_config as s


def get_note_type():
    return ran.choice(s.note)


def get_source():
    return ran.choice(s.source)



def get_requester_id():
    return ran.randint(10000,15000)



def get_random_time():
    return timedelta(seconds=ran.randint(100,3000))



def get_priority():
    return ran.choice(s.priority)



id = itertools.count(1500,1)

def get_ticket_id():
    return next(id)



note_id = itertools.count(55555,1)

def get_note_id():
    return next(note_id)



def get_work_flow():
    value = ran.randint(1,len(s.status))

    return s.status[:value]



def get_agent_id():
    return ran.choice(s.agent_id)



def performer_id():
    return ran.choice(s.agent_id)



def get_boolean():
    return ran.choice(["true", "false"])



def create_note():
    return 4 == ran.randint(1,10)



def get_issue_type():
    return ran.choice(s.issue_type)



def get_random_category():
    return ran.choice(s.category)



def get_random_group():
    return ran.choice(s.group)


if __name__ == "__main__":
    print(get_random_group())

