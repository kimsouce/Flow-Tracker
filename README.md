# Flow-Tracker
하수관로 결함탐지 알고리즘

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

![example](https://user-images.githubusercontent.com/65105801/137611561-6ec31484-beb0-402b-b36e-6df63420ede3.jpg)
![0_example](https://user-images.githubusercontent.com/65105801/137611566-e53e7a94-c58f-4b2d-a8a6-f1c163adf1f7.jpg)

### Producing 3D_vtk_file + Screenshot
python ./prog/depthto3d.py

![0_example_3D](https://user-images.githubusercontent.com/65105801/137611569-02c01bea-c391-412c-8dd9-91fcea2c30e9.png)

### Producing OBJ data
python ./prog/vtktoobj.py
