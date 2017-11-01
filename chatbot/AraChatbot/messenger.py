# import Bus Chatbot
# import Timetable Chatbot
from chatbot.AraChatbot.chatbot import AraChatbot
from chatbot.models import Account


class Session(object):

    def __init__(self):
        self.user_history = {}
        # Instantiate Bus Chatbot
        # Instantiate Timetable Chatbot
        self.arabot = AraChatbot()


    def refresh_history(self, user_id):

        if (user_id in self.user_history.keys()) and (self.user_history[user_id]['state'] is 4):

            self.user_history.pop(user_id)


    def call(self, user_id, query):

        #self.refresh_history(user_id)
        user_info = Account.objects.get(fbid=user_id)
        try:
            print('refresh_history {}'.format(user_info.fbid + str(user_info.status)))
        except Exception as e:
            print(e)
          

        if '버스' in query.lower().split()[0]:

            # Bus chatbot does something

            res = '버스 쳇봇입니다.'

            if user_id in self.user_history.keys():
                res += '\n\n아라 쳇봇 대화 기록은 초기화 되었습니다.'

                self.user_history[user_id]['state'] = 4

            return [user_id, res]

        elif '시간' in query.lower().split()[0]:

            # Timetable chatbot does something

            res = '시간표 쳇봇입니다.'

            if user_id in self.user_history.keys():
                res += '\n\n아라 쳇봇 대화 기록은 초기화 되었습니다.'

                self.user_history[user_id]['state'] = 4

            return [user_id, res]

        else:
            print('user history {}'.format(user_info.status))

            try:
                if '아라' in query.lower().split()[0]:
                    user_info.context = ' '.join(query.lower().split()[1:])
                    user_info.status = 0
                    user_info.save()
                    print('changed? {}'.format(user_info.status))

                    return [user_id, self.arabot.chat(query, user_info)]

                else:
                    res =  [user_id, self.arabot.chat(query, user_info)]
                    if len(res[-1]) == 0:
                        return [user_id, '다시 입력해주세용!!.']
                    else:
                        return res
            except Exception as e:
                print('ara handling error')
                print(e)
