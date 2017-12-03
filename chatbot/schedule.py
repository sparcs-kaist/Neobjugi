# coding=utf-8

import re, os
import pickle
import sys, locale

from django.conf import settings
# from django.conf import BASE_DIR
'''
start_key = ['시작', '열', '오픈', '부터']
end_key = ['마감', '끝', '까지']
stop_words = ['함', '해', '혀', '해요', '합니까', '할까요', '하나요', '합니까요', '하는데', '하냐']
punctuations = ',.?!\"\'@#$%^&*()'
pickle_file = os.path.join(settings.PROJECT_ROOT, '../chatbot/schedule.p')
default_response = '일치하는 일정이 없습니다. 궁금하신 학사일정 키워드를 입력해주세요.'
'''
class Schedule(object):

    def __init__(self):
        self.start_key = ['시작', '열', '오픈', '부터']
        self.end_key = ['마감', '끝', '까지']
        self.stop_words = ['함', '해', '혀', '해요', '합니까', '할까요', '하나요', '합니까요', '하는데', '하냐']
        self.punctuations = ',.?!\"\'@#$%^&*()'
        self.pickle_file = os.path.join(settings.PROJECT_ROOT, '../chatbot/schedule.p')
        self.default_response = '일치하는 일정이 없습니다. 궁금하신 학사일정 키워드를 입력해주세요.'

    def scheduler(msg):
        msg = msg.encode('utf8').decode('utf8')
        print(msg)
        for sw in self.stop_words:
           msg = re.sub(sw, '', msg)
        print(msg)
            
        for ps in self.punctuations:
           msg = msg.rstrip(self.punctuations)
        print(msg)

        schedule = pickle.load(open(self.pickle_file, "rb"))
        msg = msg.rstrip('\n')
        msg = re.sub('은 ', ' ', msg)
        msg = re.sub('는 ', ' ', msg)
        msg = re.sub('이 ', ' ', msg)
        if not '평가 ' in msg:
            msg = re.sub('가 ', ' ', msg)

        sf = False
        ef = False

        for st in self.start_key:
            if st in msg:
                sf = True
        for st in self.end_key:
            if st in msg:
                ef = True

        msg_list = msg.split('언제')
        keyword_list = []
        
        print(msg_list)

        for msg_el in msg_list:
            keyword_list += msg_el.split(' ') 

        selected = [(self.default_response, -1)]
        
        print(keyword_list)

        for sch in schedule:
            title = sch['title']
            sch_keyword = sch['keyword'] + title.split(' ')
            count = 0
            musthave = False
            if len(sch['musthave']) == 0:
                musthave = True
            for key in keyword_list:
                if key in sch_keyword:
                    count += 1
                if not musthave:
                    for mh in sch['musthave']:
                        if mh in key:
                            musthave = True
            
            if count > 0 and musthave:
                selected.append((sch, count))
             
        print(selected)
        selected.sort(key = lambda tup: tup[1])
        selected_sch, _ = selected[-1]
        if selected_sch == self.default_response:
            return selected_sch 
        s_title = selected_sch['title']
        s_start = selected_sch['start']
        s_start = '{}월 {}일'.format(s_start[1], s_start[2])
        s_end = selected_sch['end']
        s_end = '{}월 {}일'.format(s_end[1], s_end[2])
        res = ''

        if s_end == s_start:
           res = '{}은(는) {}입니다'.format(s_title, s_start) 

        elif sf:
           res = '{}은(는) {}에 시작합니다'.format(s_title, s_start) 
        elif ef:
           res = '{}은(는) {}에 끝납니다'.format(s_title, s_end) 
        else:
           res = '{}은(는) {}에 시작해서 {}에 끝납니다'.format(s_title, s_start, s_end) 
        
        return res
'''
def scheduler(msg):
    msg = msg.encode('utf8').decode('utf8')
    print(msg)
    for sw in stop_words:
       msg = re.sub(sw, '', msg)
    print(msg)
        
    for ps in punctuations:
       msg = msg.rstrip(punctuations)
    print(msg)

    schedule = pickle.load(open(pickle_file, "rb"))
    msg = msg.rstrip('\n')
    msg = re.sub('은 ', ' ', msg)
    msg = re.sub('는 ', ' ', msg)
    msg = re.sub('이 ', ' ', msg)
    if not '평가 ' in msg:
        msg = re.sub('가 ', ' ', msg)

    sf = False
    ef = False

    for st in start_key:
        if st in msg:
            sf = True
    for st in end_key:
        if st in msg:
            ef = True

    msg_list = msg.split('언제')
    keyword_list = []
    
    print(msg_list)

    for msg_el in msg_list:
        keyword_list += msg_el.split(' ') 

    selected = [(default_response, -1)]
    
    print(keyword_list)

    for sch in schedule:
        title = sch['title']
        sch_keyword = sch['keyword'] + title.split(' ')
        count = 0
        musthave = False
        if len(sch['musthave']) == 0:
            musthave = True
        for key in keyword_list:
            if key in sch_keyword:
                count += 1
            if not musthave:
                for mh in sch['musthave']:
                    if mh in key:
                        musthave = True
        
        if count > 0 and musthave:
            selected.append((sch, count))
         
    print(selected)
    selected.sort(key = lambda tup: tup[1])
    selected_sch, _ = selected[-1]
    if selected_sch == default_response:
        return selected_sch 
    s_title = selected_sch['title']
    s_start = selected_sch['start']
    s_start = '{}월 {}일'.format(s_start[1], s_start[2])
    s_end = selected_sch['end']
    s_end = '{}월 {}일'.format(s_end[1], s_end[2])
    res = ''

    if s_end == s_start:
       res = '{}은(는) {}입니다'.format(s_title, s_start) 

    elif sf:
       res = '{}은(는) {}에 시작합니다'.format(s_title, s_start) 
    elif ef:
       res = '{}은(는) {}에 끝납니다'.format(s_title, s_end) 
    else:
       res = '{}은(는) {}에 시작해서 {}에 끝납니다'.format(s_title, s_start, s_end) 
    
    return res
'''

'''
if __name__ == '__main__':
    while True:
        msg = input('Question?: ').encode('utf8').decode('utf8')
        print(scheduler(msg))
    
    
'''
