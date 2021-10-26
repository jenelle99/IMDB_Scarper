import scrapy

#response.url + 'fullcredits'
#response.url + link

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt0386676/']

    def parse(self, response): 

        yield scrapy.Request(response.urljoin("fullcredits"), callback = self.parse_full_credits)
              

    def parse_full_credits(self, response):

        actor_links = [a.attrib['href'] for a in response.css('td.primary_photo a')]

        for link in actor_links:
            yield scrapy.Request(response.urljoin(link), callback = self.parse_actor_page)


    def parse_actor_page(self, response):

        actor_name = response.css("div span.itemprop::text").get()

        for movie in response.css("b a::text").getall():

            yield {'actor' : actor_name, 'movie_or_TV_name' : movie}