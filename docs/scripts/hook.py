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

from matrix import compose_to_csv
from readmes import copy_readmes, remove_readmes


def create_support_matrix():
    """
    Extracts metadata from the repositories and creates the support matrix for all relevant pages.

    Returns:
        None
    """
    # See matrix.md for expected format
    os.makedirs("docs/assets", exist_ok=True)
    os.makedirs("docs/repos", exist_ok=True)
    compose_to_csv("python", None)
    compose_to_csv("pytorch", None)
    compose_to_csv("pytorch", "serving")
    compose_to_csv("tensorflow", None)
    compose_to_csv("classical-ml", None)
    compose_to_csv("jax", None)

    # get_repo(models)
    compose_to_csv("preset/classical-ml", "classical_ml")
    compose_to_csv("preset/deep-learning-pytorch-cpu", "deep_learning_pytorch_cpu")
    compose_to_csv("preset/deep-learning-pytorch-gpu", "deep_learning_pytorch_gpu")
    compose_to_csv(
        "preset/deep-learning-tensorflow-cpu", "deep_learning_tensorflow_cpu"
    )
    compose_to_csv(
        "preset/deep-learning-tensorflow-gpu", "deep_learning_tensorflow_gpu"
    )
    compose_to_csv("preset/deep-learning-jax-cpu", "deep_learning_jax_cpu")


def on_pre_build(*args, **kwargs):
    "Runs before the build process."
    copy_readmes()
    create_support_matrix()


def on_post_build(*args, **kwargs):
    "Runs after the build process."
    remove_readmes()
    shutil.rmtree("docs/assets", ignore_errors=True)


if __name__ == "__main__":
    on_pre_build()
    on_post_build()
