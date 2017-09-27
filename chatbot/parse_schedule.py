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
        try:
            keyword = el['keyword'].split(',')
        except:
            pass
        event['keyword'] = keyword
        cal.append(event)
        print(event)
    pickle.dump( cal, open( "schedule.p", "wb" ) )
