from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from configparser import ConfigParser
import requests
import asyncio
import json

config=ConfigParser()
config.read('pishock.cfg')

APIKEY=config['API']['APITOKEN']
USERNAME=config['API']['USERNAME']
NAME=config['API']['APPNAME']
pets=config['PETS']['PETS'].split()
touchpoints=config['TOUCHPOINTS']['TOUCHPOINTS'].split()



verbose=0
funtype="2"
fundelaymax="10"
fundelaymin="0"
funduration="15"
funintensity="0"
funtouchpointstate="False"
boolsend='False'
typesend="beep"


def set_verbose(address, *args):
    piverbose=str({args})
    cleanverbose=''.join((x for x in piverbose if x.isdigit()))
    global verbose
    verbose=int(cleanverbose)

#Pet functions
def set_target(address, *args):
    global funtarget
    global pets
    pitarget=str({args})
    cleantarget=''.join((x for x in pitarget if x.isdigit()))
    arratarget=int(cleantarget)
    funtarget=pets[arratarget]
    #print(f"target set to {funtarget}")

def set_pet_type(adress, *args):
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

    #print(funtype)

def set_pet_intensity(address, *args):
    piintensity=str({args})
    global funintensity
    global verbose
    tempintensity=str(piintensity.strip("{()},")[:4])
    floatintensity=float(tempintensity)
    intensity=floatintensity*100
    funintensity=int(intensity)

    #print(funintensity)

def set_pet_duration(address, *args):
    piduration=str({args})
    global funduration
    global verbose
    cleanduration=str(piduration.strip("{()},")[:4])
    floatduration=float(cleanduration)
    time=floatduration*15
    funduration=int(time)
    #print(funduration)
    #print(cleanduration)

def set_pet_state(address:str, *args) -> None:
    global boolsend
    global verbose
    booltest=str({args})
    boolsend= ''.join((x for x in booltest if x.isalpha()))

    #print(boolsend)

#TouchPointFunctions
def set_touchpoint(address, *args):
    global funtouchpoint
    global funtouchpointstate
    pitouchpointstate=str({args})
    cleantouchpointstate=''.join((x for x in pitouchpointstate if x.isalpha()))
    if cleantouchpointstate == "True":
        pitouchpoint=str({address})
        cleantouchpoint=''.join((x for x in pitouchpoint if x.isdigit()))
        touchpointtarget=int(cleantouchpoint)
        funtouchpoint=touchpoints[touchpointtarget]
        funtouchpointstate=cleantouchpointstate
    if cleantouchpointstate == "False":
        funtouchpointstate=cleantouchpointstate

    #print(funtouchpoint)
    #print(funtouchpointstate)

def set_TP_type(adress, *args):
    piTPtype=str({args})
    global funTPtype
    global typeTPsend
    global verbose
    funTPtype= ''.join((x for x in piTPtype if x.isdigit()))
    if funTPtype == '0':
        typeTPsend="shock"
    if funTPtype == '1':
        typeTPsend="vibrate"
    if funTPtype == '2':
        typeTPsend="beep"

    #print(funTPtype)

def set_TP_intensity(address, *args):
    piTPintensity=str({args})
    global funTPintensity
    global verbose
    tempTPintensity=str(piTPintensity.strip("{()},")[:4])
    floatTPintensity=float(tempTPintensity)
    TPintensity=floatTPintensity*100
    funTPintensity=int(TPintensity)

    #print(funTPintensity)

def set_TP_duration(address, *args):
    piTPduration=str({args})
    global funTPduration
    global verbose
    cleanTPduration=str(piTPduration.strip("{()},")[:4])
    floatTPduration=float(cleanTPduration)
    TPtime=floatTPduration*15
    funTPduration=int(TPtime)

    #print(cleanTPduration)
    #print(funTPduration)

dispatcher = Dispatcher()
#dispatchers for pet functions
dispatcher.map("/avatar/parameters/pishock/Type", set_pet_type)
dispatcher.map("/avatar/parameters/pishock/Intensity", set_pet_intensity)
dispatcher.map("/avatar/parameters/pishock/Duration", set_pet_duration)
dispatcher.map("/avatar/parameters/pishock/Shock", set_pet_state)
dispatcher.map("/avatar/parameters/pishock/Target", set_target)
#dispatchers for touchpoint functions
dispatcher.map("/avatar/parameters/pishock/TPType", set_TP_type)
dispatcher.map("/avatar/parameters/pishock/TPIntensity", set_TP_intensity)
dispatcher.map("/avatar/parameters/pishock/TPDuration", set_TP_duration)
dispatcher.map("/avatar/parameters/pishock/Touchpoint_*", set_touchpoint)
#verbose functions
dispatcher.map("/avatar/parameters/pishock/Debug", set_verbose)

ip=config['Settings']['IP']
port=config['Settings']['Port']

async def loop():
    #i suck at this, import all values from other functions
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
    global funtarget
    global funtouchpoint
    global typeTPsend
    global funTPtype
    global funTPduration
    global funTPintensity
    
    # set default values if not set
    funtype = 3 if funtype is None else funtype
    funduration = 0 if funduration is None else funduration
    funintensity = 0 if funintensity is None else funintensity
    funtarget = 0 if funtarget is None else funtarget
    funTPtype = 3 if funTPtype is None else funTPtype
    funTPduration = 0 if funTPduration is None else funTPduration
    funTPintensity = 0 if funTPintensity is None else funTPintensity
    
    await asyncio.sleep(0.1)
    if boolsend == 'True':
        sleeptime=funduration+0.5
        print(f"sending {typesend} at {funintensity} for {funduration} seconds")
        datajson = str({"Username":USERNAME,"Name":NAME,"Code":funtarget,"Intensity":funintensity,"Duration":funduration,"Apikey":APIKEY,"Op":funtype})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        sendrequest=requests.post('https://do.pishock.com/api/apioperate', data=datajson, headers=headers)

        print(f"waiting {sleeptime} before next command")
        #print(sendrequest)
        #print (sendrequest.text)

        await asyncio.sleep(sleeptime)

    if funtouchpointstate == 'True':
        sleeptime=funTPduration+1.7
        print(f"touch point sending {typeTPsend} at {funTPintensity} for {funTPduration} seconds")
        datajson = str({"Username":USERNAME,"Name":NAME,"Code":funtouchpoint,"Intensity":funTPintensity,"Duration":funTPduration,"Apikey":APIKEY,"Op":funTPtype})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        sendrequest=requests.post('https://do.pishock.com/api/apioperate', data=datajson, headers=headers)

        print(f"waiting {sleeptime} before next command")
        #print(sendrequest)
        #print (sendrequest.text)

        await asyncio.sleep(sleeptime)


async def init_main():
    server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()

    while True:
        await loop()

    transport.close()


asyncio.run(init_main())
