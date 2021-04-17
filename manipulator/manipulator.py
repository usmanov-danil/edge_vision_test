import os
import socket
import json
import logging

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))

logging.basicConfig(filename="/log/manipulator_logs.log", level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        while True:
            data = conn.recv(1024)
            data = json.loads(data.decode("utf-8"))
            logging.info(f"time: {data.get('datetime')}, status: {data.get('status')}")
