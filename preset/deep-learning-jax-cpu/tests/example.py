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

# pylint: skip-file

import jax
import jax.numpy as jnp

print("jax.local_devices(): ", jax.local_devices())


@jax.jit
def lax_conv():
    key = jax.random.PRNGKey(0)
    lhs = jax.random.uniform(key, (2, 1, 9, 9), jnp.float32)
    rhs = jax.random.uniform(key, (1, 1, 4, 4), jnp.float32)
    side = jax.random.uniform(key, (1, 1, 1, 1), jnp.float32)
    out = jax.lax.conv_with_general_padding(
        lhs, rhs, (1, 1), ((0, 0), (0, 0)), (1, 1), (1, 1)
    )
    out = jax.nn.relu(out)
    out = jnp.multiply(out, side)
    return out


print(lax_conv())
