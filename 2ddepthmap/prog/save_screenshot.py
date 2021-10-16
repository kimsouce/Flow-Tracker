import os
import os.path
import shutil
from PIL import Image
import numpy as np
import pyvista as pv
import vtk 
import open3d as o3d

# lets create dummy {x,y,z} coordinates
glob_path = "C:/Users/Dell/Desktop/depthmap/spm/outfile/"

file_list = os.listdir(glob_path)
file_list_vtk1 = []
file_list_png1 = []

file_list_vtk = [file for file in file_list if file.endswith(".vtk")]

for i in range(0,len(file_list_vtk)):
    #데이터 이름만 추출
    file_list_vtk1.append(file_list_vtk[i].split('.vt')[0])
    
for k in range(0,len(file_list_vtk1)):
    mesh = pv.read(glob_path + file_list_vtk1[k] + '.vtk')
    print(glob_path + file_list_vtk1[k] + '.vtk')
    data = np.loadtxt(glob_path + file_list_vtk1[k] + '.txt')
    mesh["elevation"] = data
    plotter = pv.Plotter(off_screen=True)
    plotter.add_mesh(mesh,render_points_as_spheres=True)
    plotter.show(screenshot= glob_path + file_list_vtk1[k] + '_3D.png')
    ## data list [:,-1]
    ## Class별 normalization 변경
    ## filename에서 if 구문으로 0,1,2,3,4,5,6 별 구분