import datetime
import psycopg2

from .query import Query


class Processor:
    def __init__(self, database_url):

        self.connection = psycopg2.connect(database_url)

    def add_user_to_gateway(self, id, *user_ids):

        cursor = self.connection.cursor()
        args = []
        for user_id in user_ids:
            args.extend((id, user_id))
        list_s = f"(%s, %s, TRUE)," * len(user_ids)
        cursor.execute(Query.ADD_USER_GATEWAY.format(LIST_S=list_s), args)
        cursor.close()

    def add_user_to_group(self, *user_ids):

        cursor = self.connection.cursor()
        args = []
        for user_id in user_ids:
            args.extend((id, user_id))
        list_s = f"(%s, %s, TRUE)," * len(user_ids)
        cursor.execute(Query.ADD_USER_PRIVATE_GROUP.format(LIST_S=list_s), args)
        cursor.close()

    def approve_user(self, id, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.APPROVE_USER, (id, user_id))
        cursor.close()

    def close(self):

        self.connection.close()

    def create_group(self, title, gateway_id, moderate_id, private_group_id, admins, clean_interval, prompt, refresh_interval):

        cursor = self.connection.cursor()
        cursor.execute(Query.ADD_GROUP, (title, gateway_id, moderate_id, private_group_id, admins, clean_interval, prompt, refresh_interval))
        id = next(cursor, None)
        cursor.close()
        return id

    def delete_group(self, id):

        cursor = self.connection.cursor()
        cursor.execute(Query.DELETE_GROUP, (id,))
        cursor.close()

    def find_id(self, chat_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.FIND_ID, (chat_id,))
        id = next(cursor, None)
        cursor.close()
        return id

    def get_admins(self, id):

        cursor = self.connection.cursor()
        cursor.execute(Query.GET_ADMINS, (id,))
        admins = next(cursor, [])
        cursor.close()
        return admins

    def get_clean_interval(self, id):

        cursor = self.connection.cursor()
        cursor.execute(Query.GET_CLEAN_INTERVAL, (id,))
        interval = next(cursor, None)
        cursor.close()
        return interval

    def get_chat_ids(self, id):

        cursor = self.connection.cursor()
        cursor.execute(Query.GET_CHAT_IDS, (id,))
        chat_ids = next(cursor, [None, None, None])
        cursor.close()

    def get_eligible_for_link(self, id, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.ELIGIBLE_FOR_LINK, (id, user_id))
        vals = next(cursor, (False, False, False))
        cursor.close()

        in_priv_group, approved, restricted = vals
        if not approved or restricted:
            return -1
        if approved and not in_priv_group:
            return 0
        if in_priv_group:
            return 1

    def get_gateway_id(self, id):

        cursor = self.connection.cursor()
        cursor.execute(Query.GET_GATEWAY_ID, (id,))
        gateway_id  = next(cursor, None)
        cursor.close()
        return gateway_id

    def get_groups(self, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.GET_GROUPS, (user_id,))
        id_titles = next(cursor, [])
        groups = {id: title for id, title in id_titles}
        cursor.close()
        return groups

    def get_invite_link(self, id):

        cursor = self.connection.cursor()
        cursor.execute(Query.GET_INVITE_LINK, (id,))
        link  = next(cursor, None)
        cursor.close()
        return link

    def get_moderate_id(self, id):

        cursor = self.connection.cursor()
        cursor.execute(Query.GET_MODERATE_ID, (id,))
        moderate_id = next(cursor, None)
        cursor.close()
        return moderate_id

    def get_private_group_id(self, id):

        cursor = self.connection.cursor()
        cursor.execute(Query.GET_PRIVATE_GROUP_ID, (id,))
        private_group_id = next(cursor, None)
        cursor.close()
        return private_group_id

    def get_prompt(self, id):

        cursor = self.connection.cursor()
        cursor.execute(Query.GET_PROMPT, (id,))
        prompt = next(cursor, None)
        cursor.close()
        return prompt

    def get_refresh_interval(self, id):

        cursor = self.connection.cursor()
        cursor.execute(Query.GET_REFRESH_INTERVAL, (id,))
        interval = next(cursor, None)
        cursor.close()
        return interval

    def get_title(self, title):

        cursor = self.connection.cursor()
        cursor.execute(Query.GET_TITLE, (id,))
        title = next(cursor, None)
        cursor.close()
        return title

    def get_unapproved_users(self, id, before_date=None):

        cursor = self.connection.cursor()
        if not before_date:
            before_date = datetime.datetime.now()
        cursor.execute(Query.UNAPPROVED_USERS, (id, before_date))
        for user_id in cursor:
            yield user_id
        cursor.close()

    def ignore_user(self, id, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.IGNORE_USER, (id, user_id))
        cursor.close()

    def is_user_approved(self, id, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.USER_APPROVED, (id, user_id))
        val = next(cursor, False)
        cursor.close()
        return val

    def is_user_in_gateway(self, id, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.USER_IN_GATEWAY, (id, user_id))
        val = next(cursor, False)
        cursor.close()
        return val

    def is_user_in_private_group(self, id, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.USER_IN_GROUP, (id, user_id))
        val = next(cursor, False)
        cursor.close()
        return val

    def is_user_restricted(self, id, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.USER_REJECTED, (id, user_id))
        val = next(cursor, False)
        cursor.close()
        return val

    def remove_user_from_gateway(self, id, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.REMOVE_USER_GATEWAY, (id, user_id))
        cursor.close()

    def remove_user_from_group(self, id, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.REMOVE_USER_GROUP, (id, user_id))
        cursor.close()

    def restrict_user(self, id, user_id):

        cursor = self.connection.cursor()
        cursor.execute(Query.RESTRICT_USER, (id, user_id))
        cursor.close()

    def set_admins(self, id, admins):

        cursor = self.connection.cursor()
        cursor.execute(Query.SET_ADMINS, (admins, id))
        cursor.close()

    def set_clean_interval(self, id, interval):

        cursor = self.connection.cursor()
        cursor.execute(Query.SET_CLEAN_INTERAL, (interval, id))
        cursor.close()

    def set_invite_link(self, id, link):

        cursor = self.connection.cursor()
        cursor.execute(Query.SET_INVITE_LINK, (link, id))
        cursor.close()

    def set_prompt(self, id, prompt):

        cursor = self.connection.cursor()
        cursor.execute(Query.SET_PROMPT, (prompt, id))
        cursor.close()

    def set_refresh_interval(self, id, interval):

        cursor = self.connection.cursor()
        cursor.execute(Query.SET_REFRESH_INTERVAL, (interval, id))
        cursor.close()

    def set_title(self, id, title):

        cursor = self.connection.cursor()
        cursor.execute(Query.SET_TITLE, (title, id))
        cursor.close()
