import scrapy
import csv
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep


class ItdashboardSpider(scrapy.Spider):
    name = 'itdashboard'
    start_urls = ['https://itdashboard.gov/']
    headers = { 
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                # "Cache-Control": "no-cache",
                # "Connection": "keep-alive",
                "Cookie": "SSESS04ae24068a2b6b9bb1975f7ad3e4d1c2=6jlUkWTvKqGui1azMl8iQZw32XCryACAIvDn01u-MOM; has_js=1; wstact=d00da1a01ad1162f15f32f06bf9d82fff2a18cc966e10de10c52cc084f7cc3bf",
                # "Host": "itdashboard.gov",
               #  "Pragma": "no-cache",
                "Referer": "https://itdashboard.gov/",
                # "sec-ch-ua": "Google Chrome", #;v="93", " Not;A Brand";v="99", "Chromium";v="93",
                # "sec-ch-ua-mobile": "?0",
                # "sec-ch-ua-platform": "Windows",
                # "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                # "X-Session-Token": "d00da1a01ad1162f15f32f06bf9d82fff2a18cc966e10de10c52cc084f7cc3bf"
        }

    def parse(self, response):
        path = "C:\work\chromedriver.exe"
        driver = webdriver.Chrome(path)
        driver.get('https://itdashboard.gov/')
        link = driver.find_element_by_link_text("DIVE IN")
        link.click()
        sleep(10)
        url = 'https://itdashboard.gov/api/v1/ITDB2/visualization/govwide/agencyTiles'
        
        request = scrapy.Request(url, callback=self.parse_api, headers = self.headers)
        yield request
    
    def parse_api(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        
        with open('Agencies.csv', mode='w') as csv_file:
            fieldnames = ['fiscalYear', 'agencycode', 'agencyName', 'totalSpendingCY']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for val in data['result']:
                writer.writerow({
                    'fiscalYear': val['fiscalYear'], 
                    'agencycode': val['agencyCode'], 
                    'agencyName': val['agencyName'],
                    'totalSpendingCY': val['totalSpendingCY']})
        
        
            
            
    
        
