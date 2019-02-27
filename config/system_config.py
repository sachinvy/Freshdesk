#!/usr/bin/env python
"""
system_config.py

this file contains all the config and validvalues for parameters in ticketing system.

"""

#valid values of note type in the activity.
note = [
         "Reply",
         "Forward",
         "Reply_to_forward",
         "Private_note",
         "Public_note",
         "Phone_note",
         "Broadcast_note"
        ]

#valid values for source in activity
source = [
        "Email",
        "Portal",
        "Phone",
        "Forums",
        "Twitter",
        "Facebook",
        "Chat",
        "Mobihelp",
        "Feedback widget",
        "Outbound email",
        "E-commerce",
        "Bot"
        ]


#valid values of priority for ticket
priority = [
            "Low",
            "Medium",
            "High",
            "Urgent"
            ]

#valid values of status for ticket, we will be using same order for workflow
status = [
            "Open",
            "Waiting for Customer",
            "Waiting for Third Party",
            "Pending",
            "Open",
            "Resolved",
            "Closed"
         ]

# valid agent id of agent working in our system
agent_id = [
            149015, #
            149016, #
            149017,
            149018]


# valid values for issue type
issue_type = [
                'Incident',
                'Issue',
                'Defect'
                ]
# valid values for group
group = [
                'Refund',
                'Delivery',
                'Engineering'
        ]
# valid values for category
category = [
                'Phone',
                'Tablet',
                'Wearable'
            ]
