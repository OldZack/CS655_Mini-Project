#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
 
def request_img_recog(host, port, file_path) -> str:
    """Create Socket connection to request recognition for img file"""
    
    # Connection
    s = socket.socket()                  
    s.connect((host, port))

    # Read binary file
    with open(file_path, "rb") as f:
        data = f.read()
    length_msg = "LENGTH"+" "+str(len(data))

    # Send length info
    s.send(bytes(length_msg,encoding="utf-8"))
    reply = s.recv(1024).decode("utf-8")
    if reply != "LENGTHACK":
        print("Invalid Reply Format")
        print("Received: "+reply)
        print("Expected: "+"LENGTHACK")
        return ""
    print("Received: "+reply)
    
    # Send file data
    s.send(data)
    reply = s.recv(1024).decode("utf-8")
    if not reply.startswith("RECOG"):
        print("Invalid Reply Format")
        print("Received: "+reply)
        print("Expected: "+"RECOG TYPE")
        return ""
    else:
        type_recog = reply.split("\n")[1]
        print("Received Recognition Type: "+type_recog)
    s.close()
    return type_recog

# request_img_recog("pcvm2-16.instageni.uvm.edu", 12345, "dog.jpg")