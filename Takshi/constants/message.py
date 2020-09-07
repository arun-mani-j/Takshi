class Message:

    ALREADY_JOINED = "You are already there in group. Why do you want the link ? If you want me to say something to admins, tell me."

    APPROVED_JOIN = "Hey ! You have been approved to join {TITLE}. Please send me a /join and select the group."

    CHAT_ID = "Chat ID : <code>{CHAT_ID}</code>\nUser ID : <code>{USER_ID}</code>"

    CREATE_BANNER = (
        "Creating a new group is easy. Just tell me which group for what purpose and I will start monitoring them.\n"
        " • <b>Gateway</b> - Public group where new users join and verify they are legit.\n"
        " • <b>Moderation</b> - Admins group where I can report status.\n"
        " • <b>Private Group</b> - The real group where approved users can join.\n"
        "\n"
        "If you are confused in any step, check /help.\n"
        "Make sure you <b>make me an admin</b> after adding me !"
    )

    CREATE_NOT_ALLOWED = "Sorry, my owner has not allowed creation of new groups. Not a big deal, you can host me yourself."

    DELETE_GROUP = (
        "Are you sure you want to <b>DELETE {TITLE}</b> ? "
        "All the saved settings and data will be permanently <b>lost</b> !"
    )

    FORWARD_MESSAGE = (
        "User ID : {ID}\nUsername : @{USERNAME}\n{NAME}\nChat ID : {CHAT_ID}\n{TEXT}"
    )

    DONE = "Done successfully !"

    GROUP_CREATED = "New Group <b>{TITLE}</b> have been created successfully ! Check out /settings to tweak the group behavior."

    GROUP_DELETED = "Group {TITLE} deleted successfully !"

    GROUP_EXISTS = "It seems like I'm already monitoring the given group. If you wanted to change settings, try /settings."

    GROUP_COMMAND = "This command is meant to be used in a group."

    GROUP_NOT_FOUND = "{TITLE} is not found. May be someone deleted it now ?"

    IGNORED_USER = "Fine. I'm not bothered about the user now."

    INVALID_COMMAND = "What do you mean ? This action will be reported."

    INVALID_FORWARD = (
        "I'm not able to understand that message. Is it the right message ?"
    )

    INVALID_ID = "No group found with the given ID."

    INVALID_INTERVAL = "Please send a positive integer."

    INVALID_MESSAGE = (
        "I can't understand your reason for a message. "
        "If you wanted to say something to admins of a group, then select a group using /join first."
    )

    INVALID_PROMPT = "Please send a valid text message."

    INVALID_QUERY = "The button click was totally unexpected. Please try again the previous process."

    INVALID_REPLY = "You should reply to a message for this action to proceed."

    INVALID_SESSION_MESSAGE = (
        "I didn't ask you a text message. Please reply using above buttons."
    )
    INVALID_START_ARG = (
        "Nobody expected that argument for /start. What are you trying to do ?"
    )

    JOIN_SELECT_GROUP = (
        "We have the following groups in common. Which one do you want to join ?"
    )

    LINK_CAUTION = (
        "Please join the group by clicking the following button. <b>Remember the link may expire anytime</b>."
        "If it happens, you can regenerate another by clicking on Refresh Link."
    )

    LINK_REFRESHED = "Link refreshed."

    MENTION = "<a href='tg://user?id={USER_ID}'>{CAPTION}</a"

    NO_COMMON_GROUPS = "We have no groups in common. Are you sure that it was me in the gateway group ?"

    PM_COMMAND = "This command is meant to be used in private message. Please contact me in personal message."

    PM_FOR_LINK = "You are just a click away from joining the group. Please click the button below to get the group link."

    PROMPT = "{PROMPT}"

    REMIND_UNAPPROVED_USERS = (
        "A reminder that you have not explained your eligibility to join the private group."
        "If you continue to remain <i>silent</i> you will be <b>removed</b> from the group soon !"
    )

    REMOVED_OUTDATED_USERS = "As a part of regular clean up, I removed {COUNT} users."

    REMOVED_USER = "I have removed the user."

    RESTRICTED_USER = "I have restricted the user."

    REVOKED_LINK = "I have revoked the old link and generated new one."

    SELECT_GATEWAY = "Please choose the Gateway Group."

    SELECT_MODERATE = "Please choose the Moderation Group."

    SELECT_PRIVATE_GROUP = "Please choose the Private Group."

    SELECTED_GATEWAY = "You have selected this group as Gateway Group."

    SELECTED_MODERATE = "You have selected this group as Moderation Group."

    SELECTED_PRIVATE_GROUP = "You have selected this group as Private Group."

    SENT_LINK = "I have sent the link to the user."

    SENT_MESSAGE = "Sent the message to the user."

    SENT_TO_MODERATORS = "I have sent the message to admins of {TITLE}"

    SENT_EXPLANATION = "I have asked the user for explanation."

    SESSION_CONTINUED = "To avoid chat getting clumsy, I have sent a new message below."

    SESSION_EXPIRED = (
        "You have started doing something else. So this session has expired."
    )

    SET_CLEAN_INTERVAL = (
        "New Clean Interval of {TITLE} has been set successfully to {INTERVAL} minutes."
    )

    SET_PROMPT = "New Prompt of {TITLE} has been set successfully to the sent message."

    SET_REFRESH_INTERVAL = "New Refresh Interval of {TITLE} has been set successfully to {INTERVAL} minutes."

    SETTING_CLEAN_INTERVAL = (
        "You are editing <b>Clean Interval</b> of <b>{TITLE}</b>\n"
        "Current value is {INTERVAL} minutes.\n"
        "To change please send a positive number.\n"
    )

    SETTING_PROMPT = (
        "You are editing <b>Prompt</b> of <b>{TITLE}</b>\n"
        "Current prompt :\n"
        "{PROMPT}\n"
        "To change please send me a message.\n"
    )

    SETTING_REFRESH_INTERVAL = (
        "You are editing <b>Refresh Interval</b> of <b>{TITLE}</b>\n"
        "Current value is {INTERVAL} minutes.\n"
        "To change please send a positive number.\n"
    )

    SETTING_UPDATE = (
        "You are viewing <b>Update Difference</b> of <b>{TITLE}</b>\n"
        "Old title : <i>{OLD_TITLE}</i>\n"
        "New title : <i>{NEW_TITLE}</i>\n"
        "\n"
        "Old admins count : <i>{OLD_COUNT}</i>\n"
        "New admins count : <i>{NEW_COUNT}</i>"
    )

    SETTINGS_SELECT_PROPERTY = (
        "You are currently editing <b>{TITLE}</b>\n."
        "The following properties can be changed or used to process a change.\n"
        " • <b>Clean Interval</b> - Time in minutes between two periodic clean up of unapproved members.\n"
        " • <b>Prompt</b> - The message shown to unapproved members when they want to join your group.\n"
        " • <b>Link Refresh Interval</b> - Time in minutes between two refresh of invite links of private group.\n"
        " • <b>Update</b> - Updates admins and title of your group.\n"
        "What do you want to change ?"
    )

    SETTINGS_SELECT_GROUP = (
        "I have the following groups where you are assigned as an admin.\n"
        "Choose the group and then I will show you the properties that can be changed."
    )

    SETTINGS_NO_GROUP = (
        "I can't find any group where you are an admin. Are you sure that I have been assigned to your group ?\n"
        "If you want to create a new group, use /create."
    )

    START = "Hey there ! If you want the link of the group please send me a /link."

    START_GROUP = "Yea, I'm here. What's up ?"

    THANK_FOR_JOIN = "Thanks for joining !"
