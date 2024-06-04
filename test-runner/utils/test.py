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
import re
import sys
from shlex import split
from signal import SIGKILL
from subprocess import PIPE, Popen
from typing import Dict, List, Optional

import pint
from expandvars import expandvars
from pydantic import BaseModel
from python_on_whales import DockerException, docker
from yaml import YAMLError, full_load

units = pint.UnitRegistry()


class PerfException(Exception):
    "Constructs a PerfException class."


class Threshold(BaseModel):
    "Constructs a Threshold class."
    name: str
    modelName: str
    boundary: float
    lower_is_better: bool
    unit: str


class Volume(BaseModel):
    "Constructs a Volume class."
    src: str
    dst: str


class Test(BaseModel):
    "Runs the test command."
    __test__ = False
    name: str
    cmd: str
    img: Optional[str] = None
    volumes: Optional[List[Volume]] = None
    env: Optional[Dict[str, str]] = None
    mask: Optional[List[str]] = []
    notebook: Optional[bool] = False
    serving: Optional[bool] = False
    cap_add: Optional[str] = "AUDIT_READ"
    device: Optional[str] = "/dev/dri"
    entrypoint: Optional[str] = ""
    groups_add: Optional[List[str]] = ["109", "44"]
    hostname: Optional[str] = None
    ipc: Optional[str] = None
    performance: Optional[str] = None
    privileged: Optional[bool] = False
    pull: Optional[str] = "missing"
    user: Optional[str] = None
    shm_size: Optional[str] = None
    workdir: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.performance:
            perf_repo = os.environ.get("PERF_REPO")
            if perf_repo:
                os.system(
                    f"git clone https://github.com/{perf_repo} models-perf > /dev/null 2>&1"
                )
            else:
                logging.error(
                    "Performance mode enabled, but PERF_REPO environment variable not set"
                )
            units.load_definitions("./models-perf/definitions.txt")

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

    def serving_run(self, img: str, env: dict, volumes: Volume):
        """Runs the Docker container in a client/server configuration and returns the log.

        Args:
            img (str): server image
            env (dict): environment variables
            volumes (Volume): container volumes

        Returns:
            str: client output log
        """
        # Always add proxies to the envs list
        log = ""
        with docker.run(
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
            cap_add=[self.cap_add],
            devices=[expandvars(self.device, nounset=True)],
            entrypoint=(
                expandvars(self.entrypoint, nounset=True) if self.entrypoint else None
            ),
            hostname=self.hostname,
            ipc=self.ipc,
            privileged=self.privileged,
            pull=self.pull,
            shm_size=self.shm_size,
        ) as serving_container:
            client_output = docker.run(
                # Image
                expandvars("${CACHE_REGISTRY}/cache/library/python:3.11-slim-bullseye"),
                # Command
                split(expandvars(self.cmd, nounset=True)),
                # Stream Logs
                stream=True,
                # Envs
                envs=env,
                # Volumes
                volumes=volumes,
                # Networks
                networks=["host"],
                # Misc
                cap_add=[self.cap_add],
                devices=[expandvars(self.device, nounset=True)],
                hostname=self.hostname,
                ipc=self.ipc,
                privileged=self.privileged,
                pull=self.pull,
                remove=True,
                user=self.user,
                shm_size=self.shm_size,
                workdir=(
                    expandvars(self.workdir, nounset=True) if self.workdir else None
                ),
            )
            # Log within the function to retain scope for debugging
            for _, stream_content in client_output:
                # All process logs will have the stream_type of stderr despite it being stdout
                logging.info(stream_content.decode("utf-8").strip())
                log += stream_content.decode("utf-8").strip()
            logging.debug("--- Server Logs ---")
            logging.debug(docker.logs(serving_container))

        return log

    def notebook_run(self, img: str):
        """Runs a notebook using a jupyter notebook and papermill.

        Args:
            img (str): docker image
        """
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
                # load into current images context
                load=True,
            )

    def check_perf(self, content):
        """
        Check the performance of the test against the thresholds.

        Args:
            content (str): test output log

        Raises:
            PerfException: if the performance does not meet the target performance
        """
        with open(
            f"models-perf/{self.performance.split(':')[0]}", "r", encoding="utf-8"
        ) as file:
            try:
                thresholds = full_load(file)
            except YAMLError as yaml_exc:
                raise YAMLError(yaml_exc)
        model_thresholds = [
            threshold
            for threshold in thresholds
            if self.performance.split(":")[1] == threshold["modelName"]
        ]
        for threshold in model_thresholds:
            perf = re.search(
                rf"{threshold['key']}[:]?\s+(.\d+[\s]?.*)",
                content,
                re.IGNORECASE,
            )
            if perf:
                if threshold["lower_is_better"]:
                    if units.Quantity(perf.group(1)) > units.Quantity(
                        f"{threshold['boundary']} {threshold['unit']}"
                    ):
                        raise PerfException(
                            f"Performance Threshold {threshold['name']} did not meet the target performance."
                        )
                else:
                    if units.Quantity(perf.group(1)) < units.Quantity(
                        f"{threshold['boundary']} {threshold['unit']}"
                    ):
                        raise PerfException(
                            f"Performance Threshold {threshold['name']} did not meet the target performance."
                        )

    def container_run(self):
        """Runs the docker container.

        Returns:
            str: container output log
        """
        # Define each volume as (src, dst) for a list of volumes
        volumes = (
            [(expandvars(vol.src), expandvars(vol.dst)) for vol in self.volumes]
            if self.volumes
            else []
        )
        # Define each env as {key: value} for a dict of envs
        env = (
            {key: expandvars(val) for key, val in self.env.items()} if self.env else {}
        )
        default_env = {
            "http_proxy": os.environ.get("http_proxy"),
            "https_proxy": os.environ.get("https_proxy"),
            "no_proxy": os.environ.get("no_proxy"),
        }
        # Always add proxies to the envs list
        env.update(default_env)
        img = expandvars(self.img, nounset=True)
        if self.serving:
            log = Test.serving_run(self, img, env, volumes)
        else:
            if self.notebook is True:
                Test.notebook_run(self, img)
            output_generator = docker.run(
                # Image
                img,
                # Command
                split(expandvars(self.cmd, nounset=True)),
                # Stream Logs
                stream=True,
                # Envs
                envs=env,
                # Volumes
                volumes=volumes,
                # Misc
                cap_add=[self.cap_add],
                devices=[expandvars(self.device, nounset=True)],
                entrypoint=(
                    expandvars(self.entrypoint, nounset=True)
                    if self.entrypoint
                    else None
                ),
                groups_add=[expandvars(self.groups_add, nounset=True)],
                hostname=self.hostname,
                ipc=self.ipc,
                privileged=self.privileged,
                pull=self.pull,
                remove=True,
                user=self.user,
                shm_size=self.shm_size,
                workdir=(
                    expandvars(self.workdir, nounset=True) if self.workdir else None
                ),
            )
            # Log within the function to retain scope for debugging
            log = ""
            for _, stream_content in output_generator:
                # All process logs will have the stream_type of stderr despite it being stdout
                if self.performance:
                    self.check_perf(stream_content.decode("utf-8"))
                for item in self.mask:
                    stream_content = re.sub(
                        rf"({item}[:]?\s+)(.*)",
                        r"\1***",
                        stream_content.decode("utf-8"),
                    ).encode("utf-8")
                logging.info(stream_content.decode("utf-8").strip())
                log += stream_content.decode("utf-8").strip()

        return log

    def run(self):
        """Run the command on baremetal.

        Raises:
            KeyboardInterrupt: re-raise the interrupt to flag the test as a failure

        Returns:
            str: subprocess output log
        """
        # Define each env as {key: value} for a dict of envs
        env = (
            {key: expandvars(val) for key, val in self.env.items()} if self.env else {}
        )
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
            if self.performance:
                self.check_perf(stdout.decode("utf-8"))
            for item in self.mask:
                stdout = re.sub(
                    rf"({item}[:]?\s+)(.*)", r"\1***", stdout.decode("utf-8")
                ).encode("utf-8")
            if stderr:
                logging.error(stderr.decode("utf-8").strip())
            if stdout:
                logging.info("Test Output: %s", stdout.decode("utf-8").strip())
            return stdout.decode("utf-8")
        except KeyboardInterrupt:
            os.killpg(os.getpgid(p.pid), SIGKILL)
            raise KeyboardInterrupt
