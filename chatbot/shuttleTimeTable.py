import json
from datetime import datetime

olevTT = {
    'buses': [[8,45], [8,55], [9,15], [9,25], [9,45], [9,55], [10,15], [10,25], [10,45], [10,55], [11,15], [11,25], [11,45], [12,55], [13,15], [13,25], [13,45], [13,55], [14,15], [14,25], [14,45], [14,55], [15,15], [15,25], [15,45], [15,55], [16,15], [16,25], [16,45], [16,55]],
    'stops': {
        'undergradCafe1': 0,
        'sportsComp': 1,
        'creativeLearn': 3,
        'medDept': 4,
        'medCent': 6,
        'mainGate': 9,
        'duckPond': 10,
        'eduSupport': 11,
        'underGradCafe2': 14
    }
}

DTBusTT = {
    'buses': [[9,5], [10,5], [11,5], [13,5], [14,5], [15,5], [16,5], [17,5]],
    'stops': {
        'auditorium1': 0,
        'admin1': 2,
        'duckPond1': 4,
        'cnUniv': 10,
        'wpStat1': 15,
        'galleria': 20,
        'govnBld': 27,
        'wpStat2': 35,
        'duckPond2': 38,
        'admin2': 39,
        'auditorium2': 40,
    }
}

olevKey = [
    "올레브",
    "전기",
    "학교 버스",
    "학교버스",
    "전기버스",
    "전기 버스",
    "캠퍼스버스",
    "캠퍼스 버스",
]

olevStopsKey = {
    'undergradCafe1': ["카마", "카이마루", "출발", "북측식당", "학식"],
    'sportsComp': ["스컴", "스포츠컴플렉스", "스포츠 컴플렉스", "체육관"],
    'creativeLearn': ["창의관", "창의", "E11", "e11", "창의학습관"],
    'medDept': [],
    'medCent': [],
    'mainGate': ["정문", "입구"],
    'duckPond': ["오리연못", "연못"],
    'eduSupport': ["지원"],
    'underGradCafe2': []
} 

DTBusKey = [
    "월평",
    "시내",
    "셔틀"
]

DTBusStopsKey = {
    'auditorium1': ["강당", "대강당"],
    'admin1': ["본관"],
    'duckPond1': ["오리연못", "연못", "오리"],
    'cnUniv': ["충남대", "충남", "궁동"],
    'wpStat1': ["월평역"],
    'galleria': ["갤러리아", "백화점"],
    'govnBld': ["청사", "정부"],
    'wpStat2': ["월평역"],
    'duckPond2': ["오리연못", "연못", "오리"],
    'admin2': ["본관"],
    'auditorium2': ["대강당", "강당"],    
}



def bus(str):
    response = ""
    if checkOlev(str):
        response = "올레브는 " + olev(str) 
    elif checkDTBus(str):
        response = "셔틀버스는 " + DTBus(str) 

    return response

def checkDTBus(str):
    for i in DTBusKey:
        if i in str:
            return True
    return False

def checkOlev(str):
    for i in olevKey:
        if i in str:
            return True
    return False

def olev(str):
    hour = datetime.now().hour
    minute = datetime.now().minute
    hour = 9
    

    response = "현재 운행중이 아닙니다"

    for i in olevStopsKey:
        for j in olevStopsKey[i]:
            if j in str:
                for t in olevTT['buses']:
                    if t[0] >= hour and t[1] >= minute:
                        m = olevTT['stops'][i] + t[1]
                        h = t[0]
                        if m >= 60:
                            m -= 60
                            h += 1
                        response = i + "에 " + str(h) + "시 " + str(m) + "분에 도착합니다."

    return response

def DTBus(str):
    hour = datetime.now().hour
    minute = datetime.now().minute

    response = "현재 운행중이 아닙니다"
    for i in DTBusStopsKey:
        for j in DTBusStopsKey[i]:
            if j in str:
                for t in DTBusTT['buses']:
                    if t[0] >= hour and t[1] >= minute:
                        m = olevTT['stops'][i] + t[1]
                        if m >= 60:
                            m -= 60
                            h += 1
                        response = i + "에 " + str(h) + "시 " + str(m) + "분에 도착합니다."
                
    return response

print(bus(input()))
