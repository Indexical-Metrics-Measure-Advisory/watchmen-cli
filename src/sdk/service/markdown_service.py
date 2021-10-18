import base64
import json
from os import walk

from src.sdk.admin.admin_sdk import import_pipelines, import_topics
from src.sdk.utils.array_utils import ArrayUtils


def list_asset_markdown(folder):
    _, _, filenames = next(walk(folder))
    asset = []
    for file_name in filenames:
        if file_name.endswith(".md"):
            with open(folder + "/" + file_name, encoding="utf-8") as f:
                data = f.read()
                asset.append(data)
    return asset


def read_data_from_markdown(markdown: str):
    topic_list = []
    pipeline_list = []

    array = ArrayUtils(markdown.split("\n"))
    json_list = array \
        .map(lambda x: x.strip()) \
        .filter(lambda x: x.startswith('<a href="data:application/json;base64,')) \
        .map(lambda x: x.replace('<a href="data:application/json;base64,', '')) \
        .map(lambda x: base64.b64decode(x[0:x.find('"')])) \
        .map(lambda x: json.loads(x))\
        .toList()

    for json_data in json_list:
        if "pipelineId" in json_data:
            pipeline_list.append(json_data)
        elif "topicId" in json_data:
            topic_list.append(json_data)
    return topic_list, pipeline_list


def import_markdowns(folder,site):
    markdown_list = list_asset_markdown(folder)
    for markdown in markdown_list:
        topic_list, pipeline_list = read_data_from_markdown(markdown)
        import_pipelines(site,pipeline_list)
        import_topics(site,topic_list)

