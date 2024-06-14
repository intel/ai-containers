# Copyright (c) 2024 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import re
import sys

import pandas as pd
from python_on_whales import DockerException, docker

os_types = ["apt", "yum"]


def extract_deps(deps: dict, version: str, service: str):
    """
    Extracts dependency metadata from labels and requirements.txt files

    Args:
        deps (dict): The dictionary containing the dependency metadata.
        version (str): The version of the compose metadata.
        service (str): The name of the compose service.

    Returns:
        tuple: A tuple containing the os dependencies, python dependencies, and conda dependencies.
    """

    def get_dependency_string(dep_type):
        tmp_deps = {
            k: v
            for k, v in deps.items()
            if f"dependency.{dep_type}" in k and re.match(r"^([^.]*(\.)){2}[^.]*$", k)
        }
        tmp_deps.update(
            {k: v for k, v in deps.items() if f"dependency.{version}.{dep_type}" in k}
        )
        return (
            "\n".join(
                [
                    f"{k.split('.')[-1]} {v}" if v != "true" else f"{k.split('.')[-1]}"
                    for k, v in tmp_deps.items()
                ]
            ).strip("\n")
            if tmp_deps
            else " "
        )

    os_deps = ""
    for os_type in os_types:
        os_deps = os_deps + get_dependency_string(os_type)

    conda_deps = get_dependency_string("conda") if version != "pip" else " "

    if deps.get(f"dependency.{version}.pip") == "false":
        return os_deps, " ", conda_deps

    py_deps = get_dependency_string("pip") if version != "conda" else " "

    service = deps.get("dependency.name", service)
    requirements_file = [
        dep for key, dep in deps.items() if "dependency.python." in key
    ] or [f"{service}-requirements.txt"]
    for file in requirements_file:
        with open(file, "r", encoding="utf-8") as f:
            py_reqs = re.sub(r"\n-(.*)", "", f.read())
            py_reqs = re.sub(r"(.*]?)(\W=)(.*)", r"\1 \3", py_reqs)
            py_reqs = re.sub(r"#(.*)", "", py_reqs)
            py_deps = py_deps + "\n".join(py_reqs.split("\n"))

    return os_deps, py_deps, conda_deps


def compose_to_csv(path: str, name: str):
    """
    Extracts metadata from container group and converts it to a csv file

    Args:
        path (str): The path to the compose metadata and .actions.json file.
        name (str): The name of the csv table.

    Returns:
        None
    """

    def extract_labels(setting: str = None):
        if setting:
            with open(".env", "w", encoding="utf-8") as f:
                f.write(setting)

        try:
            compose_metadata = docker.compose.config(return_json=True)
            if os.path.isfile(".env"):
                os.remove(".env")
        except DockerException as e:
            print(e)
            if os.path.isfile(".env"):
                os.remove(".env")
            sys.exit(1)

        return compose_metadata

    def make_table(setting: str = None, compose_metadata: dict = None):
        df = pd.DataFrame(data={})
        for svc in compose_metadata["services"]:
            if compose_metadata["services"][svc]["build"]["labels"]["docs"] != path:
                continue

            labels = compose_metadata["services"][svc]["build"]["labels"]
            if labels.get(f"dependency.{setting.split('=')[1]}") == "false":
                return pd.DataFrame(data={})

            os_deps, py_deps, conda_deps = extract_deps(
                labels, setting.split("=")[1], svc
            )
            try:
                svc_df = pd.DataFrame(
                    data=[
                        ["Container", labels["org.opencontainers.image.title"]],
                        [
                            "Image Name",
                            labels["org.opencontainers.image.name"]
                            + ":"
                            + labels["org.opencontainers.image.version"],
                        ],
                        ["Base Image Name", labels["org.opencontainers.base.name"]],
                        ["Python Version", labels["dependency.python"]],
                        ["OS Dependencies", os_deps],
                        ["Python Dependencies", py_deps],
                        ["Conda Dependencies", conda_deps],
                    ],
                    columns=[
                        setting.split("=")[0].lower().replace("_", " ").title(),
                        setting.split("=")[1],
                    ],
                )
            except:
                print(f"Failed to insert container metadata for {svc}")
                sys.exit(1)

            df = pd.concat([df, svc_df])

        return df

    root = os.getcwd()
    os.chdir(path)
    with open(".actions.json", "r", encoding="utf-8") as f:
        actions_env = json.loads(f.read())

    actions_env.pop("experimental", None)
    actions_env.pop("runner_label", None)
    actions_env.pop("env_overrides", None)

    df = pd.DataFrame(data={})
    settings = [
        f"{key}={value}" for key, values in actions_env.items() for value in values
    ]

    if name:
        path = name

    if len(settings) > 1:
        for setting in settings:
            metadata = extract_labels(setting)
            df = pd.concat([df, make_table(setting, metadata)], axis=1)
    else:
        metadata = docker.compose.config(return_json=True)
        df = make_table("Name=Version", metadata)

    os.chdir(root)
    df.loc[:, ~df.columns.duplicated()].to_csv(f"docs/assets/{path}.csv", index=False)
