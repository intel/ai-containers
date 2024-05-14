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

import os
import sys

from matrix import compose_to_csv

models = {
    "name": "Intel AI Reference Models",
    "shortname": "models",
    "url": "https://github.com/IntelAI/models",
    "ref": "v3.1.1",
    "paths": {
        "docker/flex-gpu": "flex-pvc",
        "docker/max-gpu": "max-pvc",
        "docker/pyt-cpu": "pytorch-cpu",
        "docker/tf-cpu": "tensorflow-cpu",
    },
}

transformers = {
    "name": "Intel Extension for Transformers",
    "shortname": "itrex",
    "url": "https://github.com/intel/intel-extension-for-transformers",
    "ref": "v1.4.1",
    "paths": {
        "docker": "transformers",
    },
}

genai = {
    "name": "OPEA Generative AI Examples",
    "shortname": "genaiexamples",
    "url": "https://github.com/opea-project/GenAIExamples",
    "ref": "v0.1.0",
    "paths": {},
}


def get_repo(repo: dict):
    """
    Clones the repository and extracts metadata from the repository into csv tables.

    Args:
        repo (dict): The repository metadata containing the name, shortname, ref, paths, and url.

    Returns:
        None
    """
    # Clone the repository
    try:
        os.system(f"rm -rf docs/repos/{repo['shortname']}")
        os.system(
            f"git clone -b {repo['ref']} {repo['url']} docs/repos/{repo['shortname']}"
        )
    except:
        print(f"Failed to clone {repo['name']}")
        sys.exit(1)
    # Extract metadata from the repository
    for path in repo["paths"]:
        compose_to_csv(f"docs/repos/{repo['shortname']}/{path}", repo["paths"][path])
    os.system("rm -rf docs/repos/{repo['shortname']}")
