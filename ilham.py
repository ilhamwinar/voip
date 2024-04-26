import asyncio
import websockets
import pyaudio
import json
import requests
import time

async def audio_server(websocket, path):

    url = "http://localhost:8200"

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output=True)

    try:

        audio_data = await websocket.recv()
        
        if(audio_data != '') :
            response = requests.get(url+"/voip_on")
        #     seconds = time.time()
        no =1
        while websocket.open:
            # Check if the WebSocket is still open

            try:

                audio_data = await websocket.recv()
                # Play the audio data using PyAudio
                stream.write(audio_data)

                # if (time.time() - start == 180):
                #     response = requests.get(url+"/voip_off")

            except websockets.exceptions.ConnectionClosedError:
                break  # Break the loop if the WebSocket is closed
    except Exception as e:
        # await websocket.close()
        print(f"Error in audio_server: {e}")

    finally:
        try:
            response = requests.get(url+"/voip_off")
            await websocket.close()
        except Exception as e:
            print(f"Error while closing WebSocket connection: {e}")

        try:
            stream.stop_stream()
            stream.close()
            p.terminate()
        except Exception as e:
            print(f"Error while stopping stream: {e}")


start_server = websockets.serve(audio_server, "0.0.0.0", 8767)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
