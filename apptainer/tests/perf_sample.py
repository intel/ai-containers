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

import time

import numpy as np

start = time.time()

rd = np.random.RandomState(88)
a = rd.randint(1, 1000, (1000, 1000))
y = rd.randint(1, 1000, (1000))
res = np.linalg.solve(a, y)

end = time.time()

print(res)
print("Time Consuming:", end - start)
