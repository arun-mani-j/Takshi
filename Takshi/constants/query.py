class Query:

    ADD_USER_GATEWAY = (
        "INSERT INTO users (id, user_id, in_gateway) VALUES {LIST_S} "
        "ON CONFLICT (id, user_id) DO UPDATE SET joined = NOW(), in_gateway = TRUE;"
    )

    ADD_USER_PRIVATE_GROUP = (
        "INSERT INTO users (id, user_id, in_group) VALUES {LIST_S} "
        "ON CONFLICT (id, user_id) DO UPDATE SET in_group = TRUE;"
    )

    APPROVE_USER = "UPDATE users SET approved = TRUE, restricted = FALSE WHERE id = %s AND user_id = %s;"

    CREATE_GROUP = (
        "INSERT INTO groups (title, gateway_id, moderate_id, private_group_id, admins, clean_interval, prompt, refresh_interval) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING RETURNING id;"
    )

    DELETE_GROUP = "DELETE FROM groups WHERE id = %s;"

    ELIGIBLE_FOR_LINK = "SELECT in_private_group, approved, restricted FROM users WHERE id = %s AND user_id = %s;"

    FIND_ID = (
        "SELECT id, ARRAY_POSITION(ARRAY[gateway_id = %s, moderate_id = %s,  private_group_id = %s], TRUE) "
        "FROM groups WHERE gateway_id = %s OR moderate_id = %s OR private_group_id = %s;"
    )

    GET_ADMINS = "SELECT admins FROM groups WHERE id = %s;"

    GET_CLEAN_INTERVAL = "SELECT clean_interval FROM groups WHERE id = %s;"

    GET_CHAT_IDS = (
        "SELECT gateway_id, moderate_id, private_group_id FROM groups WHERE id = %s;"
    )

    GET_CONTROLLED_GROUPS = "SELECT id, title FROM groups WHERE %s = ANY(admins);"

    GET_GROUPS = "SELECT groups.id, groups.title FROM groups, users WHERE groups.id = users.id AND users.user_id = %s;"

    GET_GATEWAY_ID = "SELECT gateway_id FROM groups WHERE id = %s;"

    GET_INTERVALS = "SELECT id, clean_interval, refresh_interval FROM groups;"

    GET_INVITE_LINK = "SELECT invite_link FROM groups WHERE id = %s;"

    GET_MODERATE_ID = "SELECT moderate_id FROM groups WHERE id = %s;"

    GET_OUTDATED_USERS = (
        "SELECT user_id FROM users "
        "JOIN groups ON users.id = groups.id "
        "WHERE groups.id = %s AND users.in_gateway "
        "AND EXTRACT(EPOCH FROM (NOW() - users.joined)) / 60 >= groups.clean_interval;"
    )

    GET_PRIVATE_GROUP_ID = "SELECT private_group_id FROM groups WHERE id = %s;"

    GET_PROMPT = "SELECT prompt FROM groups WHERE id = %s;"

    GET_REFRESH_INTERVAL = "SELECT refresh_interval FROM groups WHERE id = %s;"

    GET_TITLE = "SELECT title FROM groups WHERE id = %s;"

    GET_TO_REMIND_USERS = (
        "SELECT user_id FROM users "
        "JOIN groups ON users.id = groups.id "
        "WHERE groups.id = %s AND users.in_gateway = TRUE "
        "AND EXTRACT(EPOCH FROM (NOW() - users.joined)) / 60 >= groups.clean_interval / 2;"
    )

    GET_UNAPPROVED_USERS = "SELECT user_id FROM users WHERE id = %s AND approved;"

    IGNORE_USER = "DELETE FROM users WHERE id = %s AND user_id = %s;"

    REMOVE_USER_GATEWAY = (
        "UPDATE users SET in_gateway = FALSE WHERE id = %s AND user_id = %s;"
    )

    REMOVE_USER_GROUP = (
        "UPDATE users SET in_private_group = FALSE WHERE id = %s AND user_id = %s;"
    )

    RESTRICT_USER = "UPDATE users SET approved = FALSE, restricted = TRUE WHERE id = %s AND user_id = %s;"

    SET_ADMINS = "UPDATE groups SET admins = %s WHERE id = %s;"

    SET_CLEAN_INTERVAL = "UPDATE groups SET clean_interval = %s WHERE id = %s;"

    SET_INVITE_LINK = "UPDATE groups SET invite_link = %s WHERE id = %s;"

    SET_PROMPT = "UPDATE groups SET prompt = %s WHERE id = %s;"

    SET_REFRESH_INTERVAL = "UPDATE groups SET refresh_interval = %s WHERE id = %s;"

    SET_TITLE = "UPDATE groups SET title = %s WHERE id = %s;"

    USER_ADMIN = "SELECT %s = ANY(admins) FROM groups WHERE id = %s;"

    USER_APPROVED = "SELECT approved FROM users WHERE id = %s AND user_id = %s;"

    USER_IN_GATEWAY = "SELECT in_gateway FROM users WHERE id = %s AND user_id = %s;"

    USER_IN_GROUP = "SELECT in_private_group FROM users WHERE id = %s AND user_id = %s;"

    USER_RESTRICTED = "SELECT restricted FROM users WHERE id = %s AND user_id = %s;"
