

import socket
import sys
import threading
import torch
from torchvision import transforms
import os
from PIL import Image

def socket_service():
    """Start Socket service"""
    try:
        s = socket.socket()
        host = socket.gethostname()
        port = 12345
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('Wait connection...')
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()


def deal_data(conn, addr):
    """Running file transfer protocol and recognize image received"""
    print('Accept new connection from {0}'.format(addr))
    name = 'test_img.jpg'
    filename = open(name, 'wb')
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
    type_recog = "RECOG"+"\n"+recon_pic(name)

    try:
        conn.send(bytes(type_recog, encoding="utf-8"))
    except:
        conn.close()
    conn.close()
    print("=============== Connection Closed ===============")


def recon_pic(filename) -> str:
    model = torch.hub.load('pytorch/vision:v0.10.0', 'googlenet', pretrained=True)
    model.eval()
    img = Image.open(filename)
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(img)
    input_batch = input_tensor.unsqueeze(0)  # create a mini-batch as expected by the model
    # move the input and model to GPU for speed if available
    if torch.cuda.is_available():
        input_batch = input_batch.to('cuda')
        model.to('cuda')
    with torch.no_grad():
        output = model(input_batch)
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    # Read the categories
    with open("class.txt", "r") as f:
        categories = [s.strip() for s in f.readlines()]
    # Show top categories per image
    top5_prob, top5_catid = torch.topk(probabilities, 5)
    # for i in range(top5_prob.size(0)):
    #     print(categories[top5_catid[i]], top5_prob[i].item())
    print(categories[top5_catid[0]])
    os.remove(filename)
    return categories[top5_catid[0]]

if __name__ == '__main__':
    socket_service()