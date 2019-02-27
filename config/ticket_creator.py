
from datetime import datetime
import logging
import json
import config.util_func as sc
from config import loggerinit


logger = logging.getLogger(__name__)

class Ticket():

    """
    Ticket class contains all the attributes which are common for all activies for ticket.

    """

    def __init__(self):
        """
        constructor of class ticket,
        Initializes all the attributes and creates all the activities based on work flow.
        """
        self.ticket_id = sc.get_ticket_id()
        self.priority = sc.get_priority()
        self.work_flow = sc.get_work_flow()
        self.requester = sc.get_requester_id()
        self.activities = []
        self.notes = []
        self.performed_at = datetime.now()

        #local variables used to passed as parameter to constructor of Activity.
        group = sc.get_random_group()
        category = sc.get_random_category()
        issue_type = sc.get_issue_type()


        logger.debug("Creating ticket {} with activities {}.".format(self.ticket_id,", ".join(self.work_flow)))

        if len(self.work_flow) == 0 :
            logger.error("There is no workflow configured. exiting the program")
            assert()

        for action in self.work_flow:
            self.activities.append(Activity(action, self.performed_at,issue_type,category, group))
            self.performed_at += sc.get_random_time()
            if sc.create_note():
                self.notes.append(Note())
                self.performed_at += sc.get_random_time()

    def get_json(self):
        """
        function to convert class attribute to dictionary which will be used to create final json.
        :return: list containing dictionary/json data for each activity on the ticket.
        """
        all_activity_data =[]
        for act in self.activities:
            activity_data = {}
            activity_data['performed_at'] = act.performed_at
            activity_data['ticket_id'] = self.ticket_id
            activity_data['performer_type'] = "user"
            activity_data['performer_id'] = sc.get_agent_id()
            activity_data['activity'] = act.get_json()
            all_activity_data.append(activity_data)

        for n in self.notes:
            note_data = {}
            note_data['performed_at'] = str(self.performed_at)
            note_data['ticket_id'] = self.ticket_id
            note_data['performer_type'] = "user"
            note_data['performer_id'] = sc.get_agent_id()
            note_data['activity'] = n.get_json()
            all_activity_data.append(note_data)

        return all_activity_data



    def print_ticket(self):
        """
        To be used only to debug, prints all the attribute of object's of Class Ticket and Activities
        :return:
        """

        for k, v in self.__dict__.items():
            logger.debug("{} = {}".format(k,v))

        for act in self.activities:
            logger.debug("Activity==========")
            for k, v in act.__dict__.items():
                logger.debug("{} = {}".format(k, v))

class Note():
    """
    class containing all the attributes of Note added to the ticket.

    """
    def __init__(self):
        self.note_id = sc.get_note_id()
        self.type = sc.get_note_type()

    def get_json(self):
        note_sub_data = {}
        note_sub_data['note'] = {}
        note_sub_data['note']['note_id'] = self.note_id
        note_sub_data['note']['type'] = self.type
        return note_sub_data


class Activity():
    """
    Class containing various activity performed on the ticket.
    """
    def __init__(self, action="Open", performed_at=False, priority="Medium",issue_type="Incident", category="Phone", group="Refund"):


        self.performed_at = str(performed_at)
        self.shipping_address = "NA"
        self.shipment_date = "{:%d %b %Y}".format(performed_at)
        self.contacted_customer = sc.get_boolean()
        self.source = sc.get_source()
        self.status = action
        self.agent_id = sc.get_agent_id()
        self.group =  group
        self.product = "mobile"
        self.category = category
        self.issue_type = issue_type
        self.priority = priority
        self.requester = sc.get_requester_id()

    def get_json(self):

        """
        function to convert class attribute to dictionary which will be used to create final json.
        :return: dictionary/json data for each activity on the ticket.
        """
        activity_sub_data = {}
        activity_sub_data['shipping_address'] = self.shipping_address
        activity_sub_data['shipment_date'] = self.shipment_date
        activity_sub_data['category'] = self.category
        activity_sub_data['contacted_customer'] = self.contacted_customer
        activity_sub_data["issue_type"] = self.issue_type
        activity_sub_data["source"] = self.source
        activity_sub_data["status"] = self.status
        activity_sub_data["priority"] = self.priority
        activity_sub_data["group"] = self.group
        activity_sub_data["agent_id"] = self.agent_id
        activity_sub_data["requester"] = self.requester
        activity_sub_data["product"] = self.product

        return activity_sub_data

def create_multiple_tickets(num_of_ticket=0,output_file=None):
    """

    :param num_of_ticket:
    :param output_file:
    :return:
    """

    try:
        final_list = []
        logger.info("Started creating tickets")
        for i in range(num_of_ticket):
            final_list = final_list + Ticket().get_json()

        with open(output_file,'w') as of:
            json.dump(final_list,of)


    except FileNotFoundError as e:
        logger.error("Not able to open input file")
        raise

    except Exception as e:
        logger.error("Got exception {} while creating ticket.".format(e))
        raise

    else:
        logger.info("All the tickets are written to output file")


if __name__ == "__main__":
    # driver program for testing.
    create_multiple_tickets(10,"test.json")
