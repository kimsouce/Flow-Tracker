import os 
import pandas as pd
import csv
import datetime

DIR = "../media/yoloresult/test/crops/"

for files in os.walk(DIR):
    for i in range(len(files[2])):
        first_data = files[2][0][0:1],files[2][0][2:-18],files[2][0][-17:-9]
        df = pd.DataFrame(first_data)
        print(files[2][i][0:1],files[2][i][2:-18],files[2][i][-17:-9])
        data = files[2][i][0:1],files[2][i][2:-18],files[2][i][-17:-9]
        if not data in df:
            df.to_csv('output.csv', index=False, mode='w', encoding='utf-8')
        else:
            df.to_csv('output.csv', index=False, mode='a', encoding='utf-8')
        i = i+1
        if i == (len(files[2])-1):
            break
print(df)
        #print('class: ' + files[2][i][0:1])
    #print(files)
    #print('filename: '+files[2][3])
    #print('class: ' + files[2][3][0:1])
    #print('loc_date: ' +files[2][3][2:-9])
    #print('mp4time: ' +files[2][3][-8:-4])
    #print(range(len(files[2])))
    #print(len(files[2]))
    #print("'"+"/media/yoloresult/test/crops/"+files[2][1]+"'")
