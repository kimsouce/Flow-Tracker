import math

import numpy as np
import matplotlib.pyplot as plt

import torch

from torchvision import transforms

def concat_image(tensor_input, tensor_pred) : #tensor_target) :
        # Initialize Torch Transformation
        to_pil = transforms.Compose([transforms.ToPILImage()])

        # Convert Tensor to Pillow Image
        image_input = np.array(to_pil(tensor_input), dtype = "uint8")
        image_pred = np.array(to_pil(torch.cat([tensor_pred, tensor_pred, tensor_pred], dim = 0)), dtype = "uint8")
        #image_target = np.array(to_pil(tensor_target), dtype = "uint8")

        # Stack Images
        stacked_image = np.hstack((image_input, image_pred)) #image_target))

        return stacked_image