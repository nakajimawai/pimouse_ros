#!/usr/bin/python
import socket
from PIL import Image
import io
import pickle

PORT = 5000

HOST = "192.168.11.25"
#HOST = "127.0.0.1"

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

sock.bind((HOST,PORT))

img = Image.open("/home/ubuntu/Pictures/cameratest.png").resize((300, 300))

#change to BytosIo
img_io = io.BytesIO()
img.save(img_io, format="PNG")
#I make object linear
img_bytes = pickle.dumps(img)
#sending
sock.sendto(img_bytes, (HOST, PORT))
