from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
import requests
import asyncio
import json

#change these values
APIKEY="ChangeMe"
SHARECODE="ChangeMe"
USERNAME="ChangeMe"
NAME="vrcosc"
#change to True to see http responses
verbose="0"
#dont touch below
funtype="2"
fundelaymax="10"
fundelaymin="0"
funduration="15"
funintensity="0"
boolsend='False'
typesend="beep"

def set_type(adress, *args):
    pitype=str({args})
    global funtype
    global typesend
    global verbose
    funtype= ''.join((x for x in pitype if x.isdigit()))
    if funtype == '0':
        typesend="shock"
    if funtype == '1':
        typesend="vibrate"
    if funtype == '2':
        typesend="beep"
    if verbose == "1":
        print(funtype)
    

def set_intensity(address, *args):
    piintensity=str({args})
    global funintensity
    global verbose
    tempintensity=str(piintensity.strip("{()},")[:4])
    floatintensity=float(tempintensity)
    intensity=floatintensity*100
    funintensity=int(intensity)
    if verbose == "1":
        print(funintensity)

def set_duration(address, *args):
    piduration=str({args})
    global funduration
    global verbose
    cleanduration=str(piduration.strip("{()},")[:4])
    floatduration=float(cleanduration)
    time=floatduration*15
    funduration=int(time)
    if verbose == "1":
        print(piduration)
    
def set_state(address:str, *args) -> None:
    global boolsend
    global verbose
    booltest=str({args})
    boolsend= ''.join((x for x in booltest if x.isalpha()))
    if verbose == "1":
        print(boolsend)

dispatcher = Dispatcher()
funtype=dispatcher.map("/avatar/parameters/pishock/Type", set_type)
funintensity=dispatcher.map("/avatar/parameters/pishock/Intensity", set_intensity)
funduration=dispatcher.map("/avatar/parameters/pishock/Duration", set_duration)
dispatcher.map("/avatar/parameters/pishock/Shock", set_state)


ip = "127.0.0.1"
port = 9001


async def loop():
    global boolsend
    global verbose
    global funtype
    global funduration
    global funintensity
    global USERNAME
    global NAME
    global SHARECODE
    global APIKEY
    global typesend
    await asyncio.sleep(0.1)
    if boolsend == 'True':
        sleeptime=funduration+1.1
        print(f"sending {typesend} at {funintensity} for {funduration} seconds")
        datajson = str({"Username":USERNAME,"Name":NAME,"Code":SHARECODE,"Intensity":funintensity,"Duration":funduration,"Apikey":APIKEY,"Op":funtype})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        sendrequest=requests.post('https://do.pishock.com/api/apioperate', data=datajson, headers=headers)
        if verbose == "1":
            print(sendrequest)
        await asyncio.sleep(sleeptime)


async def init_main():
    server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()

    while True:
        await loop()

    transport.close()


asyncio.run(init_main())