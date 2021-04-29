from typing import List

from src.sdk.admin.admin_sdk import search_spaces, search_topics, search_users, search_user_groups


def search_user(self, site, name):
    users = search_users(site, name)
    for user in users:
        print("user name :{} user id :{}".format(user["name"], user["userId"]))


def search_topic(self, site, name):
    results: List = search_topics(site, name)
    for result in results:
        print("topic name :{} , topic_id :{}".format(result["name"], result["topicId"]))
    return results


def search_space(self, site, name):
    results: List = search_spaces(site, name)
    for result in results:
        print("space name :{} , space_id :{}".format(result["name"], result["spaceId"]))
    return results


def search_user_group(self, site, name):
    user_groups = search_user_groups(site, name)
    for group in user_groups:
        print("group name :{} . group id :{}".format(group["name"], group["userGroupId"]))


def __search_report(self, site, name):
    pass


def __search_connect_spac(self, site, name):
    pass


def __search_subject(self, site, name):
    pass
