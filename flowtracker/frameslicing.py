import cv2
import os
import os.path

glob_path = "/home/blushy/flowtracker/media/Uploaded Files/"
file_list = os.listdir(glob_path)
file_list_mp4 = [file for file in file_list if file.endswith(".mp4")]
file_list_mp41 = []
for i in range(0,len(file_list_mp4)):
    #데이터 이름만 추출
    file_list_mp41.append(file_list_mp4[i].split('.mp')[0])
    
savepath = "/home/blushy/flowtracker/media/sliceimage/1/"
for j in range(0,len(file_list_mp41)):
    path = glob_path + file_list_mp41[j] + '.mp4'
    videocap = cv2.VideoCapture(path)
    a = videocap.get(cv2.CAP_PROP_FPS)
    b = videocap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(a)
    print(b)
    count = 1
    frame = 1
    while(videocap.isOpened()):
        ret, image = videocap.read() 
        # 이미지 사이즈 변환
        #image = cv2.resize(image, (960, 540)) 
        if frame == b:
            quit()
        #몇프레임당 이미지 하나씩 추출할껀지 선택 (여기는 30이 초당 1, 60이 2초당 1)
        if(int(videocap.get(1)) % a == 0): 
            print('Saved frame number : ' + str(int(videocap.get(1)))) 
        
            # 추출된 이미지저장
            cv2.imwrite(savepath + file_list_mp41[j] + "_" + '{0:04}'.format(count) +".png" , image) 
            count += 1
        frame += 1
