#python train.py --raw-train-dir  "/home/blushy/DATA_clahe/train/images/" --mask-train-dir "/home/blushy/DATA_clahe/train/masks/" --raw-valid-dir  "/home/blushy/DATA_clahe/val/images/" --mask-valid-dir "/home/blushy/DATA_clahe/val/masks/" --device "1"

#python train.py --raw-train-dir  "/home/blushy/DATA_unet/images/" --mask-train-dir "/home/blushy/DATA_unet/masks/" --raw-valid-dir  "/home/blushy/DATA_unet/images/" --mask-valid-dir "/home/blushy/DATA_unet/masks/" --device "0"

python train.py --raw-train-dir  "/home/blushy/DATA_unet_cb/images/" --mask-train-dir "/home/blushy/DATA_unet_cb/masks/" --raw-valid-dir  "/home/blushy/DATA_unet_cb/val_img/" --mask-valid-dir "/home/blushy/DATA_unet_cb/val_msk/" --device "1"

#python train1.py --raw-train-dir  "/home/blushy/DATA_unet/images/" --mask-train-dir "/home/blushy/DATA_unet/masks/" --raw-valid-dir  "/home/blushy/DATA_unet/images/" --mask-valid-dir "/home/blushy/DATA_unet/masks/" --device "1"
