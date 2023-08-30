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
    def __init__(self, name, arguments):
        self.name = name
        for key, val in arguments.items():
            setattr(self, key, val)

    def container_run(self):
        """Use Python on Whales to run a Docker Container with img and cmd. Extracts volumes and env"""
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
        # Always add proxies to the envs list
        env.update(default_env)
        logging.info("%s Started", self.name)
        try:  # https://gabrieldemarmiesse.github.io/python-on-whales/sub-commands/container/#python_on_whales.components.container.cli_wrapper.ContainerCLI.run
            log = docker.run(
                # Image
                expandvars(self.img),
                # Command
                split(expandvars(self.cmd)),
                # Envs
                envs=env,
                # Volumes
                volumes=volumes,
                # Misc
                cap_add=[self.cap_add if hasattr(self, "cap_add") else "AUDIT_READ"],
                devices=[expandvars(self.device) if hasattr(self, "device") else "/dev/dri"],
                entrypoint=expandvars(self.entrypoint) if hasattr(self, "entrypoint") else None,
                hostname=self.hostname if hasattr(self, "hostname") else None,
                ipc=self.ipc if hasattr(self, "ipc") else None,
                privileged=self.privileged if hasattr(self, "privileged") else True,
                pull=self.pull if hasattr(self, "pull") else "Always",
                remove=self.rm if hasattr(self, "rm") else True,
                user=self.user if hasattr(self, "user") else None,
                shm_size=self.shm_size if hasattr(self, "shm_size") else None,
                workdir=expandvars(self.workdir) if hasattr(self, "workdir") else None,
            )
        except DockerException as err:
            return err.return_code  # assume the return code is 0 unless otherwise specified
        # Log within the function to retain scope for debugging
        logging.info(log)
        return log, 0

    def run(self):
        """Create a process for cmd on Baremetal System. Extracts env"""
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
    """CLI"""
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
    """Change filehandler file name"""
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
    error = False
    for idx, test in enumerate(tests):
        # Switch logging context to a new filename
        set_log_filename(logging.getLogger(), test.name, args.logs_path)
        logging.debug("Attrs: %s", dir(test)[26:])
        # If 'img' is present in the test, ensure that the test is a container run, otherwise run on baremetal
        # returns the stdout of the test and the returncode
        try:
            log, returncode = test.container_run() if hasattr(test, "img") else test.run()
        except:
            summary.append([idx + 1, test.name, "FAIL"])
            error = True
            continue
        summary.append([idx + 1, test.name, "PASS"])
    # Switch logging context back to the initial state
    set_log_filename(logging.getLogger(), "test-runner", args.logs_path)
    # Print Summary Table
    logging.info("\n%s", tabulate(summary, headers=["#", "Test", "Status"], tablefmt="orgtbl"))
    if error:
        sysexit(1)
