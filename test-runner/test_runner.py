from argparse import ArgumentParser
from shlex import split
from shutil import rmtree
from signal import SIGKILL
from subprocess import Popen, PIPE
from sys import exit as sysexit
import logging
import os
# Third Party
from expandvars import expandvars
from python_on_whales import docker, DockerException
from tabulate import tabulate
from yaml import full_load, YAMLError


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
            setattr(self, key, val)

    def get_path(self, name):
        """Given a filename, find that file from the users current working directory

        Args:
            name (string): Filename

        Returns:
            string: Path to filename of input name
        """
        for root, dirs, files in os.walk(os.getcwd()):
            if name in files:
                return os.path.join(root, name)
        logging.error("Notebook Dockerfile not found")
        exit(1)

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
            if self.notebook == 'true':
                try: # Try for Docker CLI Failure Conditions
                    docker.run(img, ["which", "papermill"])
                except DockerException as papermill_not_found:
                    logging.debug("Papermill not found: %s", papermill_not_found)
                    docker.build(
                        # context path
                        '.',
                        # Image Input and Proxy Args
                        build_args={
                            "BASE_IMAGE_NAME": img.split(':')[0],
                            "BASE_IMAGE_TAG": img.split(':')[1],
                            "http_proxy": os.environ.get("http_proxy"),
                            "https_proxy": os.environ.get("https_proxy")
                        },
                        # Input File
                        file=self.get_path("Dockerfile.notebook"),
                        # Output Tag = Input Tag
                        tags=[img]
                    )
        if hasattr(self, "serving"):
            if self.serving == 'true':
                log = ""
                try: # Try for Docker CLI Failure Conditions
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
                        networks=['host'],
                        # Misc
                        cap_add=[self.cap_add if hasattr(self, "cap_add") else "AUDIT_READ"],
                        devices=[expandvars(self.device) if hasattr(self, "device") else "/dev/dri"],
                        entrypoint=expandvars(self.entrypoint) if hasattr(self, "entrypoint") else None,
                        hostname=self.hostname if hasattr(self, "hostname") else None,
                        ipc=self.ipc if hasattr(self, "ipc") else None,
                        privileged=self.privileged if hasattr(self, "privileged") else True,
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
                        networks=['host'],
                        # Misc
                        cap_add=[self.cap_add if hasattr(self, "cap_add") else "AUDIT_READ"],
                        devices=[expandvars(self.device) if hasattr(self, "device") else "/dev/dri"],
                        entrypoint=expandvars(self.entrypoint) if hasattr(self, "entrypoint") else None,
                        hostname=self.hostname if hasattr(self, "hostname") else None,
                        ipc=self.ipc if hasattr(self, "ipc") else None,
                        privileged=self.privileged if hasattr(self, "privileged") else True,
                        pull=self.pull if hasattr(self, "pull") else "missing",
                        remove=self.rm if hasattr(self, "rm") else True,
                        user=self.user if hasattr(self, "user") else None,
                        shm_size=self.shm_size if hasattr(self, "shm_size") else None,
                        workdir=expandvars(self.workdir) if hasattr(self, "workdir") else None,
                    )
                except DockerException as err:
                    return "DockerException", err.return_code  # assume the return code is 0 unless otherwise specified
                finally:
                    # Log within the function to retain scope for debugging
                    for stream_type, stream_content in client_output:
                        # All process logs will have the stream_type of stderr despite it being stdout
                        logging.info(stream_content.decode('utf-8').strip())
                        log += stream_content.decode('utf-8').strip()
                    logging.debug("--- Server Logs ---")
                    logging.debug(docker.logs(serving_container))
                    docker.stop(serving_container, time=None)
                return log, 0
        # Try for Docker CLI Failure Conditions
        try:  # https://gabrieldemarmiesse.github.io/python-on-whales/sub-commands/container/#python_on_whales.components.container.cli_wrapper.ContainerCLI.run
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
                devices=[expandvars(self.device) if hasattr(self, "device") else "/dev/dri"],
                entrypoint=expandvars(self.entrypoint) if hasattr(self, "entrypoint") else None,
                groups_add=[expandvars(self.group-add) if hasattr(self, "group-add") else "109", "44"],
                hostname=self.hostname if hasattr(self, "hostname") else None,
                ipc=self.ipc if hasattr(self, "ipc") else None,
                privileged=self.privileged if hasattr(self, "privileged") else True,
                pull=self.pull if hasattr(self, "pull") else "missing",
                remove=self.rm if hasattr(self, "rm") else True,
                user=self.user if hasattr(self, "user") else None,
                shm_size=self.shm_size if hasattr(self, "shm_size") else None,
                workdir=expandvars(self.workdir) if hasattr(self, "workdir") else None,
            )
        except DockerException as err:
            return "DockerException", err.return_code  # assume the return code is 0 unless otherwise specified
        # Log within the function to retain scope for debugging
        log = ""
        for stream_type, stream_content in output_generator:
            # All process logs will have the stream_type of stderr despite it being stdout
            logging.info(stream_content.decode('utf-8').strip())
            log += stream_content.decode('utf-8').strip()
        return log, 0

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
            return stdout.decode("utf-8"), p.returncode
        except KeyboardInterrupt:
            os.killpg(os.getpgid(p.pid), SIGKILL)


