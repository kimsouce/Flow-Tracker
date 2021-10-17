import sqlite3
import os

#db insert 부분
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBLOB(cls, loc_date, mp4time, yolo, unet, depth):
    try:
        sqliteConnection = sqlite3.connect('/home/blushy/flowtracker/db.sqlite3')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO images
                                  (cls, loc_date, mp4time, yolo, unet, depth) VALUES (?, ?, ?, ?, ?, ?)"""

        binYolo = convertToBinaryData(yolo)
        binUnet = convertToBinaryData(unet)
        bindepth = convertToBinaryData(depth)
        # Convert data into tuple format
        data_tuple = (cls, loc_date, mp4time, binYolo, binUnet, bindepth)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")

#photo
DIR = "../media/yoloresult/test/crops/"

for files in os.walk(DIR):
    for i in range(len(files[2])):
        insertBLOB(files[2][i][0:1],files[2][i][2:-9], files[2][i][-8:-4], "/home/blushy/flowtracker/media/yoloresult/test/crops/"+files[2][i], "/home/blushy/flowtracker/media/unetresult/"+files[2][i],"/home/blushy/flowtracker/media/3dresult/2d/"+files[2][i])
        i = i+1
        if i == (len(files[2])-1):
            break
