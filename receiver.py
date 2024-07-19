
import cv2
import socket
import pickle
import struct
import numpy as np

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8485))
server_socket.listen(0)

conn, addr = server_socket.accept()

data = b""
payload_size = struct.calcsize("L")

while True:
    while len(data) < payload_size:
        data += conn.recv(4096)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]

    while len(data) < msg_size:
        data += conn.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]
    img_encoded = pickle.loads(frame_data)

    nparr = np.frombuffer(img_encoded, np.byte)
    frame = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

conn.close()
cv2.destroyAllWindows()