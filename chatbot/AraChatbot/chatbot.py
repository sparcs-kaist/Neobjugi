import json

result_path = '/home/ykhong/neobjuki/neobjugi/chatbot/AraChatbot/result.json'

class AraChatbot(object):

    def __init__(self):
        self.recent_words = ['최근', '근황']
        self.accept_words = ['네', '어', 'ㅇ', 'ㅇㅇ', 'y', 'yes']
        self.decline_words = ['아니요', '아니', 'ㄴ', 'ㄴㄴ', 'n', 'no']
        self.filter_words = ['판매완료', '마감', '완료', 'deleted']
        self.contents = self.read_file(result_path)


    def read_file(self, filename):
        contents = []

        json_data = open(filename, 'r', encoding='utf-8').read()
        data = json.loads(json_data)

        for article in data:

            if not any(filter_word in article['title'].lower() for filter_word in self.filter_words):

                contents.append(article)

        return sorted(contents, key=lambda k: -int(k['article_id']))


    def search(self, keywords):
        search_results = []

        for article in self.contents:

            if any(keyword in article['title'].lower() for keyword in keywords):

                search_results.append(article)

        return search_results


    def chat(self, query, user_info):
        search_results = self.search(user_info.context.split(' '))
        print('state {}'.format(user_info.status))
        status = user_info.status
        keyword = ', '.join(user_info.context.split(' '))

        if user_info.status == 0 :

            if not search_results:
                user_info.status = 4
                user_info.save()
                return '\n{keyword} 관련 게시물을 찾지 못했습니다.'.format(keyword=keyword)

            res = '\n{keyword} 관련 게시물 {num} 개를 찾았습니다.\n'.format(keyword=keyword, num=len(search_results))
            res += '\n[검색 게시물 목록]\n'

            for i, article in enumerate(search_results):
                res += '\n[{num}] {title}'.format(num=i + 1, title=article['title'])

            res += '\n\n관심있는 게시물이 있습니까?'

            user_info.status = 1
            user_info.save()

            return res

        elif user_info.status is 1:

            if query.lower().strip() in self.accept_words:

                res = '몇번 게시물에 관심이 있습니까?'

                user_info.status = 2
                user_info.save()

                return res

            elif query.lower().strip() in self.decline_words:

                res = '쳇봇 세션을 종료하겠습니다.'

                user_info.status = 4 
                user_info.save()
                return res

            else:

                return '다시 입력해주세요.'

        elif status is 2:

            if query.isdigit():

                select = int(query.strip())

                res = '\n"{title}" 게시물의 내용입니다.\n\n'.format(title=search_results[select - 1]['title'])
                res += search_results[select - 1]['content']
                res += '\n\n게시물 주소입니다: {url}\n'.format(url=search_results[select - 1]['article_url'])
                res += '\n더 보시겠습니까?'
                
                user_info.status = 3
                user_info.save()
                return res

            else:

                return '숫자를 입력해주세요.'

        else:

            if query.lower().strip() in self.accept_words:

                res = '\n[검색 게시물 목록]\n'

                for i, article in enumerate(search_results):
                    res += '\n[{num}] {title}'.format(num=i + 1, title=article['title'])

                res += '\n\n관심있는 게시물이 있습니까?'


                user_info.status = 1
                user_info.save()
                return res

            elif query.lower().strip() in self.decline_words:

                res = '쳇봇 세션을 종료하겠습니다.'


                user_info.status = 4
                user_info.save()
                return res

            else:

                return '다시 입력해주세요.'
