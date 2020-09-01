class Message:

    ALREADY_JOINED = "You are already there in group. Why do you want link ?"

    BAD_COMMAND = "What do you mean ? This action will be reported."

    INELIGIBLE_USER = "Sorry you are not eligible to generate join link. If you think it is wrong, tell me why."

    INVALID_REPLY = "You should reply to a message for this action to proceed."

    LABEL_GET_LINK = "Get the group link"

    LABEL_JOIN_LINK = "Join the group"

    LINK_CAUTION = (
        "Please join the group by clicking the following button. **Remember the link may expire anytime**."
        "If it happens, you can regenerate another by sending /link."
    )

    PM_FOR_LINK = "You are just a click away from joining the group. Please click the button below to get the group link."

    REMIND_UNAPPROVED_USERS = (
        "A reminder that you have not explained your eligibility to join the private group."
        "If you continue to remain silent you will be **removed** from the group soon !"
    )

    REMOVED_EXPIRED_USERS = "As a part of regular clean up, I removed {COUNT} users."

    REMOVED_USER = "I have removed the user."

    REQUEST_EXPLANATION = "Please tell me a few words about you or why you should be added to the original group."

    REVOKED_LINK = "I have revoked the old link and generated new one."

    SENT_LINK = "I have sent the link to the user."

    SENT_MESSAGE_TEXT = "Sent the message to the user."

    SENT_REQUEST_EXPLANATION = "I have asked the user for explanation."

    UNAPPROVED_USER = "Sorry, you are not verified. Please tell me a few words about you or why you should be added to the original group."
