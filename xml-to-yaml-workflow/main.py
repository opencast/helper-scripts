import xml.etree.ElementTree as ElementTree
from argparse import ArgumentParser

import os
import re
import sys
import yaml


class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)


def main():
    parser = ArgumentParser()

    parser.add_argument('-i', '--input', type=str, dest='inputFile', required=False,
                        help='Path to the XML Workflow.')

    parser.add_argument('-o', '--output', type=str, dest='outputFile', required=False,
                        help='The path to the output yaml file.')

    args = parser.parse_args()

    if args.inputFile is None and args.outputFile is None:
        for file in os.listdir(sys.path[0]):
            if file.endswith(".xml"):
                translate_file(file, os.path.splitext(file)[0] + ".yaml")
    else:
        translate_file(args.inputFile, args.outputFile)


def translate_file(input_file, output_file):
    tree = ElementTree.parse(input_file)
    root = tree.getroot()

    yaml_data = dict()

    data_id = root.find('{http://workflow.opencastproject.org}id')
    if data_id is not None and data_id.text is not None: yaml_data['id'] = data_id.text

    data_title = root.find('{http://workflow.opencastproject.org}title')
    if data_title is not None and data_title.text is not None: yaml_data['title'] = data_title.text

    data_tags = root.find('{http://workflow.opencastproject.org}tags')
    if data_tags is not None: yaml_data['tags'] = [child.text for child in data_tags]

    data_displayOrder = root.find('{http://workflow.opencastproject.org}displayOrder')
    if data_displayOrder is not None and data_displayOrder.text is not None: yaml_data[
        'displayOrder'] = data_displayOrder.text

    data_description = root.find('{http://workflow.opencastproject.org}description')
    if data_description is not None and data_description.text is not None:
        yaml_data['description'] = re.sub('\\n *', "", data_description.text)

    data_configuration_panel = root.find('{http://workflow.opencastproject.org}configuration_panel')
    if data_configuration_panel is not None and data_configuration_panel.text is not None: yaml_data[
        'configuration_panel'] = re.sub('\\n *', "", data_configuration_panel.text)

    data_operations = root.find('{http://workflow.opencastproject.org}operations')
    if data_operations is not None:
        yaml_data['operations'] = []
        for operation in data_operations:
            data_operation = dict()

            if 'id' in operation.attrib:
                data_operation['id'] = operation.attrib['id']
            if 'if' in operation.attrib:
                data_operation['if'] = operation.attrib['if']
            if 'retry-strategy' in operation.attrib:
                data_operation['retry-strategy'] = operation.attrib['retry-strategy']
            if 'max-attempts' in operation.attrib:
                data_operation['max-attempts'] = operation.attrib['max-attempts']
            if 'if' in operation.attrib:
                data_operation['if'] = operation.attrib['if']
            if 'fail-on-error' in operation.attrib:
                if operation.attrib['fail-on-error'] == 'true':
                    data_operation['fail-on-error'] = True
                else:
                    data_operation['fail-on-error'] = False
            if 'exception-handler-workflow' in operation.attrib:
                data_operation['exception-handler-workflow'] = operation.attrib['exception-handler-workflow']
            if 'description' in operation.attrib:
                data_operation['description'] = operation.attrib['description']

            data_operation['configurations'] = []
            for configurations in operation:
                for configuration in configurations:
                    if configuration.text == 'true':
                        data_operation['configurations'].append({configuration.attrib['key']: True})
                    elif configuration.text == 'false':
                        data_operation['configurations'].append({configuration.attrib['key']: False})
                    else:
                        data_operation['configurations'].append({configuration.attrib['key']: configuration.text})

            yaml_data['operations'].append(data_operation)

    data_statemappings = root.find('{http://workflow.opencastproject.org}state-mappings')

    if data_statemappings is not None:
        yaml_data['state-mappings'] = []
        for statemapping in data_statemappings:
            yaml_data['state-mappings'].append({'state': statemapping.attrib['state'], 'value': statemapping.text})

    stream = open(output_file, 'w')
    yaml.dump(yaml_data, stream, sort_keys=False, Dumper=Dumper, explicit_start=True)

    print("Successful dumped " + input_file + " workflow file to " + output_file)


if __name__ == "__main__":
    main()
