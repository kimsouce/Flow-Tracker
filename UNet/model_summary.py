import argparse

import torch
import torch.onnx
from torchsummary import summary

from model import Generator

import segmentation_models_pytorch as smp

from utils import set_logging, select_device

def main() :
    # Argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-name", type = str, default = "UNet")
    parser.add_argument("--input-shape", type = int, default = 256)
    parser.add_argument("--scale", type = int, default = 2)
    parser.add_argument("--num_class", type = int, default = 2)
    parser.add_argument("--batch-size", type = int, default = 32)
    parser.add_argument("--device", default = "", help = "cuda device, i.e. 0 or 0,1,2,3 or cpu")
    args = parser.parse_args()

    # Get Current Namespace
    print(args)

    # Assign Device
    set_logging()
    device = select_device(args.project_name, args.device)

    # Initialize Model
    model = Generator(
                scale = args.scale,
                in_channels = 3,
                out_channels = args.num_class,
                channels = 64,
                kernel_size = 3,
                stride = 1,
                dilation = 1,
                bias = True
                ).to(device)

    # Get Parameters of Current Model
    print(summary(model,
                    (3, args.input_shape, args.input_shape),
                    batch_size = args.batch_size))

    # Initialize Dummy Data for Exporting Model
    dummy_data = torch.empty(args.batch_size, 3, args.input_shape, args.input_shape, dtype = torch.float32).to(device)

    # Export Model as ONNX
    #torch.onnx.export(model, dummy_data, "onnx_model/Generator.onnx")

if __name__ == "__main__" :
    main()