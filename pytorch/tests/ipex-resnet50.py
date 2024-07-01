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
import argparse
import os

import intel_extension_for_pytorch as ipex
import torch
import torch.distributed as dist
import torchvision.models as models
from torch.nn.parallel import DistributedDataParallel as DDP

os.environ["RANK"] = str(os.environ.get("PMI_RANK", 0))
os.environ["WORLD_SIZE"] = str(os.environ.get("PMI_SIZE", 1))
init_method = "tcp://127.0.0.1:29500"

parser = argparse.ArgumentParser()
parser.add_argument("--device", default="cpu", choices=["cpu", "xpu"])
parser.add_argument("--ipex", action="store_true")
parser.add_argument("--backend", default="gloo", choices=["gloo", "ccl"])
parser.add_argument("--deepspeed", action="store_true")
args = parser.parse_args()

try:
    import oneccl_bindings_for_pytorch
except:
    pass

if args.deepspeed:
    import deepspeed

    deepspeed.init_distributed(dist_backend="mpi")
else:
    dist.init_process_group(
        backend=args.backend,
        init_method=init_method,
        world_size=int(os.environ.get("WORLD_SIZE")),
        rank=int(os.environ.get("RANK")),
    )

model = models.resnet50(pretrained=False)

model.eval()
data = torch.rand(1, 3, 224, 224)

model = model.to(args.device)
if dist.get_world_size() > 1:
    model = DDP(model, device_ids=[args.device] if (args.device != "cpu") else None)
data = data.to(args.device)
print("Choosing device: {}".format(args.device))

if args.ipex:
    model = ipex.optimize(model)
    print("Applying IPEX Optimization")

import time

with torch.no_grad():
    # Warmup
    for i in range(100):
        model(data)

    # Profiling
    total = 0.0
    for i in range(100):
        start = time.time()
        model(data)
        end = time.time()
        total += end - start
    print("Average Inference Time: {} seconds".format(total / 100.0))
