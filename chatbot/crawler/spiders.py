import scrapy
from items import AraArticle
import credentials

class AraSpider(scrapy.Spider):
    name = "ara"
    start_urls = [
        "https://ara.kaist.ac.kr/",
    ]

    def parse(self, response):

        formdata = {
            "username": credentials.USERNAME,
            "password": credentials.PASSWORD,
        }

        return scrapy.FormRequest.from_response(
            response=response,
            formdata=formdata,
            callback=self.redirect,
        )

    def redirect(self, response):
        # Automatically go into search mode if keyword is not None. Else, go into recent mode.
        # modes: recent, search
        # mode = getattr(self, 'mode', 'recent')

        # /board/.../
        # Notice, Garbages, Food, Love, Infoworld, FunLife, Lostfound, Wanted,
        # BuySell, QandA, Jobs, Housing, Hobby, Siggame
        ## if not specified, go to /all
        boards = ['Notice', 'Garbages', 'Food', 'Love', 'Infoworld', 'FunLife', 'Lostfound', 'Wanted', 'BuySell', 'QandA', 'Jobs', 'Housing', 'Hobby', 'Siggame']
        depth = 3

        # search url example:
        # "http://ara.kaist.ac.kr/all/search/?search_word={keyword}&chosen_search_method=title|content|author_nickname|author_username&page_no={page}".format(keyword=keyword, page=page)
        # Set board URL
        for board in boards:
            url = "http://ara.kaist.ac.kr/board/" + board + "/"

            for i in range(depth):
                temp = url + "?page_no={page}".format(page=i + 1)

                yield scrapy.Request(
                    url = temp,
                    callback = self.parse_post_link_list,
                    meta = {'board': board},
                )

    def parse_post_link_list(self, response):
        post_link_list = response.css("table.articleList tbody tr")

        for post_link in post_link_list:

            yield scrapy.Request(
                url=response.urljoin(post_link.css("td.title a::attr(href)").extract_first()),
                callback=self.parse_post,
                meta = {'board': response.meta.get('board')},
            )

    def parse_post(self, response):
        article_id = int(response.css("div.articleTitle a::attr(id)").extract_first().strip())
        article_url = response.url
        title = response.css("div.articleTitle a::text").extract_first().strip()
        time = response.css("p.date a::text").extract_first().strip()
        content = "\n".join(map(lambda s: s.strip(), response.css("div.articleContents div.article").xpath('./descendant::text()').extract()))

        yield AraArticle({
            'board': response.meta.get('board'),
            'article_id': article_id,
            'article_url': article_url,
            'title': title,
            'time': time,
            'content': content,
        })
