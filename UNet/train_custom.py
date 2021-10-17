import argparse
import copy
import random

from os import listdir, getcwd, mkdir
from os.path import join

import wandb

import numpy as np

from datasets import DataFromFolder
from model import Generator
from utils import AverageMeter, set_logging, select_device
from export_image import concat_image

import segmentation_models_pytorch as smp

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.backends import cudnn
from torchsummary import summary
from tqdm import tqdm

def main() :
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type = str, default = "Automation")
    parser.add_argument("--model-name", type = str, default = "UNet_Custom")
    parser.add_argument("--raw-train-dir", type = str, required = True)
    parser.add_argument("--mask-train-dir", type = str, required = True)
    parser.add_argument("--raw-valid-dir", type = str, required = True)
    parser.add_argument("--mask-valid-dir", type = str, required = True)
    parser.add_argument("--input-shape", type = int, default = 256)
    parser.add_argument("--num_class", type = int, default = 2)
    parser.add_argument("--scale", type = int, default = 2)
    parser.add_argument("--batch-size", type = int, default = 8)
    parser.add_argument("--epochs", type = int, default = 500)
    parser.add_argument("--seed", type = int, default = 123)
    parser.add_argument("--device", default = "", help = "cuda device, i.e. 0 or 0,1,2,3 or cpu")
    args = parser.parse_args()

    # Get Current Namespace
    print(args)

    # Initialize Weights & Biases Library
    wandb.init(
                config = args,
                resume = "never",
                project = args.project
                )

    # Initialize Project Name
    wandb.run.name = args.model_name

    # Assign Device
    set_logging()
    device = select_device(args.model_name, args.device)

    # Set Seed
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed(args.seed)

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

    # Set Seed
    random.seed(args.seed)
    np.random.seed(args.seed)
    cudnn.deterministic = True
    cudnn.benchmark = False
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed(args.seed)

    # Load Dataset
    train_dataset = DataFromFolder(
                                    args.mask_train_dir,
                                    args.raw_train_dir,
                                    "train",
                                    args.input_shape,
                                    args.num_class,
                                    args.seed
                                    )
    valid_dataset = DataFromFolder(
                                    args.mask_valid_dir,
                                    args.raw_valid_dir,
                                    "valid",
                                    args.input_shape,
                                    args.num_class,
                                    args.seed
                                    )

    # Apply Mini-Batch
    train_dataloader = DataLoader(
                                    train_dataset,
                                    batch_size = args.batch_size,
                                    shuffle = True,
                                    drop_last = True)
    valid_dataloader = DataLoader(
                                    valid_dataset,
                                    batch_size = args.batch_size,
                                    shuffle = False,
                                    drop_last = True
                                    )

    # Get Parameters of Current Model
    print(summary(model, (3, args.input_shape, args.input_shape), batch_size = args.batch_size))

    # Initialize Optimizer
    optimizer = optim.Adam(
                            model.parameters(),
                            lr = 1e-4,
                            weight_decay = 1e-3
                            )

    # Let wandb Watch Training Process
    wandb.watch(model)

    # Initialize Learning Rate Scheduler
    scheduler = optim.lr_scheduler.StepLR(
                                            optimizer = optimizer,
                                            step_size = args.epochs // 5,
                                            gamma = 0.5
                                            )

    # Initialize Model for Savingf
    best_model = copy.deepcopy(model.state_dict())

    # Initialize Loss Function
    loss_function = nn.CrossEntropyLoss()

    # Initialize Variables
    best_epoch = 0
    best_acc = 0

    # Create Directory for Saving Weights
    if "best_model" not in listdir(getcwd()) :
        mkdir(join(getcwd(), "best_model"))

    if args.project not in listdir(join(getcwd(), "best_model")) :
        mkdir(join(getcwd(), "best_model", args.project))

    # Run Training
    for epoch in range(args.epochs) :
        # Get Current Learning Rate
        for param_group in optimizer.param_groups:
            current_lr = param_group["lr"]

        # Initialize tqdm
        train_bar = tqdm(train_dataloader)

        # Train Current Model
        model.train()

        # Initialize Loss
        train_loss = AverageMeter()
        train_acc = 0

        # Trian Data Mini-Batch
        for data in train_bar :
            # Assign Training Data
            inputs, target = data

            # Assign Device
            inputs = inputs.to(device)
            target = target.to(device)

            # Forward Pass Image
            preds = model(inputs)

            # Get Loss
            criterion = loss_function(preds, target.squeeze(1))

            # Update Loss
            train_loss.update(criterion.item(), len(inputs))

            preds = F.softmax(preds, dim = 1)
            preds = torch.argmax(preds, dim = 1)
            acc_map = torch.eq(preds, target.squeeze(1)).type(torch.float32)
            train_acc += torch.sum(acc_map).item() / (preds.size(0) * preds.size(1) * preds.size(2) * len(train_bar))

            # Set Gradient to Zero
            optimizer.zero_grad()

            # Backward Pass
            criterion.backward()

            # Update Generator Model
            optimizer.step()

            # Update tqdm Bar
            train_bar.set_description(desc=f"[{epoch}/{args.epochs - 1}] [Train] [Loss : {train_loss.avg:.6f}], [Accuracy : {train_acc:.6f}]")

        # Initialize tqdm
        valid_bar = tqdm(valid_dataloader)

        # Validate Generator
        model.eval()

        # Initialize Variables
        valid_loss = AverageMeter()
        valid_acc = 0

        with torch.no_grad() :
            # Validation Data Mini-Batch
            for data in valid_bar :
                # Assign Training Data
                inputs, target = data

                # Assign Device
                inputs = inputs.to(device)
                target = target.to(device)

                # Get Denoised Image
                preds = model(inputs)

                # Get Loss
                criterion = loss_function(preds, target.squeeze(1))

                # Update Train Loss
                valid_loss.update(criterion.item(), len(inputs))

                preds = F.softmax(preds, dim = 1)
                preds = torch.argmax(preds, dim = 1)
                acc_map = torch.eq(preds, target.squeeze(1)).type(torch.float32)
                valid_acc += torch.sum(acc_map).item() / (preds.size(0) * preds.size(1) * preds.size(2) * len(valid_bar))

                # Update tqdm Bar
                valid_bar.set_description(desc=f"[{epoch}/{args.epochs - 1}] [Validation] [Loss : {valid_loss.avg:.6f}], [Accuracy : {valid_acc:.6f}]")

        # Initialize List for Saving Image
        #sample_list = list()
        # Append Image
        #for i in range(args.batch_size) :
            #sample_image = concat_image(inputs[i], target[i])
            #sample_list.append(wandb.Image(sample_image, caption = f"Sample {i + 1}"))

        # Update Log
        wandb.log({
            "Learning Rate" : current_lr,
            "Validaion Loss" : valid_loss.avg,
            "Accuracy" : valid_acc
            })

        # Save New Values
        if valid_acc > best_acc :
            # Save Best Model
            best_model = copy.deepcopy(model.state_dict())

            # Update Variables
            best_acc = valid_acc
            best_epoch = epoch

            # Save Best Model
            torch.save(best_model, f"best_model/{args.project}/{args.model_name}_best.pth")

        # Update Learning Rate Scheduler
        scheduler.step()

    # Print Training Result
    print(f"Best Epoch : {best_epoch}")
    print(f"Best Accuracy : {best_acc:.4f}")

if __name__ == "__main__" :
    main()
