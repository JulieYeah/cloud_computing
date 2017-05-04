from PIL import Image
from os import listdir
from os.path import isfile,join
import numpy as np


def ConvertImgVec(LabelPath,FilePath):
    VectorStr = ""
    size=(100,100)
    label = [x for x in listdir(LabelPath)]
    for index,x in enumerate(label):
        ImgPath = LabelPath+"/"+str(x)+"/"
        filenames = [x for x in listdir(ImgPath) if x[-1:-5:-1]=="gpj."]
        for i in filenames:
            img_file = Image.open(ImgPath+i)
            img_file.thumbnail(size)
            new_img_file = img_file.crop((0,0,30,30))
            # img_file.save("/Users/neo/Developer/test/" + str(i), "JPEG")
            img_grey = new_img_file.convert('L')
            value = np.asarray(img_grey.getdata(), dtype=np.int16).reshape((img_grey.size[1], img_grey.size[0]))
            value = np.append(index,value).tolist()
            valueStr = ' '.join(str(v) for v in value)
            VectorStr = VectorStr+valueStr + "\n"
    Vectxt = open(FilePath,'w')
    Vectxt.write(VectorStr)


# ConvertImgVec("/Users/neo/Downloads/thumbnails_features_deduped_sample","/Users/neo/Developer/cloud_computing/cloud_pre/sample_svm.txt")
file = open("/Users/neo/training_vector.txt", 'r')
for x in file:
    values = [i for i in x.split(',')]
    print(len(values),values[1])

