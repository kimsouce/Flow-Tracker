import os
import os.path
import shutil
from PIL import Image
import numpy as np
import pyvista as pv

#원 데이터 경로
glob_path = "C:/Users/Dell/2dtodepth/2dtodepth/spm/outfile/"

file_list = os.listdir(glob_path)
file_list_jpg1 = []

file_list_jpg = [file for file in file_list if file.endswith(".jpg")]

for i in range(0,len(file_list_jpg)):
    #데이터 이름만 추출
    file_list_jpg1.append(file_list_jpg[i].split('.jp')[0])
    
for k in range(0,len(file_list_jpg1)):
    reshaped_list3 = []

    img = Image.open(glob_path + file_list_jpg1[k] + '.jpg').convert("L")
    grayimg1 = np.asarray(img.getdata()).reshape(img.size[1], img.size[0], -1)
    print(grayimg1)
    print(type(grayimg1))
    print(glob_path + file_list_jpg1[k] + '.jpg')
    print(grayimg1.shape)
    
    reshaped_gi1 = grayimg1.reshape(img.size[1],img.size[0])
    mean_z = np.mean(reshaped_gi1[:,int(img.size[0]/2):])
    standard_z = np.std(reshaped_gi1[:,int(img.size[0]/2):])
    mean_z1 = np.mean(reshaped_gi1[:,:int(img.size[0]/2)-1])
    standard_z1 = np.std(reshaped_gi1[:,:int(img.size[0]/2)-1])
    print(mean_z)
    
    # Mean Normalization        
    for i in range(0,reshaped_gi1.shape[0]):
        for j in range (int(img.size[0]/2), reshaped_gi1.shape[1]):
            reshaped_list3.append([i,j,((reshaped_gi1[i][j]+reshaped_gi1[i][j-int(img.size[0]/2)])/2)])
    
    reshaped_polydata3 = np.array(reshaped_list3)
    
    #polydata 3
    point_cloud = pv.PolyData(reshaped_polydata3)

    np.allclose(reshaped_polydata3, point_cloud.points)

    # point_cloud.plot(eye_dome_lighting=True)

    data = reshaped_polydata3[:,-1]

    point_cloud["elevation"] = data

    point_cloud.plot(render_points_as_spheres=True)