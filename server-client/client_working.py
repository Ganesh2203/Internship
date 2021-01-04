import socket
import cv2
# import sys
# import zipfile
import os

host = '127.0.0.1'
port = 1344

s = socket.socket()
print('[+] Client socket is created.')

s.connect((host, port))
print('[+] Socket is connected to {}'.format(host))

img_ctr = 0
vidobj = cv2.VideoCapture("input2.mp4")

os.mkdir("uploads_client")

while True:
    success, image = vidobj.read()
    if not success:
        break
    name = "frame_c" + str(img_ctr) + ".jpg"
    cv2.imwrite(name, img=image)
    size = os.path.getsize(name)
    print(size, "asdfg")
    s.send(("Hi server").encode('utf-8').strip())
    s.send(str(size).encode('utf-8').strip())

    f = open(name, "rb")
    data = f.read()
    print(len(data), "is data length")
    f.close()
    s.sendall(data)
    img_ctr += 1
    