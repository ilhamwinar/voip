#!/usr/bin/env python
import pyaudio
import socket
import ast
import time
import logging
import sys

file_handler = logging.FileHandler(filename='/home/ntp/Musik/voip/server_service.log')
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s [%(levelname)s] - %(message)s',
    handlers=handlers,
    datefmt="%m/%d/%Y %H:%M:%S",
)

logger = logging.getLogger('LOGGER_NAME')

f = open("/home/ntp/Musik/voip/config_server.txt", 'r')
api=f.read()
dictapi = ast.literal_eval(api)
ip_server=dictapi["ip_server"]
port=dictapi["port"]

# Pyaudio Initialization
chunk = 1024
pa = pyaudio.PyAudio()

# Opening of the audio stream
stream = pa.open(format = 8,
                channels = 1,
                rate = 10240,
                output = True)

# Socket Initialization
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # For using same port again

s.bind((str(ip_server), port))
size = 1024
s.listen(5)

logger.info("PROGRAM START TO RUN, CONNECTED TO "+str(ip_server))

while True:
    path = "/home/ntp/Musik/voip/temp.txt"
    baca = open(path, 'r+')
    status = baca.read()
    baca.close()

    if status=="0":
        logger.info("MODE VOIP ACTIVE")
        #cek temp.txt status
        path = "/home/ntp/Musik/voip/temp.txt"
        baca = open(path, 'r+')
        status = baca.read()
        baca.close()

        if status=="1":
            logger.info("MODE VOIP NOT ACTIVE, STATUS CHANGED TO 1, FIRST AFTER STATUS 0")
            client.close()
            time.sleep(1)
            continue

        #cek koneksi client
        client, address = s.accept()

        #cek temp.txt status
        path = "/home/ntp/Musik/voip/temp.txt"
        baca = open(path, 'r+')
        status = baca.read()
        baca.close()


        if status=="1":
            logger.info("MODE VOIP NOT ACTIVE, STATUS CHANGED TO 1, SECOND AFTER STATUS 0")
            client.close()
            time.sleep(1)
            continue 

        logger.info('SERVER RUNNING')
 
        while True:

            data = client.recv(size)
            logger.info(data)
            check_data=str(data)

            if data:
                stream.write(data)  # Stream the recieved audio data
                path = "/home/ntp/Musik/voip/temp.txt"
                baca = open(path, 'r+')
                status = baca.read()
                baca.close()
                if status=="0":
                    logger.info("MODE VOIP ACTIVE")
                    continue
                elif status=="1":
                    logger.info("MODE VOIP NOT ACTIVE, STATUS CHANGED TO 1")
                    client.close()
                    time.sleep(1)
                    break
            if check_data=="b''":
                logger.info("CLIENT CLOSED, NO DATA CLIENT EXIST")
                client.close()
                time.sleep(2)
                break

    elif status=="1":
        logger.info("MODE VOIP NOT ACTIVE")
        logger.info("MODE VOIP NOT ACTIVE, MAIN PROGRAM, STATUS CHANGED TO 1")
        try:
            client.close()
        except:
            pass
        time.sleep(1)
        continue


# s.bind(("172.16.12.132", 8003))
# size = 1024
# s.listen(5)
# logging.info("****")
# client, address = s.accept()
# logging.info(s)
# logging.info('running')
# logging.info(client)
# logging.info('Server Running...')
# logging.info(address)

# while True:
#         data = client.recv(size)
#         logging.info(type(data))

#         logging.info(data)
#         logging.info("*******")
#         check_data=str(data)
#         logging.info(type(check_data))
#         logging.info(check_data)
#         logging.info("*******")
#         if data:
#             stream.write(data)  # Stream the recieved audio data
#             logging.info("halo")

#             path = "/home/ntp/Musik/voip/temp.txt"
#             baca = open(path, 'r+')
#             status = baca.read()
#             baca.close()
#             logging.info(status)
#             if status=="0":
#                 logging.info("MODE VOIP ACTIVE")
#                 continue
#             elif status=="1":
#                 logging.info("MODE VOIP NOT ACTIVE")
#                 time.sleep(1)
#                 break
            
#             # client.send(b'ACK')  # Send back Acknowledgement, has to be in binary form
            
#         if check_data=="b''":
#             logging.info("kesini woy")
#             time.sleep(5)
#             continue

# client.close()
# stream.close()
# pa.terminate()
# logging.info("Server has stopped running")
