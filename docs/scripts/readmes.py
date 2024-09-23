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
import shutil

readmes = [
    "classical-ml/README.md",
    "jax/README.md",
    "preset/README.md",
    "python/README.md",
    "pytorch/README.md",
    "tensorflow/README.md",
    "workflows/README.md",
]


def copy_readmes():
    """
    Copies README.md files to the docs directory.

    Returns:
        None
    """
    shutil.copy("README.md", "docs/index.md")
    for readme in readmes:
        os.makedirs(os.path.dirname(f"docs/{readme}"), exist_ok=True)
        shutil.copy(readme, f"docs/{readme}")


def remove_readmes():
    """
    Removes README.md files added to docs directory by copy_readmes()

    Returns:
        None
    """
    try:
        os.remove("docs/index.md")
    except OSError:
        pass
    for readme in readmes:
        try:
            shutil.rmtree(os.path.dirname(f"docs/{readme}"))
        except:
            pass
