#python test.py --weights-dir "/home/blushy/UNet/best_model/Automation/DeepLabV3_ResNet152_best.pth" --raw-image-dir "/home/blushy/DATA_all/images/1" --mask-image-dir "/home/blushy/DATA_all/masks/1" --save-dir "/home/blushy/DATA_all/test_result/1" --device "1"

python test.py --weights-dir "/home/blushy/UNet/best_model/segmentation/Unet_vgg19_bn_best.pth" --raw-image-dir "/home/blushy/yolov5/yolov5-master/runs/detect/test2/crops" --save-dir "/home/blushy/DATA_unet/test_result/5" --device "0"
#---mask-image-dir "/home/blushy/DATA_unet/masks/1" --save-dir "/home/blushy/DATA_unet/test_result/1" --device "0"
