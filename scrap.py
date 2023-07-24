from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from time import sleep
import json

driver = webdriver.Chrome("E:/chromedriver_win32/chromedriver.exe")
alldata=[]

def html_response(url):
    driver.get(url)
    html = r"{}".format(driver.page_source)
    return html

for i in range(1,21):
    print(i)
    url = f"https://www.amazon.in/s?k=bags&page={i}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
    html = html_response(url)
    soup = BeautifulSoup(html,"html.parser")
    if not soup.find('span',class_='s-pagination-strip'):
        break
    break_data = soup.findAll('div',class_='s-latency-cf-section')
    for i in break_data:
        bool_manufacturer = False
        bool_asin = False
        manu = ""
        asin = ""
        sub_data_name_raw = i.find('span',class_='a-size-medium a-color-base a-text-normal')
        if sub_data_name_raw:
            sub_data_name = sub_data_name_raw.text
            sub_data_link_raw = sub_data_name_raw.parent["href"]
            sub_data_link = "https://www.amazon.in"+sub_data_link_raw
            try:
                sub_data_price_raw = i.find('span',class_='a-price-whole')
                sub_data_price = sub_data_price_raw.text
            except:
                sub_data_price = "Noting"
            try:
                sub_data_box = i.find('i',class_='a-icon-star-small')
                sub_data_star_raw = sub_data_box.find('span')
                sub_data_star = sub_data_star_raw.text
                sub_data_next_box = sub_data_box.parent.parent.parent
                sub_data_review_raw = sub_data_next_box.find_next_sibling('span').find('span')
                sub_data_review = sub_data_review_raw.text
            except:
                sub_data_star = "0 out of 0 stars"
                sub_data_review = "0"
            sub_html = html_response(sub_data_link)
            sub_soup = BeautifulSoup(sub_html,"html.parser")
            try:
                sub_product_disc_raw = sub_soup.find('div',id='aplus').find('div')
                sub_product_disc = sub_product_disc_raw.get_text(separator='\n', strip=True)
            except:
                sub_product_disc = None
            try:
                sub_disc_raw = sub_soup.find('div',id='feature-bullets')
                sub_disc = sub_disc_raw.get_text(separator='\n', strip=True)
            except:
                sub_disc = None
            sub_first_details = sub_soup.find('div',id='detailBullets_feature_div')
            sub_sec_details = sub_soup.find('div',id='productDetails_feature_div')
            if sub_first_details:
                sub_details = sub_first_details.findAll('span',class_='a-list-item')
                for sub_detail in sub_details:
                    sub_find_raw = sub_detail.find('span',class_='a-text-bold')
                    sub_find= sub_find_raw.text.lower()
                    if "manufacturer" in sub_find and not bool_manufacturer:
                        manu_raw = sub_find_raw.find_next_sibling('span')
                        manu = manu_raw.get_text(strip=True)
                        bool_manufacturer = True

                    if "asin" in sub_find and not bool_asin:
                        asin_raw = sub_find_raw.find_next_sibling('span')
                        asin = asin_raw.get_text(strip=True)

                        bool_asin = True
                    
                    if bool_manufacturer and bool_asin:
                        break
            elif sub_sec_details:
                sub_details = sub_sec_details.findAll('th')
                for sub_detail in sub_details:
                    sub_find = sub_detail.text.lower()
                    if "manufacturer" in sub_find and not bool_manufacturer:
                        manu_raw = sub_detail.find_next_sibling('td')
                        manu = manu_raw.get_text(strip=True)
                        bool_manufacturer = True

                    if "asin" in sub_find and not bool_asin:
                        asin_raw = sub_detail.find_next_sibling('td')
                        asin = asin_raw.get_text(strip=True)
                        bool_asin = True
                    if bool_manufacturer and bool_asin:
                        break
            else:
                pass
            sub_data = {"url":sub_data_link,"name":sub_data_name,"price":sub_data_price,"rating":sub_data_star,"reviews":sub_data_review,"Product details":{"ASIN":asin,"Manufacturer":manu,"Description":sub_disc,"Product Description":sub_product_disc}}
            alldata.append(sub_data)
driver.quit()
with open("amazon_bags.json",'w',encoding='utf-8') as file:
    file.write(json.dumps(alldata))


