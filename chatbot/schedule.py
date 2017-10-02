# coding=utf-8

import re, os
import pickle
import sys, locale

from django.conf import settings
# from django.conf import BASE_DIR

start_key = ['시작', '열', '오픈', '부터']
end_key = ['마감', '끝', '까지']
pickle_file = os.path.join(settings.PROJECT_ROOT, '../chatbot/schedule.p')

def scheduler(msg):
    msg = msg.encode('utf8').decode('utf8')
    print(msg)
    print(pickle_file)
    schedule = pickle.load(open(pickle_file, "rb"))
    msg = msg.rstrip('\n')
    re.sub('은 ', ' ', msg)
    re.sub('는 ', ' ', msg)
    re.sub('이 ', ' ', msg)
    if not '평가 ' in msg:
        re.sub('가 ', ' ', msg)

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

    selected = [('fuck off', 100000)]
    
    print(keyword_list)

    for sch in schedule:
        title = sch['title']
        sch_keyword = sch['keyword'] + title.split(' ')
        count = 0
        for key in keyword_list:
            if key in sch_keyword:
                count += 1
        
        if count > 0:
            selected.append((sch, count))
         
    print(selected)
    selected.sort(key = lambda tup: tup[1])
    selected_sch, _ = selected[0]
    if selected_sch == 'fuck off':
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
if __name__ == '__main__':
    while True:
        msg = input('Question?: ').encode('utf8').decode('utf8')
        print(scheduler(msg))
    
    
'''
