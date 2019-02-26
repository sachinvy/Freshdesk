drop table ticket;
drop table ticket_details;
drop table ticket_notes;
drop table activity_history;


create table ticket
    (
    ticket_id INTEGER PRIMARY KEY,
    issue_type TEXT,
    status TEXT,
    performed_at date,
    priority TEXT,
    requestor INTEGER,
    agent_id INTEGER
    );

 create table ticket_details
    (
    ticket_id INTEGER PRIMARY KEY,
    shipping_address TEXT,
    shipment_date TEXT,
    category TEXT,
    group_type TEXT
    );

create table ticket_notes
    (
    ticket_id INTEGER,
    note_id INTEGER PRIMARY KEY,
    type INTEGER
    );
create table activity_history
    (
    ticket_id INTEGER,
    performed_at date,
    status TEXT,
    requestor INTEGER,
    agent_id INTEGER
     );



with recursive
time_spend_open(ticket_id,time_spend_open)
as (
select a.ticket_id,(JulianDay(min(b.performed_at))-JulianDay(a.performed_at))*24*60*60 as time_spend_open
from activity_history a, activity_history b
where a.status='Open' and b.status!='Open'
and a.ticket_id=b.ticket_id group by a.ticket_id)
select * from time_spend_open;

WITH RECURSIVE
FILTERED_TICKET(TICKET_ID,PERFORMED_AT,STATUS) AS (
                             SELECT TICKET_ID,PERFORMED_AT,STATUS FROM ACTIVITY_HISTORY WHERE TICKET_ID IN (SELECT TICKET_ID FROM TICKET WHERE STATUS!='Open')
                               ),
TIME_SPEND_OPEN(TICKET_ID,TIME_SPEND_OPEN) AS (
                            SELECT A.TICKET_ID, ROUND((JulianDay(MIN(B.PERFORMED_AT)) - JulianDay(A.PERFORMED_AT))*24*60*60) AS TIME_SPEND_OPEN
                            FROM FILTERED_TICKET A, FILTERED_TICKET B
                            WHERE A.STATUS='Open' AND A.TICKET_ID=B.TICKET_ID
                            AND B.PERFORMED_AT > A.PERFORMED_AT
                            GROUP BY A.TICKET_ID,A.PERFORMED_AT
                            ),
TIME_SPEND_WAITING_CUSTOMER(TICKET_ID,TIME_SPEND_WAITING_CUSTOMER) AS (
                             SELECT A.TICKET_ID, ROUND((JulianDay(MIN(B.PERFORMED_AT)) - JulianDay(A.PERFORMED_AT))*24*60*60) AS TIME_SPEND_OPEN
                            FROM FILTERED_TICKET A, FILTERED_TICKET B
                            WHERE A.STATUS='Waiting for Customer' AND A.TICKET_ID=B.TICKET_ID
                            AND B.PERFORMED_AT > A.PERFORMED_AT
                            GROUP BY A.TICKET_ID,,A.PERFORMED_AT
                            ),
TIME_SPEND_PENDING(TICKET_ID,TIME_SPEND_PENDING) AS (
                             SELECT A.TICKET_ID, ROUND((JulianDay(MIN(B.PERFORMED_AT)) - JulianDay(A.PERFORMED_AT))*24*60*60) AS TIME_SPEND_OPEN
                            FROM FILTERED_TICKET A, FILTERED_TICKET B
                            WHERE A.STATUS='Pending' AND A.TICKET_ID=B.TICKET_ID
                            AND B.PERFORMED_AT > A.PERFORMED_AT
                            GROUP BY A.TICKET_ID

                ),
TIME_TILL_RESOLUTION(TICKET_ID, TIME_TILL_RESOLUTION) AS (
                             SELECT A.TICKET_ID, ROUND((JulianDay(A.PERFORMED_AT)-JulianDay(MIN(B.PERFORMED_AT)))*24*60*60) AS TIME_SPEND_OPEN
                            FROM FILTERED_TICKET A, FILTERED_TICKET B
                            WHERE A.STATUS='Resolved' AND A.TICKET_ID=B.TICKET_ID
                            GROUP BY A.TICKET_ID,A.PERFORMED_AT

),
FIRST_JOIN(TICKET_ID, TIME_SPEND_OPEN, TIME_SPEND_WAITING_CUSTOMER) AS (
                                SELECT A.TICKET_ID, A.TIME_SPEND_OPEN, ifnull(B.TIME_SPEND_WAITING_CUSTOMER,0)
                                FROM TIME_SPEND_OPEN A LEFT OUTER JOIN TIME_SPEND_WAITING_CUSTOMER B
                                ON A.TICKET_ID = B.TICKET_ID
),
SECOND_JOIN(TICKET_ID, TIME_SPEND_OPEN, TIME_SPEND_WAITING_CUSTOMER, TIME_SPEND_PENDING ) AS (
                                SELECT A.TICKET_ID, A.TIME_SPEND_OPEN, A.TIME_SPEND_WAITING_CUSTOMER, ifnull(B.TIME_SPEND_PENDING,0)
                                FROM FIRST_JOIN A LEFT OUTER JOIN TIME_SPEND_PENDING B
                                ON A.TICKET_ID = B.TICKET_ID

),
THIRD_JOIN(TICKET_ID, TIME_SPEND_OPEN, TIME_SPEND_WAITING_CUSTOMER,TIME_SPEND_PENDING, TIME_TILL_RESOLUTION ) AS (
                                SELECT A.TICKET_ID, A.TIME_SPEND_OPEN, A.TIME_SPEND_WAITING_CUSTOMER, A.TIME_SPEND_PENDING,ifnull(B.TIME_TILL_RESOLUTION,0)
                                FROM SECOND_JOIN A LEFT OUTER JOIN TIME_TILL_RESOLUTION B
                                ON A.TICKET_ID = B.TICKET_ID
)
SELECT * FROM THIRD_JOIN






WITH RECURSIVE
FILTERED_TICKET(TICKET_ID,PERFORMED_AT,STATUS) AS (
                             SELECT TICKET_ID,PERFORMED_AT,STATUS FROM ACTIVITY_HISTORY WHERE TICKET_ID IN (SELECT TICKET_ID FROM TICKET WHERE STATUS!='Open')
                               ),
TIME_SPEND_OPEN(TICKET_ID,TIME_SPEND_OPEN) AS (
                           SELECT A.TICKET_ID, A.PERFORMED_AT, ROUND((JulianDay(MIN(B.PERFORMED_AT)) - JulianDay(A.PERFORMED_AT))*24*60*60) AS TIME_SPEND_OPEN
                            FROM FILTERED_TICKET A, FILTERED_TICKET B
                            WHERE A.STATUS='Open' AND A.TICKET_ID=B.TICKET_ID
                            AND B.PERFORMED_AT > A.PERFORMED_AT
                            GROUP BY A.TICKET_ID,A.PERFORMED_AT
                            )
                            SELECT * FROM TIME_SPEND_OPEN;

















