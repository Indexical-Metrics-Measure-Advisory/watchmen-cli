import json
import os
import pathlib


def __get_path(site_name,model_name):
    path = "./temp/" + model_name + "/" + site_name
    return path


def save_to_file(site_name,data_list,model_name):
    path = __get_path(site_name,model_name)
    os.makedirs(path, exist_ok=True)
    with open(path+"/"+model_name+".json", 'w') as outfile:
        json.dump(data_list, outfile)


def load_from_file(site_name,model_name):
    path = __get_path(site_name, model_name)
    with open(path+"/"+model_name+".json","r") as outfile:
        return json.load(outfile)


def create_file(path,file_name,data_list):
    with open(path + "/" + file_name + ".json", 'w') as outfile:
        json.dump(data_list, outfile)


def load_file_to_json(file):
    with open(file, "r") as outfile:
        return json.load(outfile)


def load_folder(folder_path):
    return pathlib.Path(folder_path)


def create_folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)






