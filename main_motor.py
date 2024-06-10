from fastapi import Depends, FastAPI, HTTPException, status, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import os
import pygame
import logging
import sys
from pathlib import Path
from datetime import datetime

#defini direktori    
current_dir = os.getcwd()

## FUNGSI UNTUK READ LOG
def write_log(lokasi_log, datalog):
    waktulog = datetime.now()
    dirpathlog = f"Log/{lokasi_log}"
    os.makedirs(dirpathlog, exist_ok=True)
    pathlog = f"{waktulog.strftime('%d%m%Y')}.log"
    file_path = Path(f"{dirpathlog}/{pathlog}")
    datalog = "[INFO] - " + datalog
    if not file_path.is_file():
        file_path.write_text(f"{waktulog.strftime('%d-%m-%Y %H:%M:%S')} - {datalog}\n")
    else :
        fb = open(f"{dirpathlog}/{pathlog}", "a")
        fb.write(f"{waktulog.strftime('%d-%m-%Y %H:%M:%S')} - {datalog}\n")
        fb.close
    
    print(f"{waktulog.strftime('%d-%m-%Y %H:%M:%S')} - {datalog}")

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
    
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(current_dir+"./sound_2.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
        write_log("api", "PLAY SOUND NTP")
        return {"status":"berhasil mode auto"}
    except:
        write_log("api", "GAGAL PLAY SOUND NTP")
        return {"status":"tidak berhasil mode auto"}


# @app.get(("/open_port"))
# async def open_port():
#     os.system("sudo systemctl restart voip_server.service;")
#     logger.info("MENYALAKAN SERVICE SERVER")
#     return {"status_service":"1"}

# @app.get(("/close_port"))
# async def close_port():
#     os.system("sudo systemctl stop voip_server.service;")
#     logger.info("MEMATIKAN SERVICE SERVER")
#     return {"status_service":"0"}

# @app.get("/voip_off")
# async def voip_off():
#     tulis = open(current_dir+'/temp.txt', 'w')
#     n = 1
#     tulis.write(str(n))
#     tulis.close()
#     logger.info("MEMATIKAN SERVICE VOIP")
#     return {"status":"berhasil matikan voip"}

# @app.get("/voip_on")
# async def voip_on():
#     tulis = open(current_dir+'temp.txt', 'w')
#     n = 0
#     tulis.write(str(n))
#     tulis.close()
#     logger.info("MENYALAKAN SERVICE VOIP")
#     return {"status":"berhasil mode voip"}

# @app.get("/status")
# async def status():
#     path = current_dir+'/temp.txt'
#     baca = open(path, 'r')
#     status = baca.read()
#     baca.close()
#     logger.info("GET STATUS API VOIP")
#     return {"status":status}

if __name__ == '__main__':
    uvicorn.run("main_motor:app", host="0.0.0.0", port=8200,log_level="info",reload=True)
