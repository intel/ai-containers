import torch
import torchvision.models as models
import intel_extension_for_pytorch as ipex
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--device', default='cpu', choices=['cpu', 'xpu'])
parser.add_argument('--ipex', action='store_true')
args = parser.parse_args()

model = models.resnet50(pretrained=False)
model.eval()
data = torch.rand(1, 3, 224, 224)

model = model.to(args.device)
data = data.to(args.device)
print('Choosing device: {}'.format(args.device))

if args.ipex:
    model = ipex.optimize(model)
    print('Applying IPEX Optimization')

import time
with torch.no_grad():
    #Warmup
    for i in range(100):
        model(data)

    #Profiling
    total = 0.0
    for i in range(100):
        start = time.time()
        model(data)
        end = time.time()
        total += (end-start)
    print("Average Inference Time: {} seconds".format(total/100.0))
