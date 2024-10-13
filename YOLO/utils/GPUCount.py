import os
import torch
if torch.cuda.is_available():
    num_gpus = torch.cuda.device_count()
    print(f"Availabel GPUS:{num_gpus}")
else:
    print("no")