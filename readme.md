

#Introduction 
### Freshdesk, a helpdesk system, allows the export of activity information of all tickets. 
### The export takes the following form: 

{ 
"metadata": { 
"start_at": "20-04-2017 10:00:00 +0000", 
"end_at": "21-04-2017 09:59:59 +0000", 
"activities_count": 2 
}, 
"activities_data": [ 
{ 
"performed_at": "21-04-2017 09:33:38 +0000", 
"ticket_id": 600, 
"performer_type": "user", 
"performer_id": 149018, 
"activity": { 
"note": { 
"id": 4025864, 
"type": 4 
} 
} 
}, 
{ 
"performed_at": "21-04-2017 09:38:24 +0000", 
"ticket_id": 704, 
"performer_type": "user", 
"performer_id": 149018, 
"activity": { 
"shipping_address": "N/A", 
"shipment_date": "21 Apr, 2017", 
"category": "Phone", 
"contacted_customer": true, 
"issue_type": "Incident", 
"source": 3, 
"status": "Open", 
"priority": 4, 
"group": "refund", 
"agent_id": 149018, 
"requester": 145423, 
"product": "mobile" 
} 
] 
} 


The status column can be any of the following values: 
- "Open"
- "Closed"
- "Resolved"
- "Waiting for Customer"
- "Waiting for Third Party"
- "Pending"

## Solution
- Random Realistic Ticket Creator (./config/ticket_creator.py) aka RRTC
  - Python program generates the random ticket data based on configuration file (./config/system_config.py), which is having valid values of all the parameter of tickets and activities on ticket.
  - Program also randomly (not really :) ) selects the work flow of activities to be performed on tickets based on above mentioned config file.
  - loads the data in to a json file.
- Ticket Loader to sqlite (./datalayer/databaseloader.py)
  - This programs takes the json file created by RRTC and loads them to sqlite database.
  - Please refer below for table schema.
- Report Generator (./datalayer/report_generator.py)
  - Runs the report query on sqlite database and extracts below parameter.
    - Time spent Open
    - Time spent Waiting on Customer
    - Time spent waiting for response (Pending Status)
    - Time till resolution
    - Time to first response (Not available as this is same as Open to any other stage)
- wrapper (./main_program.py)
    - wrapper scripts to run all the above program sequentially.
    - format to run 
    ```python
       >python main_program.py -n <number_of_tickets_to_create> -o <Json_file_name> -r <report_file_name>
       >python main_program.py -n 10 -o sachin.json -r sachin.report.txt
    ```
Notes :
- Script is creating sqlite database if not exist in ./
- Currently workflow of activities is not random completely, it follows a hard coded sequence and we are taking random slice from that sequence. 
- Currently the output file is having a json structure, writing list containing json instead of each line of file having json structure.
- Currently this program is creating note to tickets but not adding it to database.
  
  
  
  
  
  
  
  - Database schema :
    - Ticket
        = table containing current status of all the tickets in the system

Column_name      | Data type   | Constraint    | Default   | comment                                  
-----------------|-------------|---------------|-----------|------------------------------------------
ticket_id        | INT | PRIMARY KEY | | Ticket id of ticket.
issue_type | Text | | | Issue type of ticket
status | Text | | | current status of ticket
performed_at | Date | | | when the activity was performed on this ticket
priority | Text | | | Priority of ticket.
requestor| INT | | | Id of person requested to open this ticket
agent_id | INT | | | Id of agent currently handing this ticket

       - Activity_history =  table contains all the activity performed on the ticket with details of activity.
    
Column_name      | Data type   | Constraint    | Default   | comment                                  
-----------------|-------------|---------------|-----------|------------------------------------------
ticket_id        | INT |  | | Ticket id of ticket.
status | Text | | | status of ticket
performed_at | Date | | | when the activity was performed on this ticket
requestor| INT | | | Id of person requested activity this ticket
agent_id | INT | | | Id of agent performed activity on this ticket

   - Ticket_details = Table containing Ticket details.
   
Column_name      | Data type   | Constraint    | Default   | comment                                  
-----------------|-------------|---------------|-----------|------------------------------------------
ticket_id        | INT |  | | Ticket id of ticket.
shipping_address | Text | | | Shipment address of product.
Shipment_date | Date | | | shipment date
category| Text | | | Category of product
Group_type | Text | | | Group handling the ticket.

   
