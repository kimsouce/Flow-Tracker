import argparse

from os import listdir
from os.path import join

import cv2
import PIL.Image as pil_image
import numpy as np

from tqdm import tqdm

def main() :
    # Argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--original-dir", type = str, required = True)
    parser.add_argument("--save-dir", type = str, required = True)
    parser.add_argument("--apply-median-blur", action = "store_true")
    args = parser.parse_args()

    # Get Current Namespace
    print(args)

    # Preprocess Image
    for upper_dir in listdir(args.original_dir) :
        # Get Absolute Path
        current_dir = join(args.original_dir, upper_dir)
        save_dir = join(args.save_dir, upper_dir)

        with tqdm(total = len(listdir(current_dir))) as pbar : 
            for x in listdir(current_dir) :
                try : 
                    # Get Absolute Path
                    image_path = join(current_dir, x)

                    # Load Image
                    image = pil_image.open(image_path)

                    # Convert into Numpy Array
                    image = np.array(image, dtype = "uint8")

                    if args.apply_median_blur :
                        # Apply Median Blur
                        image = cv2.medianBlur(image, 3)

                    # Separate Channel
                    c_1 = image[:, :, 0]
                    c_2 = image[:, :, 1]
                    c_3 = image[:, :, 2]

                    # Initialize CLAHE Instance
                    clahe = cv2.createCLAHE(clipLimit = 2.0, tileGridSize = (8, 8))
                    
                    # Apply CLAHE
                    c_1 = clahe.apply(c_1)
                    c_2 = clahe.apply(c_2)
                    c_3 = clahe.apply(c_3)

                    # Expand Dimension
                    c_1 = np.expand_dims(c_1, 2)
                    c_2 = np.expand_dims(c_2, 2)
                    c_3 = np.expand_dims(c_3, 2)

                    # Concatenate Channels
                    image = np.concatenate((c_1, c_2, c_3), 2)

                    # Convert into Pillow
                    image = pil_image.fromarray(image)
                    
                    # Save Preprocessed Image
                    image.save(f"{save_dir}/{x}")
                
                except :
                    continue

                # Update TQDM Bar
                pbar.update()

if __name__ == "__main__" :
    main()
