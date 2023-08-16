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

import argparse
import yaml
import subprocess
from slugify import slugify
import os
from collections import namedtuple

TestResult = namedtuple("TestResult", "test_name status docker_cmd")


def run_command(command):
    process = subprocess.run(
        f'bash -c "{command}"', shell=True, check=True, text=True
    )
    status = "SUCCESS" if process.returncode == 0 else "FAILED"
    return status


def main(tests_yaml):
    with open(tests_yaml, "r") as stream:
        try:
            workloads = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    results = {}
    for workload_name, workload_value in workloads.items():
        print("workload_name: ", workload_name)
        print(" image_name: ", workload_value["image_name"])
        image_name = workload_value["image_name"]
        test_results = []
        for test in workload_value["tests"]:
            test_name = slugify(test["test_name"])

            docker_cmd = "docker run --rm"
            docker_cmd += " --env http_proxy={}".format(os.environ["http_proxy"])
            docker_cmd += " --env https_proxy={}".format(os.environ["http_proxy"])
            docker_cmd += " --env no_proxy={}".format(os.environ["no_proxy"])
            docker_cmd += " -v $PWD:/test -w /test"
            if test.get("env_vars"):            
                env_vars = test["env_vars"]  # its list not dict
                for key, value in env_vars.items():
                    docker_cmd += " --env {}={}".format(key, value)
            # TODO: Bug - what if volume directory is does not exists, docker test will
            #      eventually fail but test status will be success as docker cmd
            #      will return success
            docker_cmd += " " + image_name
            docker_cmd += " " + test["cmd"]

            # print("docker cmd: ", docker_cmd)
            status = run_command(docker_cmd)
            test_results.append(TestResult(test_name, status, docker_cmd))
            print("# ", slugify(test["test_name"]), " - ", status)
        results[workload_name] = test_results
    # TODO: summerize all results
    # with open(os.path.join(logs_dir, 'results.txt'), 'w') as f:
    #     f.write("---- Test results ----\n")
    #     for workload, test_results in results.items():
    #         f.write(F"\n{workload} \n")
    #         for test in test_results:
    #             f.write(F"  {test.test_name} - {test.status}  - { test.log_file}  - {test.docker_cmd}\n")


if __name__ == "__main__":
    print("---- Test Runner --")
    parser = argparse.ArgumentParser(
        description="Test runner execute tests run command and capture logs"
    )

    parser.add_argument(
        "--tests-yaml",
        type=str,
        dest="tests_yaml",
        required=True,
        help="Yaml file specifying workload image and its tests",
    )

    args = parser.parse_args()

    main(os.path.abspath(args.tests_yaml))
