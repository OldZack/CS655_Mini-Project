#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import sys
import threading

def socket_service():
    """Start Socket service"""
    try:
        s = socket.socket()
        ip = socket.gethostname()
        port = 12345
        s.bind((ip, port))
        s.listen(5)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('Wait connection')
    while True:
        conn, addr = s.accept()
        print("connected")
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()

def deal_data(conn, addr):
    """Running file transfer protocol and recognize image received"""
    print('Accept new connection from {0}'.format(addr))
    filename = open('test_img.jpg', 'wb')
    length = -1
    buffered = 0
    while True:
        data = conn.recv(1024)
        try:
            # Decode data
            string = data.decode("utf-8") 
            # Receive LENGTH info
            if string.startswith("LENGTH"):
                length = int(string.split(" ")[1].strip("\n"))
                buffered = 0
                conn.send(b"LENGTHACK")
                print("Receive LENGTH Msg with content: "+string)
            # Receive data
            else:
                if length == -1:
                    print("Drop invalid message since no known file length")
                    continue
                filename.write(data)
                buffered += len(data)
                if buffered == length:
                    print("Receive the whole image file")
                    break         
        except:
            # Receive data
            if length == -1:
                print("Drop invalid message since no known file length")
                continue
            filename.write(data)
            buffered += len(data)
            if buffered == length:
                print("Receive the whole image file")
                break
    filename.close()

    # recognize image and send back type
    type_recog = "RECOG"+" "+img_recog(filename)
    try:
        conn.send(bytes(type_recog, encoding="utf-8"))
    except:
        conn.close()
    conn.close() 

def img_recog(filename) -> str:
    """Recognize image and return object type"""
    return "human"

if __name__ == '__main__':
    socket_service()
