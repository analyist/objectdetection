import cv2
import img

#img = cv2.imread('lena.png')
cap = cv2.VideoCapture("http://192.168.1.121:8080/video")
cap.set(3, 640)
cap.set(4, 480)

classNames= []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configpath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightspath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightspath, configpath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

while True:
    sucess,img = cap.read()
    classIds, confs, bbox = net.detect (img,confThreshold=0.5)
    print(classIds,bbox)

    if len(classIds) != 0:
     for classId,confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
      cv2.rectangle(img,box,color=(0,400,0),thickness=5)
      cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

    cv2.imshow("output", img)
    cv2.waitKey(1)

