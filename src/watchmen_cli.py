import json
from enum import Enum
from os import path

import requests

from src.sdk.common.common_sdk import test_url
from src.sdk.constants import FILE
from src.sdk.service.data_search import search_user_group, search_topic, search_space, search_user
from src.sdk.service.data_sync import list_pipeline, sync_pipeline, sync_user, sync_space, sync_user_group, sync_topic
from src.sdk.service.markdown_service import import_markdowns, import_markdowns_v2
from src.sdk.utils.file_service import load_folder, create_folder, load_file_to_json, create_file

IMPORT = "import"
GENERATE = "generate"
COMBINE = "combine"


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


def get_access_token(host, username, password):
    login_data = {"username": username, "password": password, "grant_type": "password"}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(host + "/login/access-token", data=login_data,
                             headers=headers)
    token = response.json()["access_token"]
    return token


def import_topics_to_env(token, host, topics):
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
    for topic in topics:
        response = requests.post(host + "/import/admin/topic", data=json.dumps(topic),
                                 headers=headers)
        if response.status_code == 200:
            print("import topic {0} successfully".format(topic['name']))
        else:
            print("import topic {0} failed".format(topic['name']))


def import_pipelines_to_env(token, host, pipelines):
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
    for pipeline in pipelines:
        response = requests.post(host + "/import/admin/pipeline", data=json.dumps(pipeline),
                                 headers=headers)
        if response.status_code == 200:
            print("import pipeline {0} successfully".format(pipeline['name']))
        else:
            print("import pipeline {0} failed".format(pipeline['name']))


class WatchmenCli(object):
    """
    :authors: imma-team
    :version: 1.0
    """

    def __load_site_json(self):
        data = {}
        if path.exists("site/site.json"):
            with open('site/site.json', 'r') as outfile:
                data = json.load(outfile)
                return data
        else:
            return data

    def __test_url(self, url):
        response = test_url(url)
        print(response.status_code)
        print(response.text)

    def __save_to_json(self, data):
        with open('temp/site.json', 'w') as outfile:
            json.dump(data, outfile)

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

    def asset(self, folder, site=None, import_type=None, markdown_file=None):
        sites = self.__load_site_json()
        import_markdowns(folder, sites[site], import_type, markdown_file)

    def test(self, url):
        self.__test_url(url)

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
        # print(keys)
        model_type = ModelType(type)
        sites = self.__load_site_json()
        switcher_sync = {
            ModelType.TOPIC.value: sync_topic,
            ModelType.SPACE.value: sync_space,
            ModelType.USER_GROUP.value: sync_user_group,
            ModelType.PIPELINE.value: sync_pipeline,
            ModelType.USER.value: sync_user

        }

        if target == FILE:
            target_site = FILE
        else:
            target_site = sites[target]

        if source == FILE:
            source_site = FILE
        else:
            source_site = sites[source]

        switcher_sync.get(model_type.value)(source_site, target_site, keys)

    def raw(self, type, path):
        if type == COMBINE:
            root_folder = load_folder(path)
            for folder in root_folder.iterdir():
                if folder.is_dir():
                    instance_path = str(folder.resolve())+"_instance"
                    instance_list = []
                    create_folder(instance_path)
                    for p in folder.iterdir():
                        if p.is_file():
                           json =  load_file_to_json(p)
                           instance_list.append(json)
                    create_file(instance_path,folder.name+"-instance.json",instance_list)
            print("all instances are created")
        else:
            raise KeyError("type is not supported {0}".format(type))

    def verify_topic(self):
        ## verify topic number
        pass

    def deploy(self, host: str, username: str, password: str):
        self.deploy_topics(host, username, password)
        self.deploy_pipelines(host, username, password)

    def deploy_topics(self, host: str, username: str, password: str):
        try:
            token = get_access_token(host, username, password)
            print("import topics first")
            with open("/app/config/topic/" + "topic.json", "r") as src:
                topics = json.load(src)
                import_topics_to_env(token, host, topics)
        except Exception as err:
            raise err

    def deploy_pipelines(self, host: str, username: str, password: str):
        try:
            token = get_access_token(host, username, password)
            print("import pipelines")
            with open("/app/config/pipeline/" + "pipeline.json", "r") as src:
                pipelines = json.load(src)
                import_pipelines_to_env(token, host, pipelines)
        except Exception as err:
            raise err

    def deploy_template(self, host: str, username: str, password: str):
        ## import template space
        ## import template subject
        ## import template chart

        pass

    def deploy_asset(self, host: str, username: str, password: str):
        try:
            token = get_access_token(host, username, password)
            print("import md asset")
            print(token)
            import_markdowns_v2(host, token, "replace")
        except Exception as err:
            raise err

