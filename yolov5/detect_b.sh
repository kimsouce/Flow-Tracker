#!/bin/sh
#슬라이싱이미지 초기화
rm -rf /home/blushy/flowtracker/media/sliceimage/*
rm -rf /home/blushy/flowtracker/runs/detect/*

#이름변경
mv /home/blushy/flowtracker/media/'Uploaded Files'/* /home/blushy/flowtracker/media/'Uploaded Files'/mapo_20211002.mp4

#영상 framesclicing python
#python /home/blushy/frameslicing.py

#detect.sh 실행
python /home/blushy/yolov5/yolov5-master/detect.py --weights "/home/blushy/yolov5/yolov5-master/runs/train/exp2/weights/best.pt" --source '/home/blushy/flowtracker/media/Uploaded Files/' --save-crop --nosave
#--source '/home/blushy/yolov5/9/images/test/9'

#zenity --info --text="분석이 완료되었습니다./i"

rm -rf /home/blushy/flowtracker/media/Uploaded Files/*

python /home/blushy/UNet/test.py --weights-dir "/home/blushy/UNet/best_model/segmentation/DeepLabV3_ResNet152_best.pth" --raw-image-dir "/home/blushy/flowtracker/runs/detect/test/crops" --save-dir "/home/blushy/DATA_unet/test_result/1" --device "0"

