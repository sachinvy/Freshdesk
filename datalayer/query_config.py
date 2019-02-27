



insert_ticket = """
                insert or ignore into ticket (ticket_id, issue_type, status, performed_at, priority, requestor, agent_id )
                                        values (:ticket_id, :issue_type, :status, :performed_at, :priority, :requester,:agent_id)
                """

update_ticket = """
                update ticket set  status = :status, performed_at= :performed_at, requestor = :requester, agent_id = :agent_id
                                    where ticket_id = :ticket_id and performed_at < :performed_at;
                """

insert_ticket_history = """
                        insert or ignore into activity_history (ticket_id, status, performed_at, requestor, agent_id )
                                        values (:ticket_id, :status, :performed_at, :requester,:agent_id)
                        """

insert_ticket_details = """
                        insert or ignore into ticket_details (ticket_id, shipping_address, shipment_date, category, group_type )
                                        values (:ticket_id, :shipping_address, :shipment_date, :category, :group)
                        """


report_query = """
                WITH RECURSIVE
                FILTERED_TICKET(TICKET_ID,PERFORMED_AT,STATUS) AS (
                                             SELECT TICKET_ID,PERFORMED_AT,STATUS FROM ACTIVITY_HISTORY WHERE TICKET_ID IN (SELECT TICKET_ID FROM TICKET WHERE STATUS!='Open')
                                               ),
                TIME_SPEND_OPEN(TICKET_ID,TIME_SPEND_OPEN,PERFORMED_AT) AS (
                                            SELECT A.TICKET_ID,  ROUND((JulianDay(MIN(B.PERFORMED_AT)) - JulianDay(A.PERFORMED_AT))*24*60*60) AS TIME_SPEND_OPEN,A.PERFORMED_AT
                                            FROM FILTERED_TICKET A, FILTERED_TICKET B
                                            WHERE A.STATUS='Open' AND A.TICKET_ID=B.TICKET_ID
                                            AND B.PERFORMED_AT > A.PERFORMED_AT
                                            GROUP BY A.TICKET_ID,A.PERFORMED_AT
                                            ),
                TIME_SPEND_OPEN2(TICKET_ID,TIME_SPEND_OPEN) AS (
                                            SELECT A.TICKET_ID, SUM(A.TIME_SPEND_OPEN)
                                            FROM TIME_SPEND_OPEN A
                                            GROUP BY A.TICKET_ID
                                            ),
                TIME_SPEND_WAITING_CUSTOMER(TICKET_ID,TIME_SPEND_WAITING_CUSTOMER,PERFORMED_AT) AS (
                                             SELECT A.TICKET_ID, ROUND((JulianDay(MIN(B.PERFORMED_AT)) - JulianDay(A.PERFORMED_AT))*24*60*60) AS TIME_SPEND_OPEN,A.PERFORMED_AT
                                            FROM FILTERED_TICKET A, FILTERED_TICKET B
                                            WHERE A.STATUS='Waiting for Customer' AND A.TICKET_ID=B.TICKET_ID
                                            AND B.PERFORMED_AT > A.PERFORMED_AT
                                            GROUP BY A.TICKET_ID,A.PERFORMED_AT
                                            ),
                TIME_SPEND_WAITING_CUSTOMER2(TICKET_ID,TIME_SPEND_WAITING_CUSTOMER) AS (
                                             SELECT A.TICKET_ID,SUM(A.TIME_SPEND_WAITING_CUSTOMER)
                                             FROM TIME_SPEND_WAITING_CUSTOMER A
                                            GROUP BY A.TICKET_ID
                                            ),
                TIME_SPEND_PENDING(TICKET_ID,TIME_SPEND_PENDING,PERFORMED_AT) AS (
                                             SELECT A.TICKET_ID, ROUND((JulianDay(MIN(B.PERFORMED_AT)) - JulianDay(A.PERFORMED_AT))*24*60*60) AS TIME_SPEND_OPEN,A.PERFORMED_AT
                                            FROM FILTERED_TICKET A, FILTERED_TICKET B
                                            WHERE A.STATUS='Pending' AND A.TICKET_ID=B.TICKET_ID
                                            AND B.PERFORMED_AT > A.PERFORMED_AT
                                            GROUP BY A.TICKET_ID,A.PERFORMED_AT
                
                                ),
                TIME_SPEND_PENDING2(TICKET_ID,TIME_SPEND_PENDING) AS (
                                             SELECT A.TICKET_ID,SUM(A.TIME_SPEND_PENDING)
                                             FROM TIME_SPEND_PENDING A
                                            GROUP BY A.TICKET_ID
                
                                ),
                TIME_TILL_RESOLUTION(TICKET_ID, TIME_TILL_RESOLUTION) AS (
                                             SELECT A.TICKET_ID, ROUND((JulianDay(A.PERFORMED_AT)-JulianDay(MIN(B.PERFORMED_AT)))*24*60*60) AS TIME_SPEND_OPEN
                                            FROM FILTERED_TICKET A, FILTERED_TICKET B
                                            WHERE A.STATUS='Resolved' AND A.TICKET_ID=B.TICKET_ID
                                            GROUP BY A.TICKET_ID
                
                ),
                FIRST_JOIN(TICKET_ID, TIME_SPEND_OPEN, TIME_SPEND_WAITING_CUSTOMER) AS (
                                                SELECT A.TICKET_ID, A.TIME_SPEND_OPEN, ifnull(B.TIME_SPEND_WAITING_CUSTOMER,0)
                                                FROM TIME_SPEND_OPEN2 A LEFT OUTER JOIN TIME_SPEND_WAITING_CUSTOMER2 B
                                                ON A.TICKET_ID = B.TICKET_ID
                ),
                SECOND_JOIN(TICKET_ID, TIME_SPEND_OPEN, TIME_SPEND_WAITING_CUSTOMER, TIME_SPEND_PENDING ) AS (
                                                SELECT A.TICKET_ID, A.TIME_SPEND_OPEN, A.TIME_SPEND_WAITING_CUSTOMER, ifnull(B.TIME_SPEND_PENDING,0)
                                                FROM FIRST_JOIN A LEFT OUTER JOIN TIME_SPEND_PENDING2 B
                                                ON A.TICKET_ID = B.TICKET_ID
                
                ),
                THIRD_JOIN(TICKET_ID, TIME_SPEND_OPEN, TIME_SPEND_WAITING_CUSTOMER,TIME_SPEND_PENDING, TIME_TILL_RESOLUTION ) AS (
                                                SELECT A.TICKET_ID, A.TIME_SPEND_OPEN, A.TIME_SPEND_WAITING_CUSTOMER, A.TIME_SPEND_PENDING,ifnull(B.TIME_TILL_RESOLUTION,0)
                                                FROM SECOND_JOIN A LEFT OUTER JOIN TIME_TILL_RESOLUTION B
                                                ON A.TICKET_ID = B.TICKET_ID
                )
                SELECT * FROM THIRD_JOIN

               """

create_table = """
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
                    agent_id INTEGER,
                    PRIMARY KEY(ticket_id, status)
                     );
                """