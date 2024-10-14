import cmd
import inquirer
import logging
import os
import re
import subprocess
import sys
import tempfile
import yaml
from expandvars import UnboundVariable
from python_on_whales import DockerException
from tabulate import tabulate
from utils.test import PerfException, Volume
from yaml import YAMLError


def volume_constructor(loader, node):
    values = loader.construct_mapping(node)
    return Volume(**values)


def volume_representer(dumper, data):
    return dumper.represent_dict(data.to_yaml())


yaml.add_constructor('tag:yaml.org,2002:python/object:utils.test.Volume', volume_constructor)
yaml.add_representer(Volume, volume_representer)


class StreamToLogger:
    def __init__(self, logger, log_level):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass


class TestRunnerDebugger(cmd.Cmd):
    intro = "Welcome to the Test Runner Debugger. Type help or ? to list commands.\n"
    prompt = "(debugger) "
    docker_run_commands = []

    def __init__(self, tests, args):
        super().__init__()
        self.args = args
        self.tests = tests
        self.check_env_variables()

    def redirect_output(self):
        """Redirect stdout and stderr to the logging system."""
        sys.stdout = StreamToLogger(logging.getLogger('STDOUT'), logging.INFO)
        sys.stderr = StreamToLogger(logging.getLogger('STDERR'), logging.ERROR)

    def check_env_variables(self):
        """Check for required environment variables and log warnings if any are missing."""
        expected_vars = [
            'CACHE_REGISTRY', 'EDITOR', 'REGISTRY', 'REPO', 'GITHUB_RUN_NUMBER',
            'http_proxy', 'https_proxy', 'no_proxy'
        ]
        missing_vars = [var for var in expected_vars if var not in os.environ]
        if missing_vars:
            logging.warning("The following environment variables are not set:\n - " + "\n - ".join(missing_vars))
            logging.warning("Please set these environment variables as described in the README.md file.")

    def do_run(self, arg):
        'Select and run tests: run'
        original_stdout = sys.stdout
        original_stderr = sys.stderr

        questions = [
            inquirer.Checkbox(
                'tests',
                message="Select tests to run",
                choices=[test.name for test in self.tests],
            )
        ]

        answers = inquirer.prompt(questions)
        selected_tests = answers.get('tests', [])

        self.redirect_output()

        summary = []
        try:
            for idx, test_name in enumerate(selected_tests):
                try:
                    test = next((t for t in self.tests if t.name == test_name), None)
                    log = test.container_run() if test.img else test.run()
                except (DockerException, PerfException, YAMLError, UnboundVariable) as err:
                    logging.error(err)
                    summary.append([idx + 1, test.name, "FAIL"])
                    continue
                except KeyboardInterrupt:
                    summary.append([idx + 1, test.name, "FAIL"])
                    break
                summary.append([idx + 1, test.name, "PASS"])
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            print(tabulate(summary, headers=["#", "Test", "Status"], tablefmt="orgtbl"))
            self.capture_docker_run_commands(self.args.logs_path + "/test-runner.log")

    def do_setenv(self, arg):
        'Set an environment variable: setenv VAR_NAME=VALUE'
        try:
            var, value = arg.split('=', 1)
            os.environ[var] = value
            logging.info(f"Set environment variable {var}={value}")
        except ValueError:
            logging.error("Usage: setenv VAR_NAME=VALUE")

    def do_modify(self, arg):
        'Modify a test: modify'
        
        if not self.tests:
            logging.error("No tests available to modify.")
            return

        # Prompt the user to select a test to modify
        questions = [
            inquirer.List(
                'test_name',
                message="Select a test to modify",
                choices=[test.name for test in self.tests],
            )
        ]

        answers = inquirer.prompt(questions)
        test_name = answers.get('test_name')

        if not test_name:
            logging.error("No test selected.")
            return

        test = next((t for t in self.tests if t.name == test_name), None)
        if not test:
            logging.error(f"Test {test_name} not found.")
            return

        # Serialize the test object to YAML and open it in a text editor
        with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode='w') as temp_file:
            yaml.dump(vars(test), temp_file)
            temp_file_path = temp_file.name

        editor = os.getenv('EDITOR', 'nano')
        subprocess.run([editor, temp_file_path])
        # Wait for the user to finish editing the file
        if os.environ.get("EDITOR") == "code":
            last_modified_time = os.path.getmtime(temp_file_path)
            while True:
                import time
                time.sleep(1)
                new_modified_time = os.path.getmtime(temp_file_path)
                if new_modified_time != last_modified_time:
                    break

        # Read the modified content and re-create the Test object
        try:
            with open(temp_file_path, 'r') as temp_file:
                modified_data = yaml.safe_load(temp_file)
            
            # Validate and update the test object
            for attr, value in modified_data.items():
                if attr == 'volumes' and isinstance(value, list):
                    value = [Volume(**vol) if isinstance(vol, dict) else vol for vol in value]
                if hasattr(test, attr):
                    setattr(test, attr, value)
            
            logging.info(f"Test {test_name} modified successfully.")
        except Exception as e:
            logging.error(f"Failed to modify test {test_name}: {e}")
        finally:
            os.remove(temp_file_path)


    def do_print(self, arg):
        'Print the details of a selected test: print'
        if not self.tests:
            logging.error("No tests available to print.")
            return

        questions = [
            inquirer.List(
                'test_name',
                message="Select a test to print",
                choices=[test.name for test in self.tests],
            )
        ]

        answers = inquirer.prompt(questions)
        test_name = answers.get('test_name')

        if not test_name:
            logging.error("No test selected.")
            return

        test = next((t for t in self.tests if t.name == test_name), None)
        if not test:
            logging.error(f"Test {test_name} not found.")
            return

        print(yaml.dump(vars(test), default_flow_style=False))

    def do_EOF(self, line):
        'Exit the debugger: Ctrl+D'
        logging.info("Exiting the debugger.")
        return True

    def cmdloop(self, intro=None):
        try:
            super().cmdloop(intro)
        except KeyboardInterrupt:
            logging.info("Test interrupted by user. Returning to debugger prompt.")
            self.cmdloop(intro)

    def capture_docker_run_commands(self, log_file_path):
        """Capture Docker run commands from the log file."""
        docker_run_pattern = re.compile(r"The command executed was `(/usr/bin/docker container run .+?)`")
        with open(log_file_path, 'r') as log_file:
            for line in log_file:
                match = docker_run_pattern.search(line)
                if match:
                    self.docker_run_commands.append(match.group(1))

    def do_commands(self, arg):
        'Print the last Docker run commands: commands'
        if not self.docker_run_commands:
            logging.info("No Docker run commands captured.")
            return

        print("Last Docker run commands:")
        for command in self.docker_run_commands:
            print(command)
