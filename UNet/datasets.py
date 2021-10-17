from os import listdir
from os.path import join

import random
from random import randint
import numpy as np

import PIL.Image as pil_image

import torch
from torch.utils.data import Dataset
import torchvision.transforms as transforms

# From raw Image
class DataFromFolder(Dataset) :
    def __init__(self, mask_image_dir, raw_image_dir, mode, image_size, num_class, seed) :
        # Inherit Parents Class
        super(DataFromFolder, self).__init__()

        # Initialize Variables
        self._image_size_ = image_size
        self._num_class_ = num_class

        # Fix Seed
        random.seed(seed)
        np.random.seed(seed)

        # Create List Instance for Saving Path
        self.mask_image_path_list, self.raw_image_path_list = list(), list() 
        
        # Initialize Image Path List
        for label in listdir(mask_image_dir) : 
            for local_path in [join(mask_image_dir, label, image) for image in listdir(join(mask_image_dir, label))] :
                self.mask_image_path_list.append(local_path)
            
            for local_path in [join(raw_image_dir, label, image) for image in listdir(join(raw_image_dir, label))] :
                self.raw_image_path_list.append(local_path)

        # Sort Path List in Order
        self.mask_image_path_list.sort()
        self.raw_image_path_list.sort()

        # Initialize Probability
        p_h = randint(0, 1)
        p_v = randint(0, 1)

        # Initialize Image Transformation
        if mode == "train" :
            self.transform = transforms.Compose([
                                                            transforms.Resize((image_size, image_size)),
                                                            transforms.RandomHorizontalFlip(p = p_h),
                                                            transforms.RandomVerticalFlip(p = p_v),
                                                            transforms.ToTensor()]
                                                            )

        elif mode == "valid" :
            self.transform = transforms.Compose([
                                                            transforms.Resize((image_size, image_size)),
                                                            transforms.ToTensor()]
                                                            )

    def _load_image_(self, image_path) :
        # Convert into Pillow Image
        image = pil_image.open(image_path)

        return image

    def __getitem__(self, index) :
        # Load Image
        input = self._load_image_(self.raw_image_path_list[index])
        target = self._load_image_(self.mask_image_path_list[index]).convert("L")

        # Get Label
        label = int(self.mask_image_path_list[index].split("/")[-2])

        # Apply PyTorch Transforms
        input = self.transform(input)
        target = self.transform(target)
        target = torch.where(target == 0, target, torch.ones(1))
        target = target.long() * label
        
        return input, target

    def __len__(self) :
        # Get Number of Data
        return len(self.raw_image_path_list)