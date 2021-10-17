import os
import os.path
from PIL import Image
import numpy as np
import pyvista as pv
import vtk 

glob_path =  '../spm/outfile/'

file_list = os.listdir(glob_path + '2d/')
file_list_jpg1 = []
file_class_jpg = []
file_list_png1 = []
file_class_png = []

file_list_jpg = [file for file in file_list if file.endswith(".jpg")]
file_list_png = [file for file in file_list if file.endswith(".png")]


for i in range(0,len(file_list_jpg)):
    #데이터 이름만 추출
    file_list_jpg1.append(file_list_jpg[i].split('.jp')[0])
    file_class_jpg.append(file_list_jpg1[i].split('_')[0])
print(file_class_jpg)
    
for i in range(0,len(file_list_png)):
    file_list_png1.append(file_list_png[i].split('.pn')[0])
    file_class_png.append(file_list_png1[i].split('_')[0])
print(file_class_png)

for k in range(0,len(file_list_jpg1)):
    reshaped_list_og = []
    reshaped_list_0 = []
    reshaped_list_1 = []
    reshaped_list_2 = []
    reshaped_list_3 = []
    reshaped_list_5 = []
    reshaped_list_6 = []
    img = Image.open(glob_path +'2d/' + file_list_jpg1[k] + '.jpg').convert("L")
    grayimg1 = np.asarray(img.getdata()).reshape(img.size[1], img.size[0], -1)
    reshaped_gi1 = grayimg1.reshape(img.size[1],img.size[0])
    mean_z = np.mean(reshaped_gi1[:,int(img.size[0]/2):])
    standard_z = np.std(reshaped_gi1[:,int(img.size[0]/2):])
    mean_z1 = np.mean(reshaped_gi1[:,:int(img.size[0]/2)-1])
    standard_z1 = np.std(reshaped_gi1[:,:int(img.size[0]/2)-1])
    print(glob_path + file_list_jpg1[k] + '.jpg')
    print('mean_z: ', mean_z)
    print('mean_z1 :', mean_z1)
    
    #Original Plot
    # for i in range(0,reshaped_gi1.shape[0]):
        # for j in range (0, reshaped_gi1.shape[1]):
            # reshaped_list_og.append([i,j,reshaped_gi1[i][j]])
    # reshaped_polydata1 = np.array(reshaped_list_og)
    # point_cloud = pv.PolyData(reshaped_polydata1)
    # np.allclose(reshaped_polydata1, point_cloud.points)
    # data1 = reshaped_polydata1[:,-1]
    # point_cloud["elevation"] = data1
    # # point_cloud.plot(render_points_as_spheres=True)
    #class 0 (균열)
    if int(file_class_jpg[k]) == 0:
        for i in range(0,reshaped_gi1.shape[0]):
            for j in range (int((reshaped_gi1.shape[1])/2)+1, reshaped_gi1.shape[1]):
                reshaped_list_0.append([i,j,(100*(reshaped_gi1[i][j]+mean_z)+30*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/222])
        reshaped_polydata1 = np.array(reshaped_list_0)
        point_cloud = pv.PolyData(reshaped_polydata1)
        np.allclose(reshaped_polydata1, point_cloud.points)
        data1 = reshaped_polydata1[:,-1]
        point_cloud["elevation"] = data1
        surf = point_cloud.delaunay_2d()
        # point_cloud.plot(render_points_as_spheres=True)
        surf.save(glob_path + 'vtk/' + file_list_jpg1[k] + '.vtk')
        np.savetxt(glob_path + 'vtk/' + file_list_jpg1[k] + '.txt',data1)
        plotter = pv.Plotter(off_screen=True)
        plotter.add_mesh(surf,render_points_as_spheres=True)
        plotter.show(screenshot= glob_path+'screenshot/' + file_list_jpg1[k] + '_3D.png',auto_close=True)
    #class 1 (연결관돌출)
    elif int(file_class_jpg[k]) == 1:
        for i in range(0,reshaped_gi1.shape[0]):
            for j in range (int((reshaped_gi1.shape[1])/2)+1, reshaped_gi1.shape[1]):
                reshaped_list_1.append([i,j,(-175*(reshaped_gi1[i][j]-mean_z)+30*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/145+mean_z])
        reshaped_polydata1 = np.array(reshaped_list_1)
        point_cloud = pv.PolyData(reshaped_polydata1)
        np.allclose(reshaped_polydata1, point_cloud.points)
        data1 = reshaped_polydata1[:,-1]
        point_cloud["elevation"] = data1
        surf = point_cloud.delaunay_2d()
        # point_cloud.plot(render_points_as_spheres=True)
        surf.save(glob_path + 'vtk/' + file_list_jpg1[k] + '.vtk')
        np.savetxt(glob_path + 'vtk/' + file_list_jpg1[k] + '.txt',data1)
        plotter = pv.Plotter(off_screen=True)
        plotter.add_mesh(surf,render_points_as_spheres=True)
        plotter.show(screenshot= glob_path +'screenshot/'+ file_list_jpg1[k] + '_3D.png',auto_close=True)
    #class 2 (연결관 접합부 이상)
    elif int(file_class_jpg[k]) == 2:
        for i in range(0,reshaped_gi1.shape[0]):
            for j in range (int((reshaped_gi1.shape[1])/2)+1, reshaped_gi1.shape[1]):
                reshaped_list_2.append([(150*(reshaped_gi1[i][j]+mean_z)-15*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/180,j,-i])
        reshaped_polydata1 = np.array(reshaped_list_2)
        point_cloud = pv.PolyData(reshaped_polydata1)
        np.allclose(reshaped_polydata1, point_cloud.points)
        data1 = reshaped_polydata1[:,0]
        point_cloud["elevation"] = data1
        surf = point_cloud.delaunay_2d()
        # point_cloud.plot(render_points_as_spheres=True)
        surf.save(glob_path + 'vtk/' + file_list_jpg1[k] + '.vtk')
        np.savetxt(glob_path + 'vtk/' + file_list_jpg1[k] + '.txt',data1)
        plotter = pv.Plotter(off_screen=True)
        plotter.add_mesh(surf,render_points_as_spheres=True)
        plotter.show(screenshot= glob_path +'screenshot/'+ file_list_jpg1[k] + '_3D.png',auto_close=True)
    #class 3 (이음부 이탈)
    elif int(file_class_jpg[k]) == 3:
        for i in range(0,reshaped_gi1.shape[0]):
            for j in range (int((reshaped_gi1.shape[1])/2)+1, reshaped_gi1.shape[1]):
                reshaped_list_3.append([i,j,(100*(reshaped_gi1[i][j]+mean_z)-30*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/130])
        reshaped_polydata1 = np.array(reshaped_list_3)
        point_cloud = pv.PolyData(reshaped_polydata1)
        np.allclose(reshaped_polydata1, point_cloud.points)
        data1 = reshaped_polydata1[:,-1]
        point_cloud["elevation"] = data1
        surf = point_cloud.delaunay_2d()
        # point_cloud.plot(render_points_as_spheres=True)
        surf.save(glob_path + 'vtk/' + file_list_jpg1[k] + '.vtk')
        np.savetxt(glob_path + 'vtk/' + file_list_jpg1[k] + '.txt',data1)
        plotter = pv.Plotter(off_screen=True)
        plotter.add_mesh(surf,render_points_as_spheres=True)
        plotter.show(screenshot= glob_path +'screenshot/'+ file_list_jpg1[k] + '_3D.png',auto_close=True)
    #class 5 (표면손상)
    elif int(file_class_jpg[k]) == 5:
        for i in range(0,reshaped_gi1.shape[0]):
            for j in range (int((reshaped_gi1.shape[1])/2)+1, reshaped_gi1.shape[1]):
                if reshaped_gi1[i][j-int(img.size[0]/2)] < (mean_z1 * 0.5):
                    reshaped_list_5.append([i,j,(175*(reshaped_gi1[i][j]-mean_z)-30*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/145+mean_z])
                else:
                    reshaped_list_5.append([i,j,(100*(reshaped_gi1[i][j]-mean_z)+70*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/200+mean_z])
        reshaped_polydata1 = np.array(reshaped_list_5)
        point_cloud = pv.PolyData(reshaped_polydata1)
        np.allclose(reshaped_polydata1, point_cloud.points)
        data1 = reshaped_polydata1[:,-1]
        point_cloud["elevation"] = data1
        surf = point_cloud.delaunay_2d()
        # point_cloud.plot(render_points_as_spheres=True)
        surf.save(glob_path + 'vtk/' + file_list_jpg1[k] + '.vtk')
        np.savetxt(glob_path + 'vtk/' + file_list_jpg1[k] + '.txt',data1)
        plotter = pv.Plotter(off_screen=True)
        plotter.add_mesh(surf,render_points_as_spheres=True)
        plotter.show(screenshot= glob_path+'screenshot/' + file_list_jpg1[k] + '_3D.png',auto_close=True)
    #class 6 (천공)
    elif int(file_class_jpg[k]) == 6:
        for i in range(0,reshaped_gi1.shape[0]):
            for j in range (int((reshaped_gi1.shape[1])/2)+1, reshaped_gi1.shape[1]):
                reshaped_list_6.append([(-150*(reshaped_gi1[i][j]+mean_z)+15*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/222,j,-i])
        reshaped_polydata1 = np.array(reshaped_list_6)
        point_cloud = pv.PolyData(reshaped_polydata1)
        np.allclose(reshaped_polydata1, point_cloud.points)
        data1 = reshaped_polydata1[:,0]
        point_cloud["elevation"] = data1
        surf = point_cloud.delaunay_2d()
        # point_cloud.plot(render_points_as_spheres=True)
        surf.save(glob_path + 'vtk/' + file_list_jpg1[k] + '.vtk')
        np.savetxt(glob_path + 'vtk/' + file_list_jpg1[k] + '.txt',data1)
        plotter = pv.Plotter(off_screen=True)
        plotter.add_mesh(surf,render_points_as_spheres=True)
        plotter.show(screenshot= glob_path +'screenshot/'+ file_list_jpg1[k] + '_3D.png',auto_close=True)


for k in range(0,len(file_list_png1)):
    reshaped_list_og = []
    reshaped_list_0 = []
    reshaped_list_1 = []
    reshaped_list_2 = []
    reshaped_list_3 = []
    reshaped_list_5 = []
    reshaped_list_6 = []
    img = Image.open(glob_path+ '2d/' + file_list_png1[k] + '.jpg').convert("L")
    grayimg1 = np.asarray(img.getdata()).reshape(img.size[1], img.size[0], -1)
    reshaped_gi1 = grayimg1.reshape(img.size[1],img.size[0])
    mean_z = np.mean(reshaped_gi1[:,int(img.size[0]/2):])
    standard_z = np.std(reshaped_gi1[:,int(img.size[0]/2):])
    mean_z1 = np.mean(reshaped_gi1[:,:int(img.size[0]/2)-1])
    standard_z1 = np.std(reshaped_gi1[:,:int(img.size[0]/2)-1])
    print(glob_path + file_list_png1[k] + '.jpg')
    print('mean_z: ', mean_z)
    print('mean_z1 :', mean_z1)
    
    #Original Plot
    # for i in range(0,reshaped_gi1.shape[0]):
        # for j in range (0, reshaped_gi1.shape[1]):
            # reshaped_list_og.append([i,j,reshaped_gi1[i][j]])
    # reshaped_polydata1 = np.array(reshaped_list_og)
    # point_cloud = pv.PolyData(reshaped_polydata1)
    # np.allclose(reshaped_polydata1, point_cloud.points)
    # data1 = reshaped_polydata1[:,-1]
    # point_cloud["elevation"] = data1
    # # point_cloud.plot(render_points_as_spheres=True)
    #class 0 (균열)
    if int(file_class_png[k]) == 0:
        for i in range(0,reshaped_gi1.shape[0]):
            for j in range (int((reshaped_gi1.shape[1])/2)+1, reshaped_gi1.shape[1]):
                reshaped_list_0.append([i,j,(100*(reshaped_gi1[i][j]+mean_z)+30*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/222])
        reshaped_polydata1 = np.array(reshaped_list_0)
        point_cloud = pv.PolyData(reshaped_polydata1)
        np.allclose(reshaped_polydata1, point_cloud.points)
        data1 = reshaped_polydata1[:,-1]
        point_cloud["elevation"] = data1
        surf = point_cloud.delaunay_2d()
        # point_cloud.plot(render_points_as_spheres=True)
        surf.save(glob_path + 'vtk/' + file_list_png1[k] + '.vtk')
        np.savetxt(glob_path + 'vtk/' + file_list_png1[k] + '.txt',data1)
        plotter = pv.Plotter(off_screen=True)
        plotter.add_mesh(surf,render_points_as_spheres=True)
        plotter.show(screenshot= glob_path+'screenshot/' + file_list_png1[k] + '_3D.png',auto_close=True)
    #class 1 (연결관돌출)
    elif int(file_class_png[k]) == 1:
        for i in range(0,reshaped_gi1.shape[0]):
            for j in range (int((reshaped_gi1.shape[1])/2)+1, reshaped_gi1.shape[1]):
                reshaped_list_1.append([i,j,(-175*(reshaped_gi1[i][j]-mean_z)+30*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/145+mean_z])
        reshaped_polydata1 = np.array(reshaped_list_1)
        point_cloud = pv.PolyData(reshaped_polydata1)
        np.allclose(reshaped_polydata1, point_cloud.points)
        data1 = reshaped_polydata1[:,-1]
        point_cloud["elevation"] = data1
        surf = point_cloud.delaunay_2d()
        # point_cloud.plot(render_points_as_spheres=True)
        surf.save(glob_path + 'vtk/' + file_list_png1[k] + '.vtk')
        np.savetxt(glob_path + 'vtk/' + file_list_png1[k] + '.txt',data1)
        plotter = pv.Plotter(off_screen=True)
        plotter.add_mesh(surf,render_points_as_spheres=True)
        plotter.show(screenshot= glob_path +'screenshot/'+ file_list_png1[k] + '_3D.png',auto_close=True)
    #class 2 (연결관 접합부 이상)
    elif int(file_class_png[k]) == 2:
        for i in range(0,reshaped_gi1.shape[0]):
            for j in range (int((reshaped_gi1.shape[1])/2)+1, reshaped_gi1.shape[1]):
                reshaped_list_2.append([(150*(reshaped_gi1[i][j]+mean_z)-15*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/180,j,-i])
        reshaped_polydata1 = np.array(reshaped_list_2)
        point_cloud = pv.PolyData(reshaped_polydata1)
        np.allclose(reshaped_polydata1, point_cloud.points)
        data1 = reshaped_polydata1[:,0]
        point_cloud["elevation"] = data1
        surf = point_cloud.delaunay_2d()
        # point_cloud.plot(render_points_as_spheres=True)
        surf.save(glob_path + 'vtk/' + file_list_png1[k] + '.vtk')
        np.savetxt(glob_path + 'vtk/' + file_list_png1[k] + '.txt',data1)
        plotter = pv.Plotter(off_screen=True)
        plotter.add_mesh(surf,render_points_as_spheres=True)
        plotter.show(screenshot= glob_path +'screenshot/'+ file_list_png1[k] + '_3D.png',auto_close=True)
    #class 3 (이음부 이탈)
    elif int(file_class_png[k]) == 3:
        for i in range(0,reshaped_gi1.shape[0]):
            for j in range (int((reshaped_gi1.shape[1])/2)+1, reshaped_gi1.shape[1]):
                reshaped_list_3.append([i,j,(100*(reshaped_gi1[i][j]+mean_z)-30*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/130])
        reshaped_polydata1 = np.array(reshaped_list_3)
        point_cloud = pv.PolyData(reshaped_polydata1)
        np.allclose(reshaped_polydata1, point_cloud.points)
        data1 = reshaped_polydata1[:,-1]
        point_cloud["elevation"] = data1
        surf = point_cloud.delaunay_2d()
        # point_cloud.plot(render_points_as_spheres=True)
        surf.save(glob_path + 'vtk/' + file_list_png1[k] + '.vtk')
        np.savetxt(glob_path + 'vtk/' + file_list_png1[k] + '.txt',data1)
        plotter = pv.Plotter(off_screen=True)
        plotter.add_mesh(surf,render_points_as_spheres=True)
        plotter.show(screenshot= glob_path +'screenshot/'+ file_list_png1[k] + '_3D.png',auto_close=True)
    #class 5 (표면손상)
    elif int(file_class_png[k]) == 5:
        for i in range(0,reshaped_gi1.shape[0]):
            for j in range (int((reshaped_gi1.shape[1])/2)+1, reshaped_gi1.shape[1]):
                if reshaped_gi1[i][j-int(img.size[0]/2)] < (mean_z1 * 0.5):
                    reshaped_list_5.append([i,j,(175*(reshaped_gi1[i][j]-mean_z)-30*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/145+mean_z])
                else:
                    reshaped_list_5.append([i,j,(100*(reshaped_gi1[i][j]-mean_z)+70*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/200+mean_z])
        reshaped_polydata1 = np.array(reshaped_list_5)
        point_cloud = pv.PolyData(reshaped_polydata1)
        np.allclose(reshaped_polydata1, point_cloud.points)
        data1 = reshaped_polydata1[:,-1]
        point_cloud["elevation"] = data1
        surf = point_cloud.delaunay_2d()
        # point_cloud.plot(render_points_as_spheres=True)
        surf.save(glob_path + 'vtk/' + file_list_png1[k] + '.vtk')
        np.savetxt(glob_path + 'vtk/' + file_list_png1[k] + '.txt',data1)
        plotter = pv.Plotter(off_screen=True)
        plotter.add_mesh(surf,render_points_as_spheres=True)
        plotter.show(screenshot= glob_path+'screenshot/' + file_list_png1[k] + '_3D.png',auto_close=True)
    #class 6 (천공)
    elif int(file_class_png[k]) == 6:
        for i in range(0,reshaped_gi1.shape[0]):
            for j in range (int((reshaped_gi1.shape[1])/2)+1, reshaped_gi1.shape[1]):
                reshaped_list_6.append([(-150*(reshaped_gi1[i][j]+mean_z)+15*(reshaped_gi1[i][j-int(img.size[0]/2)]-mean_z1))/222,j,-i])
        reshaped_polydata1 = np.array(reshaped_list_6)
        point_cloud = pv.PolyData(reshaped_polydata1)
        np.allclose(reshaped_polydata1, point_cloud.points)
        data1 = reshaped_polydata1[:,0]
        point_cloud["elevation"] = data1
        surf = point_cloud.delaunay_2d()
        # point_cloud.plot(render_points_as_spheres=True)
        surf.save(glob_path + 'vtk/' + file_list_png1[k] + '.vtk')
        np.savetxt(glob_path + 'vtk/' + file_list_png1[k] + '.txt',data1)
        plotter = pv.Plotter(off_screen=True)
        plotter.add_mesh(surf,render_points_as_spheres=True)
        plotter.show(screenshot= glob_path +'screenshot/'+ file_list_png1[k] + '_3D.png',auto_close=True)