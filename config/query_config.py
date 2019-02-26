



insert_ticket = """
                insert or ignore into ticket (ticket_id, issue_type, status, performed_at, priority, requestor, agent_id )
                                        values (:ticket_id, :issue_type, :status, :performed_at, :priority, :requester,:agent_id)
                """

update_ticket = """
                update ticket set  status = :status, performed_at= :performed_at, requestor = :requester, agent_id = :agent_id
                                    where ticket_id = :ticket_id and performed_at < :performed_at;
                """

insert_ticket_history = """
                        insert into activity_history (ticket_id, status, performed_at, requestor, agent_id )
                                        values (:ticket_id, :status, :performed_at, :requester,:agent_id)
                        """

insert_ticket_details = """
                        insert or ignore into ticket_details (ticket_id, shipping_address, shipment_date, category, group_type )
                                        values (:ticket_id, :shipping_address, :shipment_date, :category, :group)
                        """

