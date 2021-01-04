import socket
# import sys
# import zipfile
# import os
# import cv2
# import tqdm
port = 1344

ss = socket.socket()
print('[+] Server socket is created.')

ss.bind(('', port))
print('[+] Socket is binded to {}'.format(port))

ss.listen(5)
print('[+] Waiting for connection...')

con, addr = ss.accept()
print('[+] Got connection from {}'.format(addr[0]))
img_ctr = 0

while True:
    msg = con.recv(9).decode()
    print(msg)
    filesize = con.recv(6).decode()
    print(type(filesize))
    print(filesize)
    filesize = int(filesize)
    print(filesize, "filesize received", type(filesize))

    name = "frame_s" + str(img_ctr) + ".jpg"

    # progress = tqdm.tqdm(range(filesize), unit="B", unit_scale=True, unit_divisor = 1024)
    f = open(name, "wb")
    bytes_read = con.recv(filesize)
    print("Continuing...")

    
    f.write(bytes_read)
    read_size = len(bytes_read)
    flag = True
    if(read_size >= filesize):
        flag = False
        f.close()
    print(read_size, " && ", filesize)
    # print("File write success...")

    while flag is True:
        print("In while loop")
        filesize = filesize - 65536
        if filesize <= 65536:
            bytes_read = con.recv(filesize)
            flag = False
            f.close()
        else:
            bytes_read = con.recv(65536)
            f.write(bytes_read)

        # now clearing the recv buffer
    img_ctr += 1
    if(img_ctr > 3):
        break
con.close()
ss.close()
