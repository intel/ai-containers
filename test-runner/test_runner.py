# Copyright (c) 2022 Intel Corporation
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
# ============================================================================
#
# This file was assembled from multiple pieces, whose use is documented
# throughout. Please refer to the TensorFlow dockerfiles documentation
# for more information.
# based on https://github.com/pytorch/pytorch/blob/master/Dockerfile
#
# NOTE: To build this you will need a docker version >= 19.03 and DOCKER_BUILDKIT=1
#
#       If you do not use buildkit you are not going to have a good time
#
#       For reference:
#           https://docs.docker.com/develop/develop-images/build_enhancements/

import json
import logging
import os
import re
import sys
from argparse import ArgumentParser
from shutil import rmtree
from typing import List

# Third Party
from expandvars import expandvars
from python_on_whales import DockerException, docker
from tabulate import tabulate
from utils.test import PerfException, Test
from yaml import YAMLError, full_load


def parse_args(args: list):
    """Parse command line arguments.

    Args:
        args (list(str)): user input parameters

    Returns:
        dict: command line arguments
    """
    parser = ArgumentParser()
    parser.add_argument(
        "-a", "--actions-file", dest="actions_path", help="-a /path/to/.actions.json"
    )
    parser.add_argument(
        "-f", "--file", dest="file_path", help="-f /path/to/tests.yaml", required=True
    )
    parser.add_argument(
        "-v", "--verbose", dest="log_level", action="store_true", help="DEBUG Loglevel"
    )
    parser.add_argument(
        "-l", "--logs", dest="logs_path", default="output", help="-l /path/to/logs"
    )

    return parser.parse_args(args)


def set_log_filename(logger: logging.Logger, name: str, logs_path: str):
    """Swap the current logger filename to another filename.

    Args:
        logger (logging.Logger): logger context
        name (str): name of the new log filename
        logs_path (str): path to the new log filename
    """
    unique_identifier = logs_path.split('/')[0] #name of the tests directory (ie. python, python1 )
    test_handler = logging.FileHandler(f"{logs_path}/{unique_identifier}-{name}.log")
    try:
        [prev_handler] = [
            handler
            for handler in logger.handlers
            if isinstance(handler, logging.FileHandler)
        ]
        test_handler.setFormatter(prev_handler.formatter)
        test_handler.setLevel(prev_handler.level)
        logger.removeHandler(prev_handler)
    except:
        test_handler.setFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        test_handler.setLevel(logging.INFO)
    logger.addHandler(test_handler)


def get_test_list(args: dict, tests_yaml: List[dict]):
    """Parse tests from yaml file and expand them if necessary.

    Args:
        args (dict): command line arguments
        tests_yaml (List[dict]): list of tests imported from a yaml file

    Returns:
        List[dict]: list of expanded tests
    """
    tests_list = {}
    disable_masking = False
    for test in tests_yaml:
        if re.search(r"\$\{([A-Za-z0-9_]*)\:\-(.*?)\}", test):
            if args.actions_path:
                with open(args.actions_path, "r", encoding="utf-8") as actions_file:
                    for key, dval in json.load(actions_file).items():
                        if key == "mask" and dval == [False]:
                            disable_masking = True
                        if isinstance(dval, list) and key != "experimental":
                            for _, val in enumerate(dval):
                                os.environ[key] = str(val)
                                if expandvars(test) not in tests_yaml.keys():
                                    tests_list[expandvars(test)] = {
                                        k: (expandvars(v) if isinstance(v, str) else v)
                                        for k, v in tests_yaml[test].items()
                                    }
                                del os.environ[key]
            else:
                if expandvars(test) not in tests_yaml.keys():
                    tests_list[expandvars(test)] = {
                        k: expandvars(v) if isinstance(v, str) else v
                        for k, v in tests_yaml[test].items()
                    }
        else:
            tests_list[test] = dict(tests_yaml[test].items())
        # Check that each test contains 'cmd' and is therefore a valid test
        if "cmd" not in tests_yaml[test]:
            logging.error("Command not found for %s", test)
            sys.exit(1)

    return tests_list, disable_masking


if __name__ == "__main__":
    # Parse CLI Args
    args = parse_args(sys.argv[1:])
    # Verify Logfile Handler Paths
    if not os.path.exists(args.logs_path):
        os.makedirs(args.logs_path)
    else:
        rmtree(args.logs_path)
        os.makedirs(args.logs_path)
    # Set up Logging for test-runner context
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f"{args.logs_path}/test-runner.log"),
        ],
    )
    # Set Debug if -v
    if args.log_level:
        logging.getLogger().setLevel("DEBUG")
        os.environ["PYTHON_ON_WHALES_DEBUG"] = "1"
    logging.debug("Reading Test File")
    with open(args.file_path, "r", encoding="utf-8") as test_file:
        try:
            tests_json = full_load(test_file)
        except YAMLError as yaml_exc:
            logging.error(yaml_exc)
            sys.exit(1)
    tests_list, disable_masking = get_test_list(args, tests_json)
    logging.debug("Creating Test Objects from: %s", tests_list)
    # For each test, create a Test Object with the test name is the key of the test in yaml
    tests = [Test(name=test, **tests_list[test]) for test in tests_list]
    logging.info("Setup Completed - Running Tests")
    summary = []
    ERROR = False
    for idx, test in enumerate(tests):
        if disable_masking:
            test.mask = []
        # Set Context to test-runner.log
        set_log_filename(logging.getLogger(), "test-runner", args.logs_path)
        logging.info("Running Test: %s", test.name)
        # Switch logging context to test filename
        set_log_filename(logging.getLogger(), test.name, args.logs_path)
        logging.debug("Attrs: %s", dir(test)[26:])
        # If 'img' is present in the test, ensure that the test is a container run, otherwise run on baremetal
        # returns the stdout of the test and the RETURNCODE
        try:  # Try for Runtime Failure Conditions
            log = test.container_run() if test.img else test.run()
        except (DockerException, PerfException, YAMLError) as err:
            logging.error(err)
            summary.append([idx + 1, test.name, "FAIL"])
            ERROR = True
            continue
        except KeyboardInterrupt:
            summary.append([idx + 1, test.name, "FAIL"])
            ERROR = True
            break
        summary.append([idx + 1, test.name, "PASS"])
    # Switch logging context back to the initial state
    set_log_filename(logging.getLogger(), "test-runner", args.logs_path)
    # Remove remaining containers
    test_images = [expandvars(test.img) for test in tests if test.img]
    if test_images:
        remaining_containers = docker.container.list()
        for container in remaining_containers:
            docker.stop(container, time=None)
        docker.image.remove(test_images, force=True, prune=False)
        docker.system.prune()
        logging.info("%d Images Removed", len(test_images))
    # Print Summary Table
    logging.info(
        "\n%s", tabulate(summary, headers=["#", "Test", "Status"], tablefmt="orgtbl")
    )
    if ERROR:
        sys.exit(1)
