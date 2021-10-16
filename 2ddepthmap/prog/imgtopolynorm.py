import os
import os.path
import shutil
from PIL import Image
import numpy as np
import pyvista as pv
import vtk 
import open3d as o3d
from pyntcloud import PyntCloud

#원 데이터 경로
glob_path = "../spm/outfile/"

file_list = os.listdir(glob_path)
file_list_jpg1 = []
file_list_png1 = []

file_list_jpg = [file for file in file_list if file.endswith(".jpg")]
file_list_png = [file for file in file_list if file.endswith(".png")]

for i in range(0,len(file_list_jpg)):
    #데이터 이름만 추출
    file_list_jpg1.append(file_list_jpg[i].split('.jp')[0])
for i in range(0,len(file_list_png)):
    file_list_png1.append(file_list_png[i].split('.pn')[0])

for k in range(0,len(file_list_jpg1)):
    #원본
    reshaped_list1 = []
    #
    reshaped_list3 = []
    #이음부 단차
    reshaped_list5 = []
    #균열
    reshaped_list7 = []
    # sphere1 = []
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
    
    # 전체 이미지
    for i in range(0,reshaped_gi1.shape[0]):
        for j in range (0, reshaped_gi1.shape[1]):
            reshaped_list1.append([i,j,reshaped_gi1[i][j]])
    print("1")
    
    for i in range(0,reshaped_gi1.shape[0]):
        for j in range (int((reshaped_gi1.shape[1])/2)+1, reshaped_gi1.shape[1]):
            if reshaped_gi1[i][j-int(img.size[0]/2)] < (mean_z1 * 0.2):
                reshaped_list3.append([i,j,(100*(reshaped_gi1[i][j]+mean_z)-10*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/170])
            else:
                reshaped_list3.append([i,j,(100*(reshaped_gi1[i][j]+mean_z)+60*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/200])
    print('3')
    # # Mean Normalization        
    # for i in range(0,reshaped_gi1.shape[0]):
        # for j in range (int(img.size[0]/2), reshaped_gi1.shape[1]):
                        # reshaped_list3.append([i,j,(((reshaped_gi1[i][j]+mean_z)+(reshaped_gi1[i][j-int(img.size[0]/2)])-mean_z1)/2)])
                        
   ###########################################################
   ######################3 번 : 이음부 단차######################## 
   ###########################################################
   
    for i in range(0,reshaped_gi1.shape[0]):
        for j in range (int((reshaped_gi1.shape[1])/2)+1, reshaped_gi1.shape[1]):
            if reshaped_gi1[i][j-int(img.size[0]/2)] < (mean_z1 * 0.5):
                reshaped_list5.append([i,j,(-100*(reshaped_gi1[i][j]+mean_z)+30*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/130])
            else:
                reshaped_list5.append([i,j,(-100*(reshaped_gi1[i][j]+mean_z)+30*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/130])

    print("5")        
    # standard dev Normalization
    # for i in range(0,reshaped_gi1.shape[0]-4):
        # for j in range (0, int(img.size[0]/2)):
            # standard_value = (reshaped_gi1[i][j] - mean_z1)/standard_z1
            # if standard_value > 0:
                # reshaped_list5.append([i,j,(mean_z1+reshaped_gi1[i][j+int(img.size[0]/2)])/2])
            # else:
                # reshaped_list5.append([i,j,(reshaped_gi1[i][j]+reshaped_gi1[i][j+int(img.size[0]/2)]) - mean_z1])
    
    # Normalization_diff2
   ###########################################################
   ######################  0 번 : 균열  ######################## 
   ###########################################################    
    for i in range(0,reshaped_gi1.shape[0]):
        for j in range (int((reshaped_gi1.shape[1])/2)+1, reshaped_gi1.shape[1]):
            reshaped_list7.append([i,j,(100*(reshaped_gi1[i][j]+mean_z)+30*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/222])
    print("7")
    # plotter = pv.Plotter()    
    # for i in range(0,reshaped_gi1.shape[0]):
        # for j in range (int((reshaped_gi1.shape[1])/2)+1, reshaped_gi1.shape[1]):
            # a = plotter.add_mesh(pv.Sphere(radius = 0.02,center = (i,j,(100*(reshaped_gi1[i][j]+mean_z)+30*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/222)))
            # print('added',i*reshaped_gi1.shape[1]+j,'spot')
    # plotter.show()
    

        
    reshaped_polydata1 = np.array(reshaped_list1)
    reshaped_polydata3 = np.array(reshaped_list3)
    reshaped_polydata5 = np.array(reshaped_list5)
    reshaped_polydata7 = np.array(reshaped_list7)
    # print(reshaped_polydata1)
    # print(type(reshaped_polydata1))
   
    # cloud = PyntCloud(pd.DataFrame(
    # # same arguments that you are passing to visualize_pcl
    # data=np.hstack((reshaped_polydata7, colors)),
    # columns=["x", "y", "z", "red", "green", "blue"]))
    
    # cloud.to_file("output.ply")
    # FROM PyVista
    #############################################################################
    # original_point_cloud = pv.read("diamond.ply")
    # cloud = PyntCloud.from_instance("pyvista", original_point_cloud)

    # # TO PyVista
    # cloud = PyntCloud.from_file("diamond.ply")
    # converted_triangle_mesh = cloud.to_instance("pyvista", mesh=True)
    
    #############################################################################
    #polydata 1
    point_cloud = pv.PolyData(reshaped_polydata1)

    np.allclose(reshaped_polydata1, point_cloud.points)

    # point_cloud.plot(eye_dome_lighting=True)
    
    data = reshaped_polydata1[:,-1]

    point_cloud["elevation"] = data
    
    point_cloud.plot(render_points_as_spheres=True)
    
    #polydata 3
    point_cloud = pv.PolyData(reshaped_polydata3)

    np.allclose(reshaped_polydata3, point_cloud.points)

    # point_cloud.plot(eye_dome_lighting=True)

    data = reshaped_polydata3[:,-1]

    point_cloud["elevation"] = data

    point_cloud.plot(render_points_as_spheres=True)
    
    # #polydata 5
    point_cloud = pv.PolyData(reshaped_polydata5)

    np.allclose(reshaped_polydata5, point_cloud.points)

    # point_cloud.plot(eye_dome_lighting=True)

    data = reshaped_polydata5[:,-1]

    point_cloud["elevation"] = data

    point_cloud.plot(render_points_as_spheres=True)
    
    #polydata 7
    point_cloud = pv.PolyData(reshaped_polydata7)

    np.allclose(reshaped_polydata7, point_cloud.points)

    # point_cloud.plot(eye_dome_lighting=True)

    data = reshaped_polydata7[:,-1]
    point_cloud.save(glob_path + file_list_jpg1[k] + '.vtk')
    
    mesh = pv.read(glob_path + file_list_jpg1[k] + '.vtk')
    # mesh.plot(render_points_as_spheres=True)
    
    mesh["elevation"] = data
    ########
    mesh.plot(render_points_as_spheres=True)
    ######
    np.savetxt(glob_path + file_list_jpg1[k] + '.txt',data)
    ######
    # mesh.plot()
    #######
    
    
    # poisson_mesh(point_cloud)
    
    
    # shell = mesh.delaunay_3d(alpha=0.005, progress_bar=True)
    # shell = shell.extract_geometry().triangulate()
    # shell.plot()
    

    

    for k in range(0,len(file_list_png1)):
        reshaped_list1 = []
        reshaped_list3 = []
        reshaped_list5 = []
        reshaped_list7 = []
        img = Image.open(glob_path + file_list_png1[k] + '.png').convert("L")
        grayimg1 = np.asarray(img.getdata(glob_path + file_list_png1[k] + '.png')).reshape(img.size[1], img.size[0], -1)
        print(type(grayimg1))
        print(glob_path + file_list_png1[k] + '.png')
        print(grayimg1.shape)
        
        reshaped_gi1 = grayimg1.reshape(img.size[1],img.size[0])
        mean_z = np.mean(reshaped_gi1[:,int(img.size[0]/2):])
        standard_z = np.std(reshaped_gi1[:,int(img.size[0]/2):])
        mean_z1 = np.mean(reshaped_gi1[:,:int(img.size[0]/2)-1])
        standard_z1 = np.std(reshaped_gi1[:,:int(img.size[0]/2)-1])
        print(mean_z)
        
        # 전체 이미지
        for i in range(0,reshaped_gi1.shape[0]):
            for j in range (0, reshaped_gi1.shape[1]):
                reshaped_list1.append([i,j,reshaped_gi1[i][j]])
        
        # Mean Normalization        
        for i in range(0,reshaped_gi1.shape[0]):
            for j in range (int(img.size[0]/2), reshaped_gi1.shape[1]):
                            reshaped_list3.append([i,j,(((reshaped_gi1[i][j]+mean_z)+(reshaped_gi1[i][j-int(img.size[0]/2)])-mean_z1)/2)])
        
        # standard dev Normalization
        # for i in range(0,reshaped_gi1.shape[0]-4):
            # for j in range (0, int(img.size[0]/2)):
                # standard_value = (reshaped_gi1[i][j] - mean_z1)/standard_z1
                # if standard_value > 0:
                    # reshaped_list5.append([i,j,(mean_z1+reshaped_gi1[i][j+int(img.size[0]/2)])/2])
                # else:
                    # reshaped_list5.append([i,j,(reshaped_gi1[i][j]+reshaped_gi1[i][j+int(img.size[0]/2)]) - mean_z1])
        
        # Normalization_diff2        
        for i in range(0,reshaped_gi1.shape[0]):
            for j in range (int((reshaped_gi1.shape[1])/2)+1, reshaped_gi1.shape[1]):
                reshaped_list7.append([i,j,(100*(reshaped_gi1[i][j]+mean_z)+30*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/222])
                
        reshaped_polydata1 = np.array(reshaped_list1)
        reshaped_polydata3 = np.array(reshaped_list3)
        # reshaped_polydata5 = np.array(reshaped_list5)
        reshaped_polydata7 = np.array(reshaped_list7)
        print(reshaped_polydata1)
        print(type(reshaped_polydata1))
        
        #polydata 1
        point_cloud = pv.PolyData(reshaped_polydata1)

        np.allclose(reshaped_polydata1, point_cloud.points)

        # point_cloud.plot(eye_dome_lighting=True)
        
        # point_cloud.save(glob_path + file_list_jpg1[k] + '.vtk')
        
        data = reshaped_polydata1[:,-1]

        point_cloud["elevation"] = data
        
        # point_cloud.plot(render_points_as_spheres=True)
        
        #polydata 3
        point_cloud = pv.PolyData(reshaped_polydata3)

        np.allclose(reshaped_polydata3, point_cloud.points)

        # point_cloud.plot(eye_dome_lighting=True)

        data = reshaped_polydata3[:,-1]

        point_cloud["elevation"] = data

        # point_cloud.plot(render_points_as_spheres=True)
        
        # #polydata 5
        # point_cloud = pv.PolyData(reshaped_polydata5)

        # np.allclose(reshaped_polydata5, point_cloud.points)

        # point_cloud.plot(eye_dome_lighting=True)

        # data = reshaped_polydata5[:,-1]

        # point_cloud["elevation"] = data

        # point_cloud.plot(render_points_as_spheres=True)
        
        #polydata 7
        point_cloud = pv.PolyData(reshaped_polydata7)

        np.allclose(reshaped_polydata7, point_cloud.points)

        # point_cloud.plot(eye_dome_lighting=True)

        data = reshaped_polydata7[:,-1]

        point_cloud["elevation"] = data
        
        point_cloud.save(glob_path + file_list_jpg1[k] + '.vtk')

        # point_cloud.plot(render_points_as_spheres=True)
