#!/usr/bin/python2

"""pictures pre-processing from .jpg to vectors in .txt"""

from os import remove
import multiprocessing
from os import listdir
from glob import glob
import threading
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

def execute(folders):
    i = 0
    for folder in folders:
        starttime = time()
        for pic in glob(folder + '/*.jpg'):
            name = pic.split('/')[1]
            cvtPic2Vector(pic, i, output)
        i += 1
        endtime = time()
        print str(i) + ' use time: ' + str(endtime-starttime)

if __name__ == "__main__":

    if 'training_vector.txt' in listdir('.'):
        remove('training_vector.txt')

    #  threads = []

    folders = glob(root_folder + '*')
    #  for i in range(1):
    #      t = threading.Thread(target=execute, args=(folders,))
    #      threads.append(t)

    #  for i in range(1):
    #      threads[i].start()

    #  for i in range(1):
    #      threads[i].join()
    execute(folders)
    #  multiprocessing.freeze_support()
    #  pool = multiprocessing.Pool()
    #  cpus = multiprocessing.cpu_count()
    #  results = []
    #  for i in xrange(0, 2):
    #      pool.apply_async(execute, args=(folders,))
    #  pool.close()
    #  pool.join()
