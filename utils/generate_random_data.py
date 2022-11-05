import datetime
import logging

import sys

sys.path.append("/opt/device")
logging.basicConfig(level=logging.INFO)

import json
import random
import os
import time

f = open("/opt/device/config/config.json")
config_data = json.load(f)

def generate_random_data_by_type_device(type_device):
    random_data = ""
    if type_device == "temperature":
        random_data = generate_random_temperature_data()
    elif type_device == "humidity":
        random_data = generate_random_humidity_data()
    elif type_device == "smart_meter":
        random_data = generate_random_smart_meter_data()
    return random_data

def generate_random_temperature_data():
    hour = datetime.datetime.now().hour
    random_data = 0
    min_temperature = config_data["min_temperature"]
    mean_temperature = config_data["mean_temperature"]
    max_temperature = config_data["max_temperature"]
    scale_temperature = config_data["scale_temperature"]
    if hour >= 0 and hour <= 6:
        random_data = random.uniform(min_temperature, (min_temperature + mean_temperature) / 2.0)
    elif hour >= 7 and hour <= 12:
        random_data = random.uniform((min_temperature + mean_temperature) / 2.0, mean_temperature)
    elif hour > 12 and hour <= 18:
        random_data = random.uniform(mean_temperature, max_temperature)
    else:
        random_data = random.uniform(mean_temperature, (mean_temperature + max_temperature) / 2.0)
    message = {"temperature": round(random_data, 2), "scale": scale_temperature, "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
    return message

def generate_random_humidity_data():
    hour = datetime.datetime.now().hour
    random_data = 0
    min_humidity = config_data["min_humidity"]
    mean_humidity = config_data["mean_humidity"]
    max_humidity = config_data["max_humidity"]
    scale_humidity = config_data["scale_humidity"]
    if hour >= 0 and hour <= 6:
        random_data = random.uniform(mean_humidity, max_humidity)
    elif hour >= 7 and hour <= 12:
        random_data = random.uniform(mean_humidity, (mean_humidity + max_humidity) / 2.0)
    elif hour > 12 and hour <= 18:
        random_data = random.uniform(min_humidity, (min_humidity + mean_humidity) / 2.0)
    else:
        random_data = random.uniform((min_humidity + mean_humidity) / 2.0, mean_humidity)
    message = {"humidity": round(random_data, 2), "scale": scale_humidity,
               "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
    return message

def generate_random_smart_meter_data():
    hour = datetime.datetime.now().hour
    random_data = 0
    min_smart_meter = config_data["min_smart_meter"]
    mean_smart_meter = config_data["mean_smart_meter"]
    max_smart_meter = config_data["max_smart_meter"]
    scale_smart_meter = config_data["scale_smart_meter"]
    if hour >= 0 and hour <= 6:
        random_data = random.uniform(min_smart_meter, (min_smart_meter + mean_smart_meter) / 2.0)
    elif hour >= 7 and hour <= 12:
        random_data = random.uniform((min_smart_meter + mean_smart_meter) / 2.0, mean_smart_meter)
    elif hour > 12 and hour <= 18:
        random_data = random.uniform(mean_smart_meter, max_smart_meter)
    else:
        random_data = random.uniform(mean_smart_meter, (mean_smart_meter + max_smart_meter) / 2.0)
    message = {"smart_meter": round(random_data, 2), "scale": scale_smart_meter,
               "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
    return message
