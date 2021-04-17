import os
from fastapi import FastAPI, Request
from fastapi.logger import logger
from starlette import status
from starlette.responses import Response
from datetime import datetime
import socket
import json
import uvicorn
import threading
import time

THRESHOLD = int(os.getenv("THRESHOLD"))
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
value = 0
status = ""


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((HOST, PORT))
except socket.error as e:
    logger.error(f"Socket connection error, host={HOST} port={PORT}", exc_info=True)


def send_data():
    global status
    while True:
        if status:
            time_now = datetime.now()
            dt = time_now.strftime("%Y/%m/%d %H:%M:%s")
            request_data = json.dumps(
                {"datetime": time_now.strftime("%Y%m%d%H%M"), "status": status}
            )
            sock.sendall(bytes(request_data, encoding="utf-8"))
            logger.warning(f"{status} is sent to controller on {dt}")

            value = 0
        time.sleep(5)


def process_data(data):
    global value
    global status

    dt = data.get("datetime", datetime.now().strftime("%Y%m%d%H%M"))
    value += data.get("payload")
    status = "up" if (value % THRESHOLD * 2) > THRESHOLD else "down"


app = FastAPI()


@app.post("/submit_data/")
async def release(request: Request):
    json_param = await request.json()
    process_data(json_param)

    return Response(status_code=200)


if __name__ == "__main__":
    x = threading.Thread(target=send_data, daemon=True)
    x.start()
    logger.warning("Thread send_data is started")
    uvicorn.run(app, host="0.0.0.0", port=8080)
