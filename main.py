from fastapi import Depends, FastAPI, HTTPException, status, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import os
import socket
import pygame
import logging
import sys

#defini direktori    
current_dir = os.getcwd()

#inisialisasi logging
file_handler = logging.FileHandler(filename=current_dir+'api_voip.log')
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s [%(levelname)s] - %(message)s',
    handlers=handlers,
    datefmt="%m/%d/%Y %H:%M:%S",
)
logger = logging.getLogger('LOGGER_NAME')

# inisialisasi API
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"])

@app.get("/status_auto")
async def status_auto():
    logger.info("PLAY SOUND NTP")
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("sound_2.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        return {"status":"berhasil mode auto"}
    except:
        logger.error("GAGAL PLAY SOUND")
        return {"status":"tidak berhasil mode auto"}
    logger.info("SELESAI PLAY SOUND")

@app.get(("/open_port"))
async def open_port():
    os.system("sudo systemctl restart voip_server.service;")
    logger.info("MENYALAKAN SERVICE SERVER")
    return {"status_service":"1"}

@app.get(("/close_port"))
async def close_port():
    os.system("sudo systemctl stop voip_server.service;")
    logger.info("MEMATIKAN SERVICE SERVER")
    return {"status_service":"0"}

@app.get("/voip_off")
async def voip_off():
    tulis = open(current_dir+'/temp.txt', 'w')
    n = 1
    tulis.write(str(n))
    tulis.close()
    logger.info("MEMATIKAN SERVICE VOIP")
    return {"status":"berhasil matikan voip"}

@app.get("/voip_on")
async def voip_on():
    tulis = open(current_dir+'temp.txt', 'w')
    n = 0
    tulis.write(str(n))
    tulis.close()
    logger.info("MENYALAKAN SERVICE VOIP")
    return {"status":"berhasil mode voip"}

@app.get("/status")
async def status():
    path = current_dir+'/temp.txt'
    baca = open(path, 'r')
    status = baca.read()
    baca.close()
    logger.info("GET STATUS API VOIP")
    return {"status":status}

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8200,log_level="info",reload=True)