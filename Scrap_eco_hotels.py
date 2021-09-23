import re
import json
import csv
import time
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.common.keys import Keys

from selenium import webdriver
driver = webdriver.Chrome("./chromedriver")
driver.get("https://www.iranhotelonline.com/ecolodge/")
time.sleep(5)

urls=[]
for j in range(1):
    # driver.get("https://www.iranhotelonline.com/ecolodge/")
    cities = driver.find_elements_by_xpath('/html/body/div[7]/div[1]/div/div[{:}]/a'.format(j+1))
    # cities.click()
    for i in cities:
        names = i.get_attribute("href")
        urls.append(names)

uls_list=[]


for url in urls:
    driver.get(url)
    time.sleep(5)
    i = True
    while i:
        ul = driver.find_elements_by_class_name('name-hotel')
        # name_hotel=ul.text
        # print(name_hotel,"namehotel")

        for d in ul:
            uls = d.get_attribute("href")
            uls_list.append(uls)
            print(uls)

        try:
            badi = driver.find_element_by_link_text("بعدی")
            badi.click()
            time.sleep(5)
        except:
            i=False

print(uls_list)

featuress=[]
Boomgardi_lst=[]
cunter=0
for urls in uls_list:
    driver.get(urls)
    time.sleep(5)
    try:
        title = driver.find_element_by_xpath("/html/body/span/div[1]/div[1]/div[1]")
        titles= title.text
        # print(titles)
    except:
        titles=None

    try:
        addres = driver.find_element_by_xpath("/html/body/span/div[1]/div[1]/div[2]/p[1]")
        addresss = addres.text
        address = addresss.replace('( نقشه هتل )', '')
        print(address)
        # print(address)
    except:
        address = None

    try:
        telphone = driver.find_element_by_xpath("/html/body/span/div[1]/div[1]/div[2]/p[2]/span")
        telphones = telphone.text
        # print(telphones)
    except:
        telphones = None

    try:
        # gheymat = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_rpt_hotel_info_ctl00_div_price"]/span[1]')
        # gheymate=gheymat.text
        # print(gheymate)
        price = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_rpt_hotel_info_ctl00_lbl_iho_price_start"]')
        prices = price.text
        print(prices)
        # old_price = driver.find_element_by_xpath(
        #     '//*[@id="ctl00_ContentPlaceHolder1_rpt_hotel_info_ctl00_lbl_hotel_price_start"]')
        # new_price = driver.find_element_by_xpath(
        #     '//*[@id="ctl00_ContentPlaceHolder1_rpt_hotel_info_ctl00_lbl_iho_price_start"]')
        # prices = price.text
        # old_prices = old_price.text
        # new_prices = new_price.text
        # new_price = prices - old_prices
        # print(new_prices)
    except:
        prices = None

    try:
        feature = driver.find_element_by_xpath('//*[@id="hotel_facilities"]')
        features = feature.text
        # featuress.append(features)
        # print(features)
    except:
        features = None
    try:
        rate = driver.find_element_by_xpath('//*[@id="view_section"]/div/div[2]/div[1]/div[1]/div/div[1]/span')
        rates = rate.text
        # print(rates)
    except:
        rates = None
    try:
        # driver.get("https://www.iranhotelonline.com/isfahan-hotels/%D9%87%D8%AA%D9%84-%D9%BE%D8%A7%D8%B1%D8%B3%DB%8C%D8%A7%D9%86-%DA%A9%D9%88%D8%AB%D8%B1/")
        tag = driver.find_element_by_xpath('//*[@id="googleMapSmall"]/script')
        x = tag.get_attribute('innerHTML')
        result = re.search(r"\[.*?]", x)
        results = result.group(0)
        # print(results)

    except:
        results = None

    hotel={
        # "price": prices,

        # "city": "Ardabil",
        # "province": "Ardabil",
        "telephone": telphones,

        "geolocation": {
            "lat": results,
            "lon": results
                        },

       "name": titles,
       "star_count": "",
       "rating":rates,
       "address": address ,
       "free_services": features,
       "type": "هتل",
        "category": "Hotel",
        "status": 1}


    print(hotel)
    Boomgardi_lst.append(hotel)

    cunter+=1
    print(cunter)


#
json_object = json.dumps(Boomgardi_lst, indent=2, ensure_ascii=False, default=str)
with open("Boomgardi_list2.json", "a+") as outfile:
    outfile.write(json_object)


