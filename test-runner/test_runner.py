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
from shlex import split
from shutil import rmtree
from signal import SIGKILL
from subprocess import PIPE, Popen

# Third Party
from expandvars import expandvars
from python_on_whales import DockerException, docker
from tabulate import tabulate
from yaml import YAMLError, full_load


class Test:
    """A class to represent a test, attributes are set dynamically via yaml config during __init__

    Methods:
        get_path(name=""):
            Given a filename, find that file from the users current working directory
        container_run():
            Use Python on Whales to run a Docker Container with img and cmd
        run():
            Create a process for cmd on Baremetal System
    """

    def __init__(self, name, arguments):
        """Initialize Test Object

        Args:
            name (string): Test name based on the key of the config's dictionary arguments
            arguments (dict): Given a test from a yaml config file, arguments is a dictionary of
                              those configs with the same yaml structure
        """
        self.name = name
        for key, val in arguments.items():
            if isinstance(val, dict) and key == "volumes":
                setattr(self, key, val[key])
            else:
                setattr(self, key, val)

    def get_path(self, name):
        """Given a filename, find that file from the users current working directory

        Args:
            name (string): Filename

        Returns:
            string: Path to filename of input name
        """
        for root, _, files in os.walk(os.getcwd()):
            if name in files:
                return os.path.join(root, name)
        logging.error("Notebook Dockerfile not found")
        sys.exit(1)

    def container_run(self):
        """Use Python on Whales to run a Docker Container with img and cmd

        Returns:
            string: Concatenated streamed stdout and stderr output from subprocess
            int: Exit code
        """
        # Define each volume as (src, dst) for a list of volumes
        volumes = (
            [(expandvars(vol["src"]), expandvars(vol["dst"])) for vol in self.volumes]
            if hasattr(self, "volumes")
            else []
        )
        # Define each env as {key: value} for a dict of envs
        env = (
            {key: expandvars(val) for key, val in self.env.items()}
            if hasattr(self, "env")
            else {}
        )
        default_env = {
            "http_proxy": os.environ.get("http_proxy"),
            "https_proxy": os.environ.get("https_proxy"),
            "no_proxy": os.environ.get("no_proxy"),
        }
        img = expandvars(self.img)
        # Always add proxies to the envs list
        env.update(default_env)
        # If Notebook modify image to include papermill
        if hasattr(self, "notebook"):
            if self.notebook == "true":
                try:  # Try for Docker CLI Failure Conditions
                    docker.run(img, ["which", "papermill"])
                except DockerException as papermill_not_found:
                    logging.error("Papermill not found: %s", papermill_not_found)
                    docker.build(
                        # context path
                        ".",
                        # Image Input and Proxy Args
                        build_args={
                            "BASE_IMAGE_NAME": img.split(":")[0],
                            "BASE_IMAGE_TAG": img.split(":")[1],
                            "http_proxy": os.environ.get("http_proxy"),
                            "https_proxy": os.environ.get("https_proxy"),
                        },
                        # Input File
                        file=self.get_path("Dockerfile.notebook"),
                        # Output Tag = Input Tag
                        tags=[img],
                    )
        if hasattr(self, "serving"):
            if self.serving == "true":
                log = ""
                serving_container = docker.run(
                    # Image
                    img,
                    # Stream Logs
                    detach=True,
                    # Envs
                    envs=env,
                    # Volumes
                    volumes=volumes,
                    # Networks
                    networks=["host"],
                    # Misc
                    cap_add=[
                        self.cap_add if hasattr(self, "cap_add") else "AUDIT_READ"
                    ],
                    devices=[
                        (
                            expandvars(self.device)
                            if hasattr(self, "device")
                            else "/dev/dri"
                        )
                    ],
                    entrypoint=(
                        expandvars(self.entrypoint)
                        if hasattr(self, "entrypoint")
                        else None
                    ),
                    hostname=self.hostname if hasattr(self, "hostname") else None,
                    ipc=self.ipc if hasattr(self, "ipc") else None,
                    privileged=(
                        self.privileged if hasattr(self, "privileged") else True
                    ),
                    pull=self.pull if hasattr(self, "pull") else "missing",
                    shm_size=self.shm_size if hasattr(self, "shm_size") else None,
                )
                client_output = docker.run(
                    # Image
                    "python:3.11-slim-bullseye",
                    # Command
                    split(expandvars(self.cmd)),
                    # Stream Logs
                    stream=True,
                    # Envs
                    envs=env,
                    # Volumes
                    volumes=volumes,
                    # Networks
                    networks=["host"],
                    # Misc
                    cap_add=[
                        self.cap_add if hasattr(self, "cap_add") else "AUDIT_READ"
                    ],
                    devices=[
                        (
                            expandvars(self.device)
                            if hasattr(self, "device")
                            else "/dev/dri"
                        )
                    ],
                    entrypoint=(
                        expandvars(self.entrypoint)
                        if hasattr(self, "entrypoint")
                        else None
                    ),
                    hostname=self.hostname if hasattr(self, "hostname") else None,
                    ipc=self.ipc if hasattr(self, "ipc") else None,
                    privileged=(
                        self.privileged if hasattr(self, "privileged") else True
                    ),
                    pull=self.pull if hasattr(self, "pull") else "missing",
                    remove=self.rm if hasattr(self, "rm") else True,
                    user=self.user if hasattr(self, "user") else None,
                    shm_size=self.shm_size if hasattr(self, "shm_size") else None,
                    workdir=(
                        expandvars(self.workdir) if hasattr(self, "workdir") else None
                    ),
                )
                # Log within the function to retain scope for debugging
                for _, stream_content in client_output:
                    # All process logs will have the stream_type of stderr despite it being stdout
                    logging.info(stream_content.decode("utf-8").strip())
                    log += stream_content.decode("utf-8").strip()
                logging.debug("--- Server Logs ---")
                logging.debug(docker.logs(serving_container))
                docker.stop(serving_container, time=None)
                return log
        # Try for Docker CLI Failure Conditions
        # https://gabrieldemarmiesse.github.io/python-on-whales/sub-commands/container/#python_on_whales.components.container.cli_wrapper.ContainerCLI.run
        output_generator = docker.run(
            # Image
            img,
            # Command
            split(expandvars(self.cmd)),
            # Stream Logs
            stream=True,
            # Envs
            envs=env,
            # Volumes
            volumes=volumes,
            # Misc
            cap_add=[self.cap_add if hasattr(self, "cap_add") else "AUDIT_READ"],
            devices=[
                expandvars(self.device) if hasattr(self, "device") else "/dev/dri"
            ],
            entrypoint=(
                expandvars(self.entrypoint) if hasattr(self, "entrypoint") else None
            ),
            groups_add=[
                (expandvars(self.groups_add) if hasattr(self, "group-add") else "109"),
                "44",
            ],
            hostname=self.hostname if hasattr(self, "hostname") else None,
            ipc=self.ipc if hasattr(self, "ipc") else None,
            privileged=self.privileged if hasattr(self, "privileged") else True,
            pull=self.pull if hasattr(self, "pull") else "missing",
            remove=self.rm if hasattr(self, "rm") else True,
            user=self.user if hasattr(self, "user") else None,
            shm_size=self.shm_size if hasattr(self, "shm_size") else None,
            workdir=expandvars(self.workdir) if hasattr(self, "workdir") else None,
        )
        # Log within the function to retain scope for debugging
        log = ""
        for _, stream_content in output_generator:
            # All process logs will have the stream_type of stderr despite it being stdout
            logging.info(stream_content.decode("utf-8").strip())
            log += stream_content.decode("utf-8").strip()
        return log

    def run(self):
        """Create a process for cmd on Baremetal System

        Returns:
            string: Concatenated streamed stdout and stderr output from subprocess
            int: Exit code
        """
        # Define each env as {key: value} for a dict of envs
        env = (
            {key: expandvars(val) for key, val in self.env.items()}
            if hasattr(self, "env")
            else {}
        )
        # Add host env to config envs
        env.update(os.environ.copy())
        logging.debug("Env: %s", env)
        logging.info("%s Started", self.name)
        p = Popen(
            self.cmd,
            stdout=PIPE,
            stderr=PIPE,
            env=env,
            shell=True,
        )
        try:
            stdout, stderr = p.communicate()
            if stderr:
                logging.error(stderr.decode("utf-8"))
            if stdout:
                logging.info("Test Output: %s", stdout.decode("utf-8"))
            return stdout.decode("utf-8")
        except KeyboardInterrupt:
            os.killpg(os.getpgid(p.pid), SIGKILL)
            raise KeyboardInterrupt


