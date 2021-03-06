import json
from datetime import datetime, timedelta
import os

BUS_DATA_PATH = "busdata"
BUS_DATA_FILE = "buses"

TEST_STRING = "testbus"
TEST_HELP = "Please send your test string with POSIX time, which can be obtained from https://www.epochconverter.com/"

TIME_STRING = "%H시 %M분"
ERR_STOP_STRING = "{}의 도착 시간을 알고 싶은 정류장의 이름을 정확히 말씀해주세요. {} {}에 갑니다."
ERR_TIME_STRING = "{} 오늘 더이상 {}에 오지 않습니다."
ERR_DAY_STRING = "{} 오늘 운행하지 않습니다."
ARRIVAL_STRING = "{} {}에 {}에 도착할 예정입니다."
DEPARTURE_STRING = "{} {}에 {}에서 출발할 예정입니다."
OMITTING_STRING = "..."

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

    res = parseTest(msg, now)
    if not res:
        return TEST_HELP
    msg, now = res
    return "\n".join(filter(lambda s: len(s) > 0, map(lambda bus: respondForBus(nmsg, now, bus), datas)))

def respondForBus(msg, now, bus):
    nmsg = hasKey(msg, bus["keys"])
    if nmsg:
        busName = bus["name"]
        today = now.weekday() - (1 if now.hour < 4 else 0)
        if today not in bus["day"]:
            return ERR_DAY_STRING.format(addJosa(busName)) if bus["errday"] else ""

        errTime = bus["errtime"]
        busTime = bus["times"]
        stops = bus["stops"]

        responses = list(filter(lambda s: len(s) > 0, map(lambda stop: respondForStop(nmsg, now, busName, errTime, busTime, stop), stops)))

        if len(responses) > 0:
            return "\n".join(responses)
        else:
            return ERR_STOP_STRING.format(busName, addJosa(busName), ", ".join(map(lambda stop: stop["name"], stops)))
    else:
        return ""

def respondForStop(msg, now, busName, errTime, times, stop):
    if hasKey(msg, stop["keys"]):
        stopTime = stop["time"]
        stopName = stop["name"]

        def f(x):
            dt = timedelta(minutes = stopTime[x[0]])
            availables = list(filter(lambda t: t >= now, map(lambda l: datetime(now.year, now.month, now.day, hour = l[0], minute = l[1]) + dt, times)))
            availableString = ", ".join(map(lambda t: t.strftime(TIME_STRING), availables[0:3])) + (OMITTING_STRING if len(availables) > 3 else "")
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
                    [("arrival", ARRIVAL_STRING), ("departure", DEPARTURE_STRING)]
                )
            )
        ))

        if len(results) > 0:
            return "\n".join(results)
        else:
            return ERR_TIME_STRING.format(addJosa(busName), stopName) if errTime else ""
    else:
        return ""

def hasKey(st, keys):
    filtered = list(filter(lambda k: k in st, keys))
    if len(filtered) > 0:
        return st.replace(filtered[0], "b", 1)
    else:
        return None

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
    return st + ("은" if ((ord(st[-1]) - 44032) % 28) else "는")

def parseTest(msg, now):
    if not msg.startswith(TEST_STRING):
        return (msg, now)

    msg = msg[len(TEST_STRING):]
    try:
        return (msg[10:], datetime.fromtimestamp(int(msg[0:10])))
    except:
        return None

#print(bus(input()))
