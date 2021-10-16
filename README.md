# Flow-Tracker
하수관로 결함탐지 알고리즘  using UNET

# YOLOv5_Model

# UNet_Model

# Depthmap_Model
pip install -r ./requirements.txt
### Producing Depthmap
python ./prog/spm.py --input=black
### Producing 3D_vtk_file + Screenshot
python ./prog/depthto3d.py
### Producing OBJ data
python ./prog/vtktoobj.py

>>>>>>> 82381b54f979c9396d39542d767316eefc2d2be2
