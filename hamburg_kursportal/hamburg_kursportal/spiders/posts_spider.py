import scrapy


class PostsSpider(scrapy.Spider):
    name = "posts"

    start_urls = [
        'https://hamburg.kursportal.info/search?qs=zeige%3Akurse&q=&qf=&qsrc=s&qtrigger=h'       
    ]
    

    def parse(self, response):
        self.log('i just visited: ' + response.url)
        for kurse in response.css('tr'):
            #breakpoint()
            item = {
                'name_kurse': kurse.css('a.fav_add::text').extract_first(),
                'name_company': kurse.css('td.wisy_anbieter.wisyr_anbieter::text').extract_first(),
                'phone': kurse.css('span.wisyr_anbieter_telefon::text').extract_first(),
                'url': kurse.css('span.wisyr_anbieter_profil > a::attr(href)').extract_first(),
                'date': kurse.css('span.wisyr_termin_datum::text').extract_first(),
                'lenght_time': kurse.css('td.wisyr_dauer::text').extract_first(),
                'lessons': kurse.css('span.wisyr_dauer_detail::text').extract_first(),
                'place': kurse.css('td.wisyr_ort.multiple::text').extract_first(),
                'price': kurse.css('span.wisyr_euro::text').extract_first(),
                #'name_kurse': kurse.xpath('./a[@class="fav_add"]/text()').extract_first(),
            }
            yield item

        next_page_url = response.css('span.wisy_paginate.wisyr_paginate_bottom > a.wisy_paginate_next::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)



#scrapy.utils.response.open_in_browser(response)