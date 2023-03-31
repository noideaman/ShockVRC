from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from configparser import ConfigParser
import requests
import asyncio
import json
import os
import PySimpleGUIQt as sg

config_file = 'pishock.cfg'

def setup_wizard():
    config = ConfigParser()

    layout = [
        [sg.Text("Please enter your API token (default: <empty>):"), sg.InputText(key="api_token")],
        [sg.Text("Please enter your username (default: user):"), sg.InputText(default_text="user", key="username")],
        [sg.Text("Please enter your application name (default: MyApp):"), sg.InputText(default_text="MyApp", key="app_name")],
        [sg.Text("Please enter the pets you want to control (comma-separated, default: pet1):"), sg.InputText(default_text="pet1", key="pets")],
        [sg.Text("Please enter the touch points you want to add to your avatar (comma-separated, default: tp1):"), sg.InputText(default_text="tp1", key="touchpoints")],
        [sg.Button("Submit"), sg.Button("Cancel")]
    ]

    window = sg.Window("Setup Wizard", layout)

    while True:
        event, values = window.read()
        if event == "Submit":
            break
        elif event == sg.WIN_CLOSED or event == "Cancel":
            window.close()
            return

    window.close()

    config['API'] = {
        'APITOKEN': values['api_token'],
        'USERNAME': values['username'],
        'APPNAME': values['app_name']
    }

    config['PETS'] = {
        'PETS': values['pets']
    }

    config['TOUCHPOINTS'] = {
        'TOUCHPOINTS': values['touchpoints']
    }

    # Save the configuration to the file
    with open(config_file, 'w') as f:
        config.write(f)

    print("Configuration saved to", config_file)

# Check if the configuration file exists
if not os.path.exists(config_file):
    setup_wizard()

config = ConfigParser()
config.read(config_file)

API_KEY = config['API']['APITOKEN']
USERNAME = config['API']['USERNAME']
APP_NAME = config['API']['APPNAME']
pets = config['PETS']['PETS'].split()
touchpoints = config['TOUCHPOINTS']['TOUCHPOINTS'].split()

verbose = 0
fun_type = "2"
fun_delay_max = "10"
fun_delay_min = "0"
fun_duration = "15"
fun_intensity = "0"
fun_touchpoint_state = "False"
send_enabled = 'False'
type_send = "beep"


def set_verbose(address, *args):
    global verbose
    verbose = int(''.join((x for x in str(args) if x.isdigit())))


# Pet functions
def set_target(address, *args):
    global fun_target
    fun_target = pets[int(''.join((x for x in str(args) if x.isdigit())))]


def set_pet_type(adress, *args):
    global fun_type, type_send
    fun_type = ''.join((x for x in str(args) if x.isdigit()))

    type_send = {
        '0': 'shock',
        '1': 'vibrate',
        '2': 'beep'
    }.get(fun_type)


def set_pet_intensity(address, *args):
    global fun_intensity
    temp_intensity = float(str(args).strip("{()},")[:4])
    fun_intensity = int(temp_intensity * 100)


def set_pet_duration(address, *args):
    global fun_duration
    clean_duration = float(str(args).strip("{()},")[:4])
    fun_duration = int(clean_duration * 15)


def set_pet_state(address: str, *args) -> None:
    global send_enabled
    send_enabled = ''.join((x for x in str(args) if x.isalpha()))


# TouchPoint functions
def set_touchpoint(address, *args):
    global fun_touchpoint, fun_touchpoint_state
    clean_touchpoint_state = ''.join((x for x in str(args) if x.isalpha()))
    if clean_touchpoint_state == "True":
        fun_touchpoint = touchpoints[int(''.join((x for x in str(address) if x.isdigit())))]
        fun_touchpoint_state = clean_touchpoint_state
    if clean_touchpoint_state == "False":
        fun_touchpoint_state = clean_touchpoint_state


def set_TP_type(adress, *args):
    global fun_TP_type, type_TP_send
    fun_TP_type = ''.join((x for x in str(args) if x.isdigit()))

    type_TP_send = {
        '0': 'shock',
        '1': 'vibrate',
        '2': 'beep'
    }.get(fun_TP_type)


def set_TP_intensity(address, *args):
    global fun_TP_intensity
    temp_TP_intensity = float(str(args).strip("{()},")[:4])
    fun_TP_intensity = int(temp_TP_intensity * 100)


def set_TP_duration(address, *args):
    global fun_TP_duration
    clean_TP_duration = float(str(args).strip("{()},")[:4])
    fun_TP_duration = int(clean_TP_duration * 15)


dispatcher = Dispatcher()
# Dispatchers for pet functions
dispatcher.map("/avatar/parameters/pishock/Type", set_pet_type)
dispatcher.map("/avatar/parameters/pishock/Intensity", set_pet_intensity)
dispatcher.map("/avatar/parameters/pishock/Duration", set_pet_duration)
dispatcher.map("/avatar/parameters/pishock/Shock", set_pet_state)
dispatcher.map("/avatar/parameters/pishock/Target", set_target)

# Dispatchers for touchpoint functions
dispatcher.map("/avatar/parameters/pishock/TPType", set_TP_type)
dispatcher.map("/avatar/parameters/pishock/TPIntensity", set_TP_intensity)
dispatcher.map("/avatar/parameters/pishock/TPDuration", set_TP_duration)
dispatcher.map("/avatar/parameters/pishock/Touchpoint_*", set_touchpoint)

# Verbose functions
dispatcher.map("/avatar/parameters/pishock/Debug", set_verbose)

ip = "127.0.0.1"
port = 9001


async def loop():
    global send_enabled
    await asyncio.sleep(0.1)

    if send_enabled == 'True':
        sleep_time = fun_duration + 1.7
        print(f"sending {type_send} at {fun_intensity} for {fun_duration} seconds")
        data_json = str({"Username": USERNAME, "Name": APP_NAME, "Code": fun_target,
                         "Intensity": fun_intensity, "Duration": fun_duration,
                         "Apikey": API_KEY, "Op": fun_type})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        requests.post('https://do.pishock.com/api/apioperate', data=data_json, headers=headers)

        print(f"waiting {sleep_time} before next command")
        await asyncio.sleep(sleep_time)

    if fun_touchpoint_state == 'True':
        sleep_time = fun_TP_duration + 1.7
        print(f"touch point sending {type_TP_send} at {fun_TP_intensity} for {fun_TP_duration} seconds")
        data_json = str({"Username": USERNAME, "Name": APP_NAME, "Code": fun_touchpoint,
                         "Intensity": fun_TP_intensity, "Duration": fun_TP_duration,
                         "Apikey": API_KEY, "Op": fun_TP_type})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        requests.post('https://do.pishock.com/api/apioperate', data=data_json, headers=headers)

        print(f"waiting {sleep_time} before next command")
        await asyncio.sleep(sleep_time)


async def init_main():
    server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()

    while True:
        await loop()

    transport.close()


asyncio.run(init_main())
