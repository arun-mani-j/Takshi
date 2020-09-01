import psycopg2

from .query import Query


class Processor:
    def __init__(self, database_url):

        self.connection = psycopg2.connect(database_url)

    def add_user_to_gateway(self, *user_ids):

        cursor = self.connection.cursor()
        list_s = "(%s, TRUE)," * len(user_ids)
        cursor.execute(Query.ADD_USER_TO_GATEWAY.format(LIST_S=list_s), user_ids)
        cursor.close()

    def add_user_to_group(self, *user_ids):

        cursor = self.connection.cursor()
        list_s = "(%s, TRUE)," * len(user_ids)
        cursor.execute(Query.ADD_USER_TO_GROUP.format(LIST_S=list_s), user_ids)
        cursor.close()

    def approve_user(self, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.APPROVE_USER, (user_id,))
        cursor.close()

    def close(self):

        self.connection.close()

    def get_expired_users(self, limit):

        cursor = self.connection.cursor()
        cursor.execute(Query.EXPIRED_USERS, (limit,))
        for user_id in cursor:
            yield user_id
        cursor.close()

    def get_unapproved_users(self):

        cursor = self.connection.cursor()
        cursor.execute(Query.UNAPPROVED_USERS)
        for user_id in cursor:
            yield user_id
        cursor.close()

    def get_user_eligible_for_link(self, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.ELIGIBLE_FOR_LINK, (user_id,))
        vals = next(cursor, (False, False, False))
        cursor.close()

        in_group, approved, restricted = vals
        if not approved or restricted:
            return -1
        if approved and not in_group:
            return 0
        if in_group:
            return 1

    def is_user_approved(self, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.IS_USER_APPROVED, (user_id,))
        val = next(cursor, False)
        cursor.close()
        return val

    def is_user_in_gateway(self, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.IS_USER_IN_GATEWAY, (user_id,))
        val = next(cursor, False)
        cursor.close()
        return val

    def is_user_in_group(self, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.IS_USER_IN_GROUP, (user_id,))
        val = next(cursor, False)
        cursor.close()
        return val

    def is_user_rejected(self, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.IS_USER_REJECTED, (user_id,))
        val = next(cursor, False)
        cursor.close()
        return val

    def remove_user_from_gateway(self, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.REMOVE_USER_FROM_GATEWAY, (user_id,))
        cursor.close()

    def remove_user_from_group(self, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.REMOVE_USER_FROM_GROUP, (user_id,))
        cursor.close()

    def restrict_user(self, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.RESTRICT_USER, (user_id,))
        cursor.close()
