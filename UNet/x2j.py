### xml to csv
import cv2
import os
import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np
import json
import base64


def xml2csv(xml_path):
    """Convert XML to CSV
    Args:
        xml_path (str): Location of annotated XML file
    Returns:
        pd.DataFrame: converted csv file
    """
    xml_path = '/home/blushy/UNet_CE/x2j_data/Crack_Long_1.xml'
    xml_csv=xml2csv(xml_path)
    print("xml to csv {}".format(xml_path))
    xml_list= []
    xml_df=pd.DataFrame()
    try:
        tree= ET.parse(xml_path)
        root= tree.getroot()
        for member in root.findall('object'):
            value= (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
            column_name= ['filename', 'nrows', 'ncols', 'class', 'x', 'y']
            xml_df= pd.DataFrame(xml_list, columns=column_name)
    except Exception as e:
        print('xml conversion failed:{}'.format(e))
        return pd.DataFrame(columns=['filename,nrows,ncols','class','x','y'
    return xml_df



def df2labelme(symbolDict,image_path,image):
    """ convert annotation in CSV format to labelme JSON
    Args:
        symbolDict (dataframe): annotations in dataframe
        image_path (str): path to image
        image (np.ndarray): image read as numpy array
    Returns:
        JSON: converted labelme JSON
    """

    image_path='home/blushy/UNet_CE/x2j_data/Crack_Long_1.jpg'
    image=cv2.imread(image_path)
    csv_json=df2labelme(xml_csv,image_path,image)


    try:
        symbolDict['min']= symbolDict[['x','y'()
        symbolDict['max']= symbolDict[['xmax','ymax']].values.tolist()
        symbolDict['points']= symbolDict[['min','max']].values.tolist()
        symbolDict['shape_type']='rectangle'
        symbolDict['group_id']=None
        ncols,nrows,_=image.shape
        symbolDict['ncols']=ncols
        symbolDict['nrows']=nrows
        encoded= base64.b64encode(open(image_path, "rb").read())
        symbolDict.loc[:,'imageData']= encoded
        symbolDict.rename(columns= {'class':'label','filename':'imagePath','ncols':'imagencols','nrows':'imagenrows'},inplace=True)
        converted_json= (symbolDict.groupby(['imagePath','imagenrows','imagencols','imageData'], as_index=False)
                     .apply(lambda x: x[['label','points','shape_type','group_id']].to_dict('r'))
                     .reset_index()
                     .rename(columns={0:'shapes'})
                     .to_json(orient='records'))
        converted_json= json.loads(converted_json)[0]
    except Exception as e:
        converted_json={}
        print('error in labelme conversion:{}'.format(e))
    return converted_json