def parse_args():
    """Use argparse to parse command line arguments

    Returns:
        dict: Parsed command line arguments
    """
    parser = ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        dest="file_path",
        help="-f /path/to/tests.yaml"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="log_level",
        action="store_true",
        help="DEBUG Loglevel"
    )
    parser.add_argument(
        "-l",
        "--logs",
        dest="logs_path",
        default="output",
        help="-l /path/to/logs"
    )

    return parser.parse_args()


def set_log_filename(logger, name, logs_path):
    """Change filehandler file name in current logger context

    Args:
        logger (logging.RootLogger): Current logger context
        name (string): New or Existing logger filename
        logs_path (string): Path to logs folder
    """    
    testHandler = logging.FileHandler(f"{logs_path}/{name}.log")
    # Handler[0] is the stream output to stdout/stderr
    # Handler[1] is always the file handler, see the logging declaration handlers parameter
    testHandler.setFormatter(logger.handlers[1].formatter)
    testHandler.setLevel(logger.handlers[1].level)
    logger.removeHandler(logger.handlers[1])
    logger.addHandler(testHandler)


if __name__ == "__main__":
    # Parse CLI Args
    args = parse_args()
    # Verify Logfile Handler Paths
    if os.path.exists(args.logs_path) is False:
        os.mkdir(args.logs_path)
    else:
        rmtree(args.logs_path)
        os.mkdir(args.logs_path)
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
            sysexit(1)
    # Check that each test contains 'cmd' and is therefore a valid test
    for test in tests_json:
        if "cmd" not in tests_json[test]:
            logging.error("Command not found for %s", test)
            sysexit(1)
    logging.debug("Creating Test Objects")
    # For each test, create a Test Object with the test name is the key of the test in yaml
    tests = [Test(test, tests_json[test]) for test in tests_json]
    logging.info("Setup Completed - Running Tests")
    summary = []
    ERROR = False
    returncode = 1
    for idx, test in enumerate(tests):
        # Set Context to test-runner.log
        set_log_filename(logging.getLogger(), "test-runner", args.logs_path)
        logging.info("Running Test: %s", test.name)
        # Switch logging context to test filename
        set_log_filename(logging.getLogger(), test.name, args.logs_path)
        logging.debug("Attrs: %s", dir(test)[26:])
        # If 'img' is present in the test, ensure that the test is a container run, otherwise run on baremetal
        # returns the stdout of the test and the returncode
        try: # Try for Runtime Failure Conditions
            log, returncode = test.container_run() if hasattr(test, "img") else test.run()
        except:
            summary.append([idx + 1, test.name, "FAIL"])
            ERROR = True
            continue
        finally:
            if returncode != 0 and ERROR == False:
                summary.append([idx + 1, test.name, "FAIL"])
                ERROR = True
                continue
        summary.append([idx + 1, test.name, "PASS"])
    # Switch logging context back to the initial state
    set_log_filename(logging.getLogger(), "test-runner", args.logs_path)
    # Remove remaining containers
    remaining_containers = docker.container.list()
    for container in remaining_containers:
        docker.stop(container, time=None)
    # Print Summary Table
    logging.info("\n%s", tabulate(summary, headers=["#", "Test", "Status"], tablefmt="orgtbl"))
    if ERROR:
        exit(1)
