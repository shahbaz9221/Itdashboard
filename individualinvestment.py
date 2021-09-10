import scrapy
import json
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import  Select
from time import sleep

class ItdashboardSpider(scrapy.Spider):
    name = 'individualinvestment'
    start_urls = ['https://itdashboard.gov/drupal/summary/005']
    headers = { 
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                # Cache-Control: no-cache
                # Connection: keep-alive
                "Cookie": "SSESS04ae24068a2b6b9bb1975f7ad3e4d1c2=6jlUkWTvKqGui1azMl8iQZw32XCryACAIvDn01u-MOM; has_js=1; wstact=306d9f8ae9457d6496f71f20248139af189df044400a50c0ab176bd4eea51148",
                # Host: itdashboard.gov
                # Pragma: no-cache
                "Referer": "https://itdashboard.gov/drupal/summary/005",
                # sec-ch-ua: "Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"
                # sec-ch-ua-mobile: ?0
                # sec-ch-ua-platform: "Windows"
                # Sec-Fetch-Dest: empty
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
        }

    def parse(self, response):
        path = "C:\work\chromedriver.exe"
        driver = webdriver.Chrome(path)
        base_url = 'https://itdashboard.gov/drupal/summary/005'
        driver.get(base_url)
        sleep(20)
        element = driver.find_element_by_name("investments-table-object_length")
        drp = Select(element)
        drp.select_by_visible_text("All")
        sleep(10)
        url = 'https://itdashboard.gov/api/v1/ITDB2/visualization/agency/investmentsTable/agencyCode/005'
        
        request = scrapy.Request(url, callback=self.parse_api, headers = self.headers)
        yield request
    
    
    def parse_api(self, response):
        base_url = 'https://itdashboard.gov/drupal/summary/005/'
        raw_data = response.body
        data = json.loads(raw_data)
        with open('Individual_investment.csv', mode='w') as csv_file:
            fieldnames = ['UII', 'agencycode', 'agencyAbbrev', 'bureauName','totalCySpending' 'InvestmentType',
                          'numberOfProjects', 'cioRating']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for val in data['result']:
                writer.writerow({
                    'UII': val['UII'], 
                    'agencycode': val['agencyCode'], 
                    'agencyAbbrev': val['agencyAbbrev'],
                    'bureauName': val['bureauName'],
                    'totalCySpending':val['totalCySpending'] ,
                    'InvestmentType':val['investmentType'],
                    'numberOfProjects': val['numberOfProjects'],
                    'cioRating':val['cioRating']})    
        
        for id in data['result']:
            uii_code = id['UII']
            business_case_doc = base_url + uii_code
        
        
        request = scrapy.Request(business_case_doc, callback=self.download_bcd_api, headers = self.headers)
        yield request
        
    
    def download_bcd_api(self, response):
        raw_data = response.body
        print(type(raw_data))
        data = json.loads(raw_data)
        path = "C:\work\chromedriver.exe"
        driver = webdriver.Chrome(path)
        # for search in data:            
        driver.get(response)
        sleep(20)
        bcd_link = driver.find_element_by_link_text("Download Business Case PDF")
        sleep(10)
        bcd_link.click()
    
        
        
        
            
            
    
        
