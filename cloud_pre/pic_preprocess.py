#!/usr/bin/python2

"""pictures pre-processing from .jpg to vectors in .txt"""

from os import remove
from os import listdir
from glob import glob
import numpy as np
import cv2
from PIL import Image
from time import time

root_folder_test = 'training_test/'
root_folder = 'training/'
cascPath = 'cvdata/haarcascades/haarcascade_frontalface_default.xml'
output = 'training_vector.txt'

def cvtPic2Vector(img, label, FilePath):
    """convert img to vector and save into FilePath"""

    imagePath = img
    faceCascade = cv2.CascadeClassifier(cascPath)

    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    if len(faces) is not 1:
        return
    size = (30, 30)
    x, y, w, h = faces[0]
    face = cv2.resize(image[y : y + h, x : x + w], size)

    #  VectorStr = ""
    img_file = Image.fromarray(face, mode='RGB')
    img_grey = img_file.convert('L')
    value = np.asarray(img_grey.getdata(), dtype=np.int16).reshape((img_grey.size[1], img_grey.size[0]))
    value = np.append(label, value).tolist()
    valueStr = ','.join(value)
    with open(FilePath, 'a') as f:
        f.write(valueStr + "\n")

if __name__ == "__main__":

    if 'training_vector.txt' in listdir('.'):
        remove('training_vector.txt')

    folders = glob(root_folder + '*')
    i = 0
    for folder in folders[2:]:
        starttime = time()
        i += 1
        for pic in glob(folder + '/*.jpg'):
            name = pic.split('/')[1]
            cvtPic2Vector(pic, name, output)
        endtime = time()
        print str(i) + ' use time: ' + str(endtime-starttime)
