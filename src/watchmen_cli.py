import json
from enum import Enum
from os import path
from typing import List

from src.sdk.admin.admin_sdk import search_topics, import_topics, load_topic_list, search_spaces, load_space_list, \
    import_spaces, list_all_pipeline, load_pipeline_by_id, import_pipelines, search_users, search_user_groups


class ModelType(Enum):
    TOPIC = "topic"
    PIPELINE = "pipeline"
    USER = "user"
    USER_GROUP = "user_group"
    SPACE = "space"
    CONNECT_SPACE = "connect_space"
    SUBJECT = "subject"
    REPORT = "report"
    DASHBOARD = "dashboard"


class WatchmenCli(object):
    """
    :authors: imma-team
    :version: 1.0
    """

    def __load_site_json(self):
        data = {}
        if path.exists("temp/site.json"):
            with open('temp/site.json', 'r') as outfile:
                data = json.load(outfile)
                return data
        else:
            return data


    def __search_user(self,site,name):
        users = search_users(site,name)
        for user in users:
            print("user name :{} user id :{}".format(user["name"],user["userId"]))

    def __search_topic(self, site, name):
        results: List = search_topics(site, name)
        for result in results:
            print("topic name :{} , topic_id :{}".format(result["name"], result["topicId"]))
        return results

    def __search_space(self, site, name):
        results: List = search_spaces(site, name)
        for result in results:
            print("topic name :{} , topic_id :{}".format(result["name"], result["spaceId"]))
        return results

    def __search_user_group(self,site,name):
        user_groups =  search_user_groups(site,name)
        for group in user_groups:
            print("group name :{} . group id :{}".format(group["name"],group["userGroupId"]))

    def __search_report(self,site,name):
        pass

    def __search_connect_spac(self,site,name):
        pass


    def __search_subject(self,site,name):
        pass

    

    def __save_to_json(self, data):
        with open('temp/site.json', 'w') as outfile:
            json.dump(data, outfile)

    def __sync_topic(self, source_site, target_site, names):
        topic_list: list = load_topic_list(source_site, names)
        print("find {} topic".format(len(topic_list)))
        import_topics(target_site, topic_list)

    def __sync_space(self, source_site, target_site, names):
        space_list: list = load_space_list(source_site, names)
        print("find {} space".format(len(space_list)))
        import_spaces(target_site, space_list)

    def __sync_user_group(self, source_site, target_site, names):
        pass

    def __sync_user(self, source_site, target_site, names):
        pass

    def __sync_pipeline(self, source_site, target_site, ids):
        pipeline_list =[]
        for id in ids:
            pipeline_list.append(load_pipeline_by_id(source_site,id))
        print("find {} pipeline".format(len(pipeline_list)))
        import_pipelines(target_site,pipeline_list)

    def __sync_connect_spaces(self, source_site, target_site, ids):
        pass

    def __sync_dashboards(self, source_site, target_site, ids):
        pass

    def __sync_subjects(self, source_site, target_site, ids):
        pass

    def __sync_reports(self, source_site, target_site, ids):
        pass

    def __list_pipeline(self, site):
        pipeline_list = list_all_pipeline(site)
        for pipeline in pipeline_list:
            print("pipeline name :{} , pipeline :{}".format(pipeline["name"], pipeline["pipelineId"]))

    def add_site(self, name, host, username=None, password=None):
        """ add_site {site_name} {host_url} {username} {password}
        
        """
        sites = self.__load_site_json()
        sites[name] = {"host": host, "username": username, "password": password}
        self.__save_to_json(sites)

    def search(self, type, site, name):
        """search topic {site_name} {topic_name}
           """
        model_type = ModelType(type)

        switcher_search = {
            ModelType.TOPIC.value: self.__search_topic,
            ModelType.SPACE.value: self.__search_space,
            ModelType.USER.value:self.__search_user,
            ModelType.USER_GROUP.value:self.__search_user_group
        }

        sites = self.__load_site_json()
        switcher_search.get(model_type.value)(sites[site], name)

        # print(self.source)

    def hosts(self):
        print(self.__load_site_json())

    def list(self, type, site):
        model_type = ModelType(type)
        sites = self.__load_site_json()

        switcher_list = {
            ModelType.PIPELINE.value: self.__list_pipeline
        }

        switcher_list.get(type)(sites[site])

    def sync(self, type, source, target, keys=[]):
        """sync topic {source_site_name} {target_site_name} {name_list}=["topic_name"]
                  """

        model_type = ModelType(type)

        sites = self.__load_site_json()

        switcher_sync = {
            ModelType.TOPIC.value: self.__sync_topic,
            ModelType.SPACE.value: self.__sync_space,
            ModelType.USER_GROUP.value: self.__sync_user_group,
            ModelType.PIPELINE.value:self.__sync_pipeline

        }

        switcher_sync.get(model_type.value)(sites[source], sites[target], keys)
