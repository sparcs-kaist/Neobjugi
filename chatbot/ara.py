import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from chatbot.spider import AraSpider


# Define Item Pipeline
class AraPipeline(object):

    def process_item(self, item, spider):
        # for field in ['content', 'title']:
        #     value = ' '.join(str(item[field]).split())
        #     item[field] = value
        print(item)

        for field in ['content', 'title']:
            print(field)
            item[field] = item[field].strip()

        results[item['keyword']].append(dict(item))


# Chatbot - Recieves question, extracts keywords, crawls, processes the result, and then returns the answer
class AraChatbot(object):

    def __init__(self, username, password, depth=1):
        self.username = username
        self.password = password
        self.depth = depth

        self.accept_words = ['네', 'ㅇ', 'ㅇㅇ']
        self.decline_words = ['아니요', 'ㄴ', 'ㄴㄴ']

        logging.getLogger('scrapy').propagate = True 

        
    def crawl(self, options):
        global results
        results = {option['keyword']: [] for option in options}
        print(results)

        # Define Settings
        settings = get_project_settings()
        settings.set('ITEM_PIPELINES', {'ara.AraPipeline': 1})
        print(settings)

        # Run Spider
        spider = AraSpider()
        process = CrawlerProcess(settings)
        print(process)

        for option in options:
            process.crawl(spider, **option)

        process.start()
        
        # Sort Results
        # results = sorted(results, key=lambda k: -k['article_id']) # For sorting in reverse order (most recent first)
        for key in results.keys():
            result = results[key]
            sorted_result = sorted(result, key=lambda k: -k['article_id'])
            temp = [res.pop('keyword') for res in sorted_result]
            results[key] = sorted_result
        
        return results


    # Processes the question and returns appropriate options for crawler
    def processQuery(self, question):
        options = []

        res = question.split(' ')

        option_template = {'username': self.username, \
                           'password': self.password, \
                           'board': '', \
                           'depth': self.depth, \
                           'keyword': '',
        }

        option_template['board'] = res[0]
        option_template['keyword'] = res[1]
        options.append(option_template)
        
        return options


    def answer(self, question):
        options = self.processQuery(question)
        res = self.crawl(options)
        print(res)
        
        ans = ''

        for i, key in enumerate(res.keys()):

            if key is '':
                keyword = '최근'
            else:
                keyword = key

            if options[i]['board'] is '':
                board = '전체'
            else:
                board = options[i]['board']

            ans += '\n{board} 게시판 {keyword} 게시물 {num} 개를 찾았습니다.\n'.format(board=board, keyword=keyword, num=len(res[key]))

            for j, article in enumerate(res[key]):
                ans += '게시물 {num} 제목은 "{title}" 입니다.'.format(num=j + 1, title=article['title'])
            
            return ans

            while False:
	            accept = input('\n관심있는 게시물이 있습니까? ')

	            if accept in self.accept_words:
	                select = int(input('\n몇번 게시물에 관심이 있나요? '))
	                print('\n"{title}" 게시물의 내용입니다:\n'.format(title=res[key][select - 1]['title']))
	                print(res[key][select - 1]['content'])
	                print('\n게시물 주소입니다: {url}'.format(url=res[key][select - 1]['article_url']))

	                while True:
		                accept = input('\n더 보시겠습니까? ')

		                if accept in self.accept_words:

		                    for j, article in enumerate(res[key]):
		                        print('게시물 {num} 제목은 "{title}" 입니다.'.format(num=j + 1, title=article['title']))

		                    select = int(input('\n몇번 게시물에 관심이 있나요? '))
		                    print('\n"{title}" 게시물의 내용입니다:\n'.format(title=res[key][select - 1]['title']))
		                    print(res[key][select - 1]['content'])
		                    print('\n게시물 주소입니다: {url}'.format(url=res[key][select - 1]['article_url']))
		                
		                else:
		                    break

	                break

	            elif accept in self.decline_words:
	            	break

	            else:
	            	print('\n다시 입력해주세요.')

            '''
            if i == len(res) - 1:
                print('\n쳇봇 세션을 종료하겠습니다.')
            else:
                print('\n다음 검색 결과로 넘어가겠습니다.')
            '''
            
