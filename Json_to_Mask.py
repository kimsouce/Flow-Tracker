#Json 에서 Mask 생성 코드
import json
import cv2
import numpy as np
import os
import shutil
import argparse
 
 # json, image, path 경로 및 이미지 색깔 추출
def cvt_one(json_path, img_path, save_path, label_color):
    data = json.load(open(json_path,encoding='gbk'))
    img = cv2.imread(img_path)
 
    # 배경 이미지 생성
    # mask 이미지의 넓이, 길이는 기준이되는 원본 이미지파일의 크기에 따라 설정함
    img_h = data['imageHeight']
    img_w = data['imageWidth']
    # bgr (0,0,0) 으로 검정색 배경 생성
    color_bg = (0, 0, 0)
    points_bg = [(0, 0), (0, img_h), (img_w, img_h), (img_w, 0)]
    img = cv2.fillPoly(img, [np.array(points_bg)], color_bg)
 
    # json 파일에 표기된 경로에 따른 이미지 Mask 이미지 생성
    for i in range(len(data['shapes'])):
        name = data['shapes'][i]['label']
        points = data['shapes'][i]['points']
        # bgr (255,255,255) 로 흰색 Mask 생성
        color =  (255,255,255)
        if label_color:
            img = cv2.fillPoly(img, np.array([points],dtype=np.int32), (color[0], color[1], color[2]))
        else:
            img = cv2.fillPoly(img, np.array([points],dtype=np.int32), (color[0], color[1], color[2]))
    cv2.imwrite(save_path, img)
 

# 세이브 디렉토리 지정 및 폴더생성
if __name__ == '__main__':
    save_dir ='C:/Users/Dell/Desktop/json2mask'
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
#경로는 절대경로로 지정되어있으므로 필요시 변경하여 사용
file_dir = 'C:/Users/Dell/Desktop/main'
files = os.listdir(file_dir)
img_files = list(filter(lambda x: '.jpg' in x, files))
# json 파일 내 label 별 색이 별도로 지정되어있지 않으므로 label_color은 생략
# label_color = 'CL'
save_img='C:/Users/Dell/Desktop/json2mask'
if not os.path.exists(save_img):
    os.makedirs(save_img)
#디렉토리 내 이미지파일 확인 및 각 파일별 json파일 매치
for i in range(len(img_files)):
    img_path = file_dir + '/' + img_files[i]
    shutil.copy(img_path, save_img + '/' + img_files[i])
    json_path = img_path.replace('.jpg', '.json')
    save_path = save_dir + '/' + img_files[i]
    print('Processing {}'.format(img_path))
    cvt_one(json_path, img_path, save_path, label_color)
