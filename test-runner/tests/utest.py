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

import logging
import os

import pytest
import yaml
from expandvars import expandvars
from hypothesis import given
from hypothesis.strategies import dictionaries, text
from test_runner import get_test_list, parse_args, set_log_filename
from utils.test import Test


@pytest.fixture
def test_args_input():
    "PyTest args input fixture."

    return parse_args(
        [
            "-v",
            "-f",
            "test-runner/tests.yaml",
            "-a",
            "test-runner/.actions.json",
            "-l",
            "output",
        ]
    )


@pytest.fixture
def test_json_input():
    "PyTest json input fixture."
    tests_list = []
    tests_json = []
    with open("test-runner/tests.yaml", "r", encoding="utf-8") as test_file:
        try:
            tests_json = yaml.full_load(test_file)
        except yaml.YAMLError as yaml_exc:
            pytest.raises(yaml_exc)
            for test in tests_json:
                tests_list[test] = tests_json[test]
    return tests_json


@pytest.fixture
def test_class_input():
    "PyTest test input fixture."
    tests_list = []
    tests_json = []
    with open("test-runner/tests.yaml", "r", encoding="utf-8") as test_file:
        try:
            tests_list = yaml.full_load(test_file)
        except yaml.YAMLError as yaml_exc:
            pytest.raises(yaml_exc)
            for test in tests_json:
                tests_list[test] = tests_json[test]
    return [Test(name=test, **tests_list[test]) for test in tests_list]


def test_container_run(test_class_input):
    "Test container_run() method."
    for idx, test in enumerate(test_class_input):
        if hasattr(test, "img") and test.serving is False and idx == 0:
            assert "expandvars" in test.container_run()


def test_container_run_serving(test_class_input):
    "Test container_run() method with serving input."
    for test in test_class_input:
        if hasattr(test, "img") and test.serving is True:
            assert "3.11" in test.container_run()


def test_run(test_class_input):
    "test run() method."
    for test in test_class_input:
        if test.img is None and test.mask == []:
            assert test.run() == "Hello World"


def test_set_log_filename():
    "test set_log_filename() method."
    logging.basicConfig(filename="/tmp/test-runner.log", level=logging.DEBUG)
    set_log_filename(logging.getLogger(), "test", "/tmp")
    logging.info("Unit Test")
    assert logging.getLogger().hasHandlers()
    assert os.path.exists("/tmp/test.log")
    os.remove("/tmp/test.log")


def test_get_path(test_class_input):
    "test get_path() class method."
    assert test_class_input[0].get_path("tox.ini") == os.getcwd() + "/tox.ini"


def test_get_test_list(test_args_input, test_json_input):
    "test get_test_list() method."
    test_val = {
        "test1": {
            "img": "${REGISTRY}/${REPO}:latest",
            "cmd": "head -n 1 /workspace/test-runner/requirements.txt",
            "notebook": True,
            "env": {"REGISTRY": "${REGISTRY}", "DEBUG": "true"},
            "volumes": [
                {"src": "/tf_dataset", "dst": "/tmp"},
                {"src": "$PWD", "dst": "/workspace"},
            ],
        },
        "test2": {
            "cmd": 'echo -n $TEST && python -c \'print(" World", end="")\'',
            "env": {"TEST": "Hello"},
        },
        "test3": {
            "img": "${CACHE_REGISTRY}/cache/library/python:3.10-slim-bullseye",
            "cmd": "python --version",
            "serving": True,
        },
        "test4": {
            "img": f"{expandvars('${CACHE_REGISTRY}')}/cache/library/python:3.11-slim-bullseye",
            "cmd": 'echo "4"',
        },
        "test5": {
            "img": f"{expandvars('${CACHE_REGISTRY}')}/cache/library/python:3.11-slim-bullseye",
            "cmd": 'echo "5"',
        },
        "test6": {
            "img": "${CACHE_REGISTRY}/cache/library/python:3.11-slim-bullseye",
            "cmd": "echo 'hello: world'",
            "mask": ["hello"],
        },
        "test7": {"cmd": "echo 'world: hello'", "mask": ["world"]},
    }

    test_fn = get_test_list(test_args_input, test_json_input)
    assert test_fn == test_val


def test_masking(test_class_input):
    "test masking."
    for test in test_class_input:
        if test.mask != [] and test.img:
            assert ":***" in test.container_run()
        if test.mask != [] and not test.img:
            assert ":***" in test.run()


@given(name=text(), arguments=dictionaries(text(), text()))
def test_fuzz_container_run(name, arguments):
    "Fuzz container_run()."
    try:
        test = Test(name=name, **arguments)
        test.container_run()
    except Exception as e:
        print(f"Caught exception: {e}")


@given(name=text(), arguments=dictionaries(text(), text()))
def test_fuzz_run(name, arguments):
    "Fuzz run()."
    try:
        test = Test(name=name, **arguments)
        test.run()
    except Exception as e:
        print(f"Caught exception: {e}")
