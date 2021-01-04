import socket
import sys
import os
from cv2 import cv2
import pickle
import numpy as np
import struct ## new
import zlib

HOST = ''
PORT=8485

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn,addr=s.accept()

data = b""
count=0
directory_images="output"
parent_dir = "C:/Users/Ganes/Desktop/Intern/server-client"           #do change path here and in above line
path_new = os.path.join(parent_dir, directory_images)
os.mkdir(path_new)
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))

while True:
    while len(data) < payload_size:
        print("Recv: {}".format(len(data)))
        data += conn.recv(4096)

    print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow('ImageWindow',frame)
    name = "frame" + str(count) +".jpg"
    image_path = path_new + "/" + name
    cv2.imwrite(filename = image_path, img = frame)
    count=count+1
    cv2.waitKey(1)
