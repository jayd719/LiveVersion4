"""
-------------------------------------------------------
Downloads Current logged in info
-------------------------------------------------------
Author:  JD
ID:      #
Email:   jsingh@live.com
__updated__ = "2023-05-27"
-------------------------------------------------------
"""

# Imports
from playwright.sync_api import sync_playwright
from time import sleep
from datetime import datetime


def message():
    return

HEADLESS = False
E2_WEB_ADDRESS='https://canadianbab.mye2shop.com/t3/'

def main():
    def data(webpage):
        webpage.click('//*[@id="sidebar"]/div[1]/div[1]/ul/li[3]')
        with webpage.expect_download() as download_info:
            webpage.click('//*[@id="btnPrint_gvJobClockInDetails"]')
        download_info.value.save_as(f'../GridExport1.xlsx')
        print(datetime.today())
        sleep(1)


    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS, slow_mo=00)
        webpage = browser.new_page()
        webpage.goto(E2_WEB_ADDRESS)
        webpage.fill('input#username', "")
        webpage.fill('input#password', "")
        webpage.click('button#login')
        webpage.click('div#product-quickview')
        if webpage.url != 'https://canadianbab.mye2shop.com/DashboardQV':
            webpage.click('//*[@id="baseModal"]/div/div/div[3]/span/button[2]')

        while True:
            while True:
                try:
                    data(webpage)
                except:
                    data(webpage)



if __name__ == '__main__':
    main()




        
        
            
           
        
