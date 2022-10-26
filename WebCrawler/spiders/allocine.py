import scrapy
from scrapy import Request
from WebCrawler.items import ReviewsAllocineItem


class AllocineSpider(scrapy.Spider):
    name = 'allocine'
    allowed_domains = ['www.allocine.fr']
    #n = input("Entrez le nombre de page que vous souhaitez afficher (max 10) : ")
    #Liste des pages à collecter
    start_urls = [f'https://www.allocine.fr/film/meilleurs/?page={n}' for n in range(1,10)] #/?page={n}' for n in range(1,10)


    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)
        
        
    def parse(self, response):
        liste_film = response.css('li.mdl')
        
        
        # Boucle qui parcours l'ensemble des éléments de la liste des films
        for film in liste_film:
            item = ReviewsAllocineItem()

            # Nom du film
            try:
                item['title'] = film.css('a.meta-title-link::text').extract()
            except:
                item['title'] = 'None'
              
            # Lien de l'image du film
            try:
                item['img'] = film.css('li.mdl').css('img').attrib['src']
            except:
                item['img'] = 'None'


            # Auteur du film
            try:
                item['author'] = film.css('a.blue-link::text')[0].extract().strip()
            except:
                item['author'] = 'None'
           
            # Durée du film
            try:
                item['time'] = film.css('div.meta-body-item.meta-body-info::text')[0].extract().strip('\n')
            except:
                item['time'] = 'None'

            # Genre cinématographique
            try:
                item['genre'] = film.css('.meta-body-item.meta-body-info')[0].css('span::text')[1:4].extract()
            except:
                 item['genre'] = 'None'

            # Score du film
            try:
                item['score'] = film.css('span.stareval-note::text')[1].extract()
            except:
                item['score'] = 'None'

            # Description du film
            try:
                item['desc'] = film.css('div.content-txt::text')[0].extract().strip()
            except:
                item['desc'] = 'None'

            # Date de sortie
            try:
                item['release'] = film.css('span.date::text').extract()
            except:
                item['release'] = 'None'


            yield item