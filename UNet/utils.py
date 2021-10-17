import os
import logging
import subprocess
from pathlib import Path

import torch

################################################################################ Metric
def calc_psnr(img1, img2):
    return 10. * torch.log10(1. / torch.mean((img1 - img2) ** 2))

class AverageMeter(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

################################################################################ CUDA
try :
    import thop  # for FLOPS computation
except ImportError:
    thop = None
logger = logging.getLogger(__name__)

def git_describe() :
    # return human-readable git description, i.e. v5.0-5-g3e25f1e https://git-scm.com/docs/git-describe
    if Path('.git').exists() :
        return subprocess.check_output('git describe --tags --long --always', shell=True).decode('utf-8')[:-1]
    else:
        return ''

def select_device(project_name, device = "", batch_size = None) :
    # device = 'cpu' or '0' or '0,1,2,3'1
    s = f'{project_name} {git_describe()} torch {torch.__version__} '  # string
    cpu = device.lower() == 'cpu'
    if cpu :
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # force torch.cuda.is_available() = False
    elif device :  # non-cpu device requested
        os.environ['CUDA_VISIBLE_DEVICES'] = device  # set environment variable
        assert torch.cuda.is_available(), f'CUDA unavailable, invalid device {device} requested'  # check availability

    cuda = not cpu and torch.cuda.is_available()
    if cuda :
        n = torch.cuda.device_count()
        if n > 1 and batch_size:  # check that batch_size is compatible with device_count
            assert batch_size % n == 0, f'batch-size {batch_size} not multiple of GPU count {n}'
        space = ' ' * len(s)
        for i, d in enumerate(device.split(',') if device else range(n)):
            p = torch.cuda.get_device_properties(i)
            s += f"{'' if i == 0 else space}CUDA:{d} ({p.name}, {p.total_memory / 1024 ** 2}MB)\n"  # bytes to MB
    else :
        s += 'CPU\n'

    logger.info(s)  # skip a line
    return torch.device('cuda:0' if cuda else 'cpu')

def set_logging(rank=-1):
    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO if rank in [-1, 0] else logging.WARN)