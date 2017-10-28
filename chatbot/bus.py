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

def bus(msg, now = datetime.now()):
    datas = readBusData()
    nmsg = normalize(msg)
    return "\n".join(filter(lambda s: len(s) > 0, map(lambda bus: respondForBus(nmsg, now, bus), datas)))

def respondForBus(msg, now, bus):
    if hasKey(msg, bus["keys"]):
        busName = bus["name"]
        busTime = bus["times"]
        stops = bus["stops"]

        responses = list(filter(lambda s: len(s) > 0, map(lambda stop: respondForStop(msg, now, busName, busTime, stop), stops)))

        if len(responses) > 0:
            return "\n".join(responses)
        else:
            return busName + "의 도착 시간을 알고 싶은 정류장의 이름을 정확히 말씀해주세요."
    else:
        return ""

def respondForStop(msg, now, busName, times, stop):
    if hasKey(msg, stop["keys"]):
        stopTime = stop["time"]
        stopName = stop["name"]

        def f(x):
            dt = timedelta(minutes = stopTime[x[0]])
            availables = list(filter(lambda t: t >= now, map(lambda l: datetime(now.year, now.month, now.day, hour = l[0], minute = l[1]) + dt, times)))
            availableString = ", ".join(map(lambda t: t.strftime("%H시 %M분"), availables[0:3])) + ("..." if len(availables) > 3 else "")
            if len(availables) > 0:
                return x[1].format(addJosa(busName), availableString, stopName)
            else:
                return ""

        results = list(filter(
            lambda s: len(s) > 0,
            map(
                f,
                filter(
                    lambda x: x[0] in stopTime,
                    [("arrival", "{} {}에 {}에 도착할 예정입니다."), ("departure", "{} {}에 {}에서 출발할 예정입니다.")]
                )
            )
        ))

        if len(results) > 0:
            return "\n".join(results)
        else:
            return "{} 오늘 더이상 {}에 오지 않습니다.".format(addJosa(busName), stopName)
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
    return st + ("은" if (ord(st[-1]) - 44032) % 28 else "는")

print(bus(input(), datetime.now() + timedelta(hours=int(input()))))
