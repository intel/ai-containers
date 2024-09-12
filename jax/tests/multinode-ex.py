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
import mpi4jax
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()


@jax.jit
def foo(arr):
    arr = arr + rank
    arr_sum, _ = mpi4jax.allreduce(arr, op=MPI.SUM, comm=comm)
    return arr_sum


a = jnp.zeros((3, 3))
result = foo(a)

if rank == 0:
    print(result)
