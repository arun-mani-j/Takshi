class Query:

    APPROVE_USER = (
        "UPDATE members SET approved = TRUE, rejected = FALSE WHERE user_id = %s;"
    )

    ADD_USER_TO_GATEWAY = (
        "INSERT INTO members(user_id, gateway) VALUES {LIST_S} ON CONFLICT (user_id) DO UPDATE SET joined = NOW(), gateway = TRUE; "
    )

    ADD_USER_TO_GROUP = "INSERT INTO members(user_id, private_group) VALUES {LIST_S} ON CONFLICT (user_id) DO UPDATE SET private_group = TRUE; "

    ELIGIBLE_FOR_LINK = (
        "SELECT private_group, approved, restricted FROM members WHERE user_id = %s;"
    )

    EXPIRED_USERS = "SELECT user_id FROM members WHERE joined <= %s;"

    IS_USER_APPROVED = "SELECT approved FROM members WHERE user_id = %s;"

    IS_USER_IN_GATEWAY = "SELECT gateway FROM members WHERE user_id = %s;"

    IS_USER_IN_GROUP = "SELECT private_group FROM members WHERE user_id = %s;"

    IS_USER_REJECTED = "SELECT rejected FROM members WHERE user_id = %s;"

    REMOVE_USER_FROM_GATEWAY = "UPDATE members SET gateway = FALSE WHERE user_id = %s;"

    REMOVE_USER_FROM_GROUP = (
        "UPDATE members SET private_group = FALSE WHERE user_id = %s;"
    )

    RESTRICT_USER = (
        "UPDATE members SET approved = FALSE, restricted = TRUE WHERE user_id = %s;"
    )

    UNAPPROVED_USERS = "SELECT user_id FROM members WHERE approved = FALSE;"
