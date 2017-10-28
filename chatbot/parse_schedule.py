import json
import pickle


file_path = 'schedule_kr.json'


if __name__ == '__main__':
    f = open(file_path).read()
    data = json.loads(f) 
    cal = []
    for el in data:
        event = dict()
        title = el['title']
        event['title'] = title
        start = el['start']
        start = start.split(' ')[0]
        start = [int(e) for e in start.split('-')]
        event['start'] = start 
        end = el['end']
        end = end.split(' ')[0]
        end = [int(e) for e in end.split('-')]
        event['end'] = end 
        keyword = []
        musthave = []
        try:
            keyword = el['keyword'].split(',')
            for i in range(len(keyword)):
                key = keyword[i]
                if len(key) == 1:
                    continue
                elif key[0] == ' ':
                    key = key[1:]
                elif key[-1] == ' ':
                    key = key[:-1]
                keyword[i] = key
        except:
            pass
        try:
            musthave = el['musthave'].split(',')
        except:
            pass
        event['keyword'] = keyword
        event['musthave'] = musthave
        cal.append(event)
        print(event)
    pickle.dump( cal, open( "schedule.p", "wb" ) )
