import sqlite3
from PIL import Image
import base64
from io import BytesIO

conn = sqlite3.connect('/home/blushy/flowtracker/db.sqlite3', isolation_level=None)
cursor = conn.cursor()

buffer = BytesIO()
im = Image.open('./media/sliceimage_cb/1/mapo_2021020_9.png')
im.save(buffer, format='jpeg')
img_str = base64.b64encode(buffer.getvalue())
#print(img_str)

cursor.execute("insert into Images('name','image') values('mapo_2021020_9',img_str)")

conn.commit()
