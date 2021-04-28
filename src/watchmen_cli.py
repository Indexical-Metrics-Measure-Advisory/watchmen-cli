import json
from enum import Enum
from os import path

from src.sdk.service.data_search import search_user_group, search_topic, search_space, search_user
from src.sdk.service.data_sync import list_pipeline, sync_pipeline, sync_user, sync_space, sync_user_group, sync_topic


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

    def __search_report(self, site, name):
        pass

    def __search_connect_spac(self, site, name):
        pass

    def __search_subject(self, site, name):
        pass

    def __save_to_json(self, data):
        with open('temp/site.json', 'w') as outfile:
            json.dump(data, outfile)

    def __sync_connect_spaces(self, source_site, target_site, ids):
        pass

    def __sync_dashboards(self, source_site, target_site, ids):
        pass

    def __sync_subjects(self, source_site, target_site, ids):
        pass

    def __sync_reports(self, source_site, target_site, ids):
        pass

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
            ModelType.TOPIC.value: search_topic,
            ModelType.SPACE.value: search_space,
            ModelType.USER.value: search_user,
            ModelType.USER_GROUP.value: search_user_group
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
            ModelType.PIPELINE.value: list_pipeline
        }

        switcher_list.get(type)(sites[site])

    def sync(self, type, source, target, keys=[]):
        """sync topic {source_site_name} {target_site_name} {name_list}=["topic_name"]
                  """

        model_type = ModelType(type)
        sites = self.__load_site_json()
        switcher_sync = {
            ModelType.TOPIC.value: sync_topic,
            ModelType.SPACE.value: sync_space,
            ModelType.USER_GROUP.value: sync_user_group,
            ModelType.PIPELINE.value: sync_pipeline,
            ModelType.USER.value: sync_user
        }

        if target == "file":
            target_site = "file"
        else:
            target_site = sites[target]

        if source == "file":
            source_site = "file"
        else:
            source_site = sites[source]

        switcher_sync.get(model_type.value)(source_site, target_site, keys)

    def import_data(self, data_list, topic_name):
        pass

    def generate_raw_topic(self):
        pass

    def verify_topic(self):
        ## verify topic number

        pass
