import cv2

imagePath = 'demo4.jpg'
cascPath = 'cvdata/haarcascades/haarcascade_frontalface_default.xml'

faceCascade = cv2.CascadeClassifier(cascPath)

image= cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(100,100),
    flags = cv2.cv.CV_HAAR_SCALE_IMAGE
)

print "Found {0} faces!".format(len(faces))
print faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 255, 0), 0)
    image1 = image[y:y+h,x:x+w]
    cv2.imshow("Faces found",image1)



cv2.imwrite("face_lu4.jpg",image1)
cv2.waitKey(0)
