import scrapy
import chatbot.items as items

class AraSpider(scrapy.Spider):
    name = "ara"
    start_urls = [
        "https://ara.kaist.ac.kr/",
    ]
    	
    def parse(self, response):

        formdata = {
            "username": getattr(self, 'username', None),
            "password": getattr(self, 'password', None),
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
        board = getattr(self, 'board', '')
        depth = getattr(self, 'depth', 1)
        keyword = getattr(self, 'keyword', '')

        # search url example:
        # "http://ara.kaist.ac.kr/all/search/?search_word={keyword}&chosen_search_method=title|content|author_nickname|author_username&page_no={page}".format(keyword=keyword, page=page)
        url = "http://ara.kaist.ac.kr/"

       	# Set board URL
        if board is '':
        	url += 'all/'
        else:
        	url += ("board/" + board + "/")

        for i in range(depth):

	        if keyword is not '':
	            temp = url + "search/?search_word={keyword}&chosen_search_method=title|content|author_nickname|author_username&page_no={page}".format(keyword=keyword, page=i + 1)
	        else:
	            temp = url + "?page_no={page}".format(page=i + 1)

	        yield scrapy.Request(
	            url = temp,
	            callback = self.parse_post_link_list,
	        )

    def parse_post_link_list(self, response):
        post_link_list = response.css("table.articleList tbody tr")

        for post_link in post_link_list:

            yield scrapy.Request(
                url=response.urljoin(post_link.css("td.title a::attr(href)").extract_first()),
                callback=self.parse_post,
            )

    def parse_post(self, response):
        _id = int(response.css("div.articleTitle a::attr(id)").extract_first().strip())
        _url = response.url
        title = response.css("div.articleTitle a::text").extract_first().strip()
        time = response.css("p.date a::text").extract_first().strip()
        # content = "\n".join(map(lambda s: s.strip(), response.css("div.articleContents div.article::text").extract()))
        # content = "\n".join(map(lambda s: s.strip(), response.css("div.articleContents").xpath('.//*//text()').extract()))
        content = "\n".join(map(lambda s: s.strip(), response.css("div.articleContents div.article").xpath('./descendant::text()').extract()))
        # content = "\n".join(map(lambda s: s.strip(), response.xpath("//div[@class='article']//text()").extract()))
        # content = response.xpath(".//div[@class='article']//text()").extract()


        yield items.AraArticle({
            'keyword': getattr(self, 'keyword', None),
            'article_id': _id,
            'article_url': _url,
            'title': title,
            'time': time,
            'content': content,
        })
