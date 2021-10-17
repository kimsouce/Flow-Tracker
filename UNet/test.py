import argparse

from os import listdir
from os.path import join

import PIL.Image as pil_image

import cv2
import numpy as np

import torch
from torch import functional
import torch.nn.functional as F
from torchvision import transforms

import segmentation_models_pytorch as smp

from model import Generator
from utils import set_logging, select_device

from tqdm import tqdm

def main() :
    # Argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-name", type = str, default = "UNet")
    parser.add_argument("--weights-dir", type = str, required = True)
    parser.add_argument("--raw-image-dir", type = str, required = True)
    parser.add_argument("--mask-image-dir", type = str, required = False)
    parser.add_argument("--save-dir", type = str, required = True)
    parser.add_argument("--input-shape", type = int, default = 256) 
    parser.add_argument("--num_class", type = int, default = 2)
    parser.add_argument("--scale", type = int, default = 2)
    parser.add_argument("--device", default = 1, help = "cuda device, i.e. 0 or 0,1,2,3 or cpu")
    args = parser.parse_args()

    # Get Current Namespace
    print(args)

    # Assign Device
    set_logging()
    device = select_device(args.model_name, args.device)

    # Load Trained DdenoisedNet Model
    '''
    model = model = Generator(
                scale = args.scale,
                in_channels = 3,
                out_channels = args.num_class,
                channels = 64,
                kernel_size = 3,
                stride = 1,
                dilation = 1,
                bias = True
                ).to(device)
    '''
    #model = smp.Unet("timm-regnetx_064", classes = args.num_class).to(device)
    #model = smp.Unet("resnet152", classes = args.num_class).to(device)
    model = smp.Unet("vgg19_bn", classes = args.num_class).to(device)
    model.load_state_dict(torch.load(args.weights_dir))

    # Initialize Torchvision Transforms
    to_tensor = transforms.Compose([
                                    transforms.Resize((args.input_shape, args.input_shape,)),
                                    transforms.ToTensor()]
                                    )
    to_pil = transforms.ToPILImage()

    # Assign Device
    model.to(device)
    model.eval()

    with tqdm(total = len(listdir(args.raw_image_dir))) as pbar :
        # Apply Denoising CNN
        with torch.no_grad() :
            for x in listdir(args.raw_image_dir) :
                # Get the Absolute Image Path
                raw_image_path = join(args.raw_image_dir, x)
                #target_image_path = join(args.mask_image_dir, x)

                # Get Image
                raw_image = pil_image.open(raw_image_path)
                #mask_image = pil_image.open(target_image_path).convert("L")

                # Convert Pillow Image to PyTorch Tensor
                raw_image_tensor = to_tensor(raw_image).unsqueeze(0).to(device)
                raw_image = to_pil(raw_image_tensor.squeeze(0).cpu())
                #mask_image = to_pil(to_tensor(mask_image))

                pred = F.softmax(model(raw_image_tensor).squeeze(0), dim = 0).detach().cpu()

                pred = torch.argmax(pred, dim = 0).unsqueeze(0)
                pred = pred.type(torch.float32)
                pred = to_pil(pred)
                
                dst = pil_image.new("L", (pred.width * 2, pred.height))
                dst.paste(raw_image.convert("L"), (0, 0))
                dst.paste(pred, (pred.width, 0))
                #dst.paste(mask_image, (pred.width * 2, 0))

                dst.save(f"{args.save_dir}/{x}")
                pbar.update()
                
if __name__ == "__main__" :
    main()
