# coding=utf-8

import json
from datetime import datetime, timedelta
import os

BUS_DATA_PATH = "busdata"
BUS_DATA_FILE = "buses"

# def initializeBus():
#     global datas
#     f = open(BUS_DATA_PATH + "/" + BUS_DATA_FILE, "r")
#     datas = list(map(lambda s: parseFile(s.replace("\n", "")), f.readlines()))
#     f.close()

def readBusData():
    scriptDir = os.path.dirname(__file__)
    path = os.path.join(scriptDir, BUS_DATA_PATH, BUS_DATA_FILE)
    f = open(path, "r")
    datas = list(map(lambda s: parseFile(s.replace("\n", "")), f.readlines()))
    f.close()
    return datas

def bus(st):
    datas = readBusData()
    nst = normalize(st)
    return "\n".join(filter(lambda s: len(s) > 0, map(lambda d: respond(nst, d), datas)))

def respond(st, data):
    if hasKey(st, data["keys"]):
        name = data["name"].encode("utf8")
        now = datetime.now()
        departures = list(filter(lambda s: len(s) > 0, map(lambda d: nextDeparture(st, now, name, data["times"], d), data["stops"])))
        if len(departures) > 0:
            return "\n".join(departures)
        else:
            return name + "의 도착 시간을 알고 싶은 정류장의 이름을 정확히 말씀해주세요."
    else:
        return ""

def nextDeparture(st, now, name, times, data):
    if hasKey(st, data["keys"]):
        dt = timedelta(minutes = data["time"])
        stop = data["name"].encode("utf8")
        departure = list(filter(lambda t: t > now, map(lambda l: datetime(now.year, now.month, now.day, hour = l[0], minute = l[1]) + dt, times)))
        if len(departure) > 0:
            t = departure[0]
            return addJosa(name) + str(t.hour) + "시 " + str(t.minute) + "분에 " + stop + "에 도착할 예정입니다."
        else:
            return addJosa(name) + "오늘 더이상 " + stop + "에 오지 않습니다."
    else:
        return ""

def hasKey(st, keys):
    return len(list(filter(lambda k: k in st, keys))) > 0

def parseFile(name):
    scriptDir = os.path.dirname(__file__)
    path = os.path.join(scriptDir, BUS_DATA_PATH, name)
    f = open(path, "r")
    data = json.loads(f.read())
    f.close()
    return data

def normalize(st):
    return st.replace(" ", "").replace("\t", "").replace("\n", "").lower()

def addJosa(st):
    return st + "은(는) "
