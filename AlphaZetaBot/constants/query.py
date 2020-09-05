class Query:

    ADD_GROUP = (
        "INSERT INTO groups (id, title, gateway_id, moderate_id, private_group_id, admins, prompt, clean_interval, refresh_interval) "
        "VALUES (DEFAULT %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING RETURNING id;"
    )

    ADD_USERS_GATEWAY = (
        "INSERT INTO users (id, user_id, in_gateway) VALUES {LIST_S} "
        "ON CONFLICT (id, user_id) DO UPDATE SET joined = NOW(), in_gateway = TRUE;"
    )

    ADD_USERS_GROUP = (
        "INSERT INTO users (id, user_id, in_group) VALUES {LIST_S} "
        "ON CONFLICT (id, user_id) DO UPDATE SET in_group = TRUE;"
    )

    APPROVE_USER = "UPDATE users SET approved = TRUE, rejected = FALSE WHERE id = %s AND user_id = %s;"

    DELETE_GROUP = "DELETE FROM groups WHERE id = %s;"

    ELIGIBLE_FOR_LINK = "SELECT in_private_group, approved, restricted FROM users WHERE id = %s AND user_id = %s;"

    EXPIRED_USERS = "SELECT user_id FROM users WHERE id = %s AND joined <= %s;"

    FIND_ID = "SELECT id FROM groups WHERE gateway_id = %s OR moderate_id = %s OR private_group_id = %s;"

    GATEWAY_ID = "SELECT gateway_id FROM groups WHERE id = %s;"

    GET_ADMINS = "SELECT admins FROM groups WHERE id = %s;"

    GET_CHAT_IDS = (
        "SELECT gateway_id, moderate_id, private_group_id FROM groups WHERE id = %s;"
    )

    GET_CLEAN_INTERAVL = "SELECT clean_interval FROM groups WHERE id = %s;"

    GET_GROUPS = "SELECT id, title FROM groups WHERE %s = ANY(admins);"

    GET_INVITE_LINK = "SELECT invite_link FROM groups WHERE id = %s;"

    GET_PROMPT = "SELECT prompt FROM groups WHERE id = %s;"

    GET_REFRESH_INTERVAL = "SELECT refresh_interval FROM groups WHERE id = %s;"

    IGNORE_USER = "DELETE FROM users WHERE id = %s AND user_id = %s;"

    MODERATE_ID = "SELECT moderate_id FROM groups WHERE id = %s;"

    PRIVATE_GROUP_ID = "SELECT private_group_id FROM groups WHERE id = %s;"

    REMOVE_USER_FROM_GATEWAY = (
        "UPDATE users SET in_gateway = FALSE WHERE id = %s AND user_id = %s;"
    )

    REMOVE_USER_FROM_GROUP = (
        "UPDATE users SET in_private_group = FALSE WHERE id = %s AND user_id = %s;"
    )

    RESTRICT_USER = "UPDATE users SET approved = FALSE, restricted = TRUE WHERE id = %s AND user_id = %s;"

    UNAPPROVED_USERS = "SELECT user_id FROM users WHERE id = %s AND approved = FALSE;"

    UPDATE_ADMINS = "UPDATE groups SET admins = %s WHERE id = %s;"

    UPDATE_CLEAN_INTERVAL = "UPDATE groups SET clean_interval = %s WHERE id = %s;"

    UPDATE_INVITE_LINK = "UPDATE groups SET invite_link = %s WHERE id = %s;"

    UPDATE_REFRESH_INTERVAL = "UPDATE groups SET refresh_interval = %s WHERE id = %s;"

    UPDATE_PROMPT = "UPDATE groups SET prompt = %s WHERE id = %s;"

    UPDATE_TITLE = "UPDATE groups SET title = %s WHERE id = %s;"

    USER_APPROVED = "SELECT approved FROM users WHERE id = %s AND user_id = %s;"

    USER_IN_GATEWAY = "SELECT in_gateway FROM users WHERE id = %s AND user_id = %s;"

    USER_IN_GROUP = "SELECT in_private_group FROM users WHERE id = %s AND user_id = %s;"

    USER_RESTRICTED = "SELECT restricted FROM users WHERE id = %s AND user_id = %s;"
