#! /usr/bin/env python3
"""
parmlibbuild -
Build a parmlib member from a YAML file and a JINJA map
"""

from jinja2 import Environment, FileSystemLoader
import argparse
import datetime
import yaml
from zoautil_py import datasets
from zoautil_py.exceptions import DatasetWriteException


def get_data(yaml_file_name: str) -> dict:
    # Get the user info from yaml
    with open(yaml_file_name, "r", encoding="ISO8859-1") as data_file:
        member_data = yaml.load(data_file, Loader=yaml.FullLoader)
    return member_data


def create_output(template_file_name: str, yaml_file_name: str) -> list:
    input_data = get_data(yaml_file_name)
    environment = Environment(loader=FileSystemLoader("./"))
    template = environment.get_template(template_file_name)
    template.globals["now"] = datetime.datetime.now(datetime.UTC)
    template.globals["source_file"] = yaml_file_name
    return template.render(input_data)


def main():
    parser = argparse.ArgumentParser(
        prog="parmlibbuild.py",
        description="Build a parmlib member from a YAML file and a template",
        epilog="All arguments are required except --dataset",
    )
    parser.add_argument(
        "-t", "--template", help="The template used to build the member", required=True
    )
    parser.add_argument(
        "-y", "--yaml", help="The YAML file containing the data", required=True
    )
    parser.add_argument(
        "-m", "--member", help="The member being created", required=True
    )
    parser.add_argument(
        "-d",
        "--dataset",
        default="SYS1.PARMLIB",
        help="The Parmlib dataset (default is SYS1.PARMLIB)",
    )

    arguments = parser.parse_args()
    print(f"YAML file is: {arguments.yaml}")
    print(f"Template: {arguments.template}")
    print(f"Dataset: {arguments.dataset}")
    print(f"Member: {arguments.member}")
    output = create_output(arguments.template, arguments.yaml)
    with open(arguments.member,"w") as output_file:
        output_file.write(output)



if __name__ == "__main__":
    main()
