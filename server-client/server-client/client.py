from cv2 import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import os
import imutils

frame_number = 0
prevUpdateCounter = 0  # prev 5th frame will be this one
prevFrame = None
compFrame = None
bounding_boxes = []


def ImageSegmentation(frame, count):
  # path is the video directory for which we are applying the segementation
    # any motion box of less than this size will be a noise #(assumption, to not consider, light changes as motion)
    min_size_area = 50
    cv2.imshow("frame", frame)
    frame_number = count
    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if frame is None:
        print("Frame not readed or frame read ends")
        return 0
    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)  # must be odd
    # if the first frame is None, initialize it
    if compFrame is None:
        compFrame = gray
        return 0
    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(compFrame, gray)
    if frame_number-prevUpdateCounter == 10:
        compFrame = prevFrame
        prevUpdateCounter = frame_number
        prevFrame = gray
        return 0
    prevFrame = gray
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(
        thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    temp = 0
    # loop over the contours
    for c in cnts:
        if cv2.contourArea(c) < min_size_area:
            continue
        temp = 1
    if temp == 1:
        bounding_boxes.append(frame_number)
        return 1

    return 0


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 8485))
connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)

cam.set(3, 320)
cam.set(4, 240)

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
#    data = zlib.compress(pickle.dumps(frame, 0))
    state = ImageSegmentation(frame, img_counter)
    if state==0:
        continue
    data = pickle.dumps(frame, 0)
    size = len(data)

    print("frame = {} and size = {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1
    #just as a termination condition
    if img_counter>800:
        break

cam.release()
