import logging
import os
import sys
from shlex import split
from signal import SIGKILL
from subprocess import PIPE, Popen
from typing import Dict, List, Optional

from expandvars import expandvars
from pydantic import BaseModel
from python_on_whales import DockerException, docker


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
    notebook: Optional[bool] = False
    serving: Optional[bool] = False
    cap_add: Optional[str] = "AUDIT_READ"
    device: Optional[str] = "/dev/dri"
    entrypoint: Optional[str] = None
    groups_add: Optional[List[str]] = ["109", "44"]
    hostname: Optional[str] = None
    ipc: Optional[str] = None
    privileged: Optional[bool] = False
    pull: Optional[str] = "missing"
    user: Optional[str] = None
    shm_size: Optional[str] = None
    workdir: Optional[str] = None

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
            cap_add=[self.cap_add],
            devices=[expandvars(self.device)],
            entrypoint=(expandvars(self.entrypoint) if self.entrypoint else None),
            hostname=self.hostname,
            ipc=self.ipc,
            privileged=self.privileged,
            pull=self.pull,
            shm_size=self.shm_size,
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
            cap_add=[self.cap_add],
            devices=[expandvars(self.device)],
            hostname=self.hostname,
            ipc=self.ipc,
            privileged=self.privileged,
            pull=self.pull,
            remove=True,
            user=self.user,
            shm_size=self.shm_size,
            workdir=(expandvars(self.workdir) if self.workdir else None),
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
        img = expandvars(self.img)
        if self.serving is True:
            log = Test.serving_run(self, img, env, volumes)
        else:
            if self.notebook is True:
                Test.notebook_run(self, img)
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
                cap_add=[self.cap_add],
                devices=[expandvars(self.device)],
                entrypoint=(expandvars(self.entrypoint) if self.entrypoint else None),
                groups_add=[expandvars(self.groups_add)],
                hostname=self.hostname,
                ipc=self.ipc,
                privileged=self.privileged,
                pull=self.pull,
                remove=True,
                user=self.user,
                shm_size=self.shm_size,
                workdir=(expandvars(self.workdir) if self.workdir else None),
            )
            # Log within the function to retain scope for debugging
            log = ""
            for _, stream_content in output_generator:
                # All process logs will have the stream_type of stderr despite it being stdout
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
            if stderr:
                logging.error(stderr.decode("utf-8"))
            if stdout:
                logging.info("Test Output: %s", stdout.decode("utf-8"))
            return stdout.decode("utf-8")
        except KeyboardInterrupt:
            os.killpg(os.getpgid(p.pid), SIGKILL)
            raise KeyboardInterrupt
