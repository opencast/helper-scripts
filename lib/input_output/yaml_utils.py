import yaml
import json


def read_yaml_file(path):
    """
    reads a .yaml file and returns a dictionary
    :param path: path to the yaml file
    :return: returns a dictionary
    """
    with open(path, 'r') as f:
        content = yaml.load(f, Loader=yaml.FullLoader)

    return content


def create_yaml_file_from_json_file(json_file_path, yaml_file_path='test.yaml'):
    """
    This function can be used to transform a json file to a yaml file.
    requires import json and import yaml
    :param json_file_path: path to json file
    :param yaml_file_path: path to yaml file (will be created if it does not exist)
    :return:
    """

    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
    with open(yaml_file_path, 'w') as file:
        yaml.dump(json_data, file, sort_keys=False)

    return True
