# Flow-Tracker
하수관로 결함탐지 알고리즘  using UNET

# YOLOv5_Model
### Detection
python ./yolov5/detect.py --weights 'path_to_your_weight' --source "path_to_your_infile"

# UNet_Model 
### Unet test
python ./UNet/test.py --weights-dir "path_to_your_weight" --raw-image-dir "path_to_your_infile" --save-dir "path_to_your_outfile"

# Depthmap_Model
pip install -r ./requirements.txt
### Producing Depthmap
python ./prog/spm.py --input=black
### Producing 3D_vtk_file + Screenshot
python ./prog/depthto3d.py
### Producing OBJ data
python ./prog/vtktoobj.py
