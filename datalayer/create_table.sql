drop table ticket;
drop table ticket_details;
drop table ticket_notes;
drop table activity_history;


CREATE TABLE IF NOT EXISTS ticket
    (
    ticket_id INTEGER PRIMARY KEY,
    issue_type TEXT,
    status TEXT,
    performed_at date,
    priority TEXT,
    requestor INTEGER,
    agent_id INTEGER
    );

CREATE TABLE IF NOT EXISTS ticket_details
    (
    ticket_id INTEGER PRIMARY KEY,
    shipping_address TEXT,
    shipment_date TEXT,
    category TEXT,
    group_type TEXT
    );

CREATE TABLE IF NOT EXISTS ticket_notes
    (
    ticket_id INTEGER,
    note_id INTEGER PRIMARY KEY,
    type INTEGER
    );
CREATE TABLE IF NOT EXISTS activity_history
    (
    ticket_id INTEGER,
    performed_at date,
    status TEXT,
    requestor INTEGER,
    agent_id INTEGER

     );



