def parse_args():
    """Use argparse to parse command line arguments

    Returns:
        dict: Parsed command line arguments
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

    return parser.parse_args()


def set_log_filename(logger, name, logs_path):
    """Change filehandler file name in current logger context

    Args:
        logger (logging.RootLogger): Current logger context
        name (string): New or Existing logger filename
        logs_path (string): Path to logs folder
    """
    test_handler = logging.FileHandler(f"{logs_path}/{name}.log")
    # Handler[0] is the stream output to stdout/stderr
    # Handler[1] is always the file handler, see the logging declaration handlers parameter
    test_handler.setFormatter(logger.handlers[1].formatter)
    test_handler.setLevel(logger.handlers[1].level)
    logger.removeHandler(logger.handlers[1])
    logger.addHandler(test_handler)


if __name__ == "__main__":
    # Parse CLI Args
    args = parse_args()
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
    tests_list = {}
    for test in tests_json:
        if re.search(r"\$\{([A-Za-z0-9_]*)\:\-(.*?)\}", test):
            if args.actions_path:
                with open(args.actions_path, "r", encoding="utf-8") as actions_file:
                    for key, dval in json.load(actions_file).items():
                        if isinstance(dval, list) and key != "experimental":
                            for _, val in enumerate(dval):
                                os.environ[key] = str(val)
                                if expandvars(test) not in tests_json.keys():
                                    tests_list[expandvars(test)] = {
                                        k: (
                                            expandvars(v)
                                            if isinstance(v, str)
                                            else {k: v}
                                        )
                                        for k, v in tests_json[test].items()
                                    }
                                del os.environ[key]
            else:
                if expandvars(test) not in tests_json.keys():
                    tests_list[expandvars(test)] = {
                        key: expandvars(val) if isinstance(val, str) else {key: val}
                        for key, val in tests_json[test].items()
                    }
        else:
            tests_list[test] = dict(tests_json[test].items())
        # Check that each test contains 'cmd' and is therefore a valid test
        if "cmd" not in tests_json[test]:
            logging.error("Command not found for %s", test)
            sys.exit(1)
    logging.debug("Creating Test Objects from: %s", tests_list)
    # For each test, create a Test Object with the test name is the key of the test in yaml
    tests = [Test(test, tests_list[test]) for test in tests_list]
    logging.info("Setup Completed - Running Tests")
    summary = []
    ERROR = False
    for idx, test in enumerate(tests):
        # Set Context to test-runner.log
        set_log_filename(logging.getLogger(), "test-runner", args.logs_path)
        logging.info("Running Test: %s", test.name)
        # Switch logging context to test filename
        set_log_filename(logging.getLogger(), test.name, args.logs_path)
        logging.debug("Attrs: %s", dir(test)[26:])
        # If 'img' is present in the test, ensure that the test is a container run, otherwise run on baremetal
        # returns the stdout of the test and the RETURNCODE
        try:  # Try for Runtime Failure Conditions
            log = test.container_run() if hasattr(test, "img") else test.run()
        except DockerException as err:
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
    remaining_containers = docker.container.list()
    for container in remaining_containers:
        docker.stop(container, time=None)
    # Print Summary Table
    logging.info(
        "\n%s", tabulate(summary, headers=["#", "Test", "Status"], tablefmt="orgtbl")
    )
    if ERROR:
        sys.exit(1)
