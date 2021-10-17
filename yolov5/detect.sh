#!/bin/sh

# 이미지 초기화
rm -rf /home/blushy/flowtracker/media/sliceimage/'1'/*
rm -rf /home/blushy/flowtracker/media/sliceimage_cb/'1'/*
rm -rf /home/blushy/flowtracker/runs/detect/*
rm -rf /home/blushy/flowtracker/media/yoloresult/*
rm -rf /home/blushy/flowtracker/media/unetresult/*
rm -rf /home/blushy/flowtracker/media/3dresult/*

#a.txt 초기화
rm -rf /home/blushy/flowtracker/a.txt
echo "select "title" from tab1_document order by id desc limit 1;" | sqlite3 db.sqlite3 > a.txt

#이름변경
while read line; do 
 echo $line 
 mv /home/blushy/flowtracker/media/'Uploaded Files'/* /home/blushy/flowtracker/media/'Uploaded Files'/$line.mp4
done < a.txt

#영상 framesclicing 
python /home/blushy/flowtracker/frameslicing.py

#preprocessing
python preprocess_image.py --original-dir /home/blushy/flowtracker/media/sliceimage/ --save-dir /home/blushy/flowtracker/media/sliceimage_cb/ --apply-median-blur

#yolo detect

#python /home/blushy/yolov5/yolov5-master/detect.py --weights "/home/blushy/yolov5/yolov5-master/runs/train/exp2/weights/best.pt" --source '/home/blushy/flowtracker/media/sliceimage_cb/1/' --save-crop

python /home/blushy/yolov5/yolov5-master/detect.py --weights "/home/blushy/yolov5/yolov5-master/runs/train/exp2/weights/best.pt" --source '/home/blushy/flowtracker/media/sliceimage_cb/1/' --save-crop --save-txt --hide-labels "True" --hide-conf "True"
cp -r /home/blushy/flowtracker/runs/detect/* /home/blushy/flowtracker/media/yoloresult/

#unet test
python /home/blushy/UNet/test.py --weights-dir "/home/blushy/UNet/best_model/segmentation/DeepLabV3_ResNet152_best.pth" --raw-image-dir "/home/blushy/flowtracker/runs/detect/test/crops" --save-dir "/home/blushy/flowtracker/media/unetresult" --device "0"

#3d model
python /home/blushy/depthmap/prog/spm.py --input=black --checkpoints_dir="/home/blushy/depthmap/prog/checkpoints/"
python /home/blushy/depthmap/prog/imgtopolynorm.py

#영상 초기화
#rm -rf /home/blushy/flowtracker/media/Uploaded Files/*
