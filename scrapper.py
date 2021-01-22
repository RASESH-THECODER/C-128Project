from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"
browser = webdriver.Chrome("chromedriver_win32\chromedriver.exe")
browser.get(START_URL)
time.sleep(10)

headers = ["Star", "Constellation", "Right ascensation", "App_mag", "Distance","hyperlink"]
planet_data=[]
def scrap():
    for i in range(1,430):
        while True :
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            current_page_numb=int(soup.find_all("input",attributes={"class","page_numb"}).get("value"))
            if current_page_numb  < i :
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif current_page_numb>i:
                browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break

        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyerlink_li_tag=li_tags[0]
            temp_list.append("https://en.wikipedia.org/wiki/List_of_brown_dwarfs"+hyperlink_li_tag.find_all("a",href=True)[0]["href"])
    
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f"{i} page done1")
def scrap_more_data(hyperlink):
    try:
        page=request.get(hyperlink)
        soup=BeautifulSoup(page.content,"html.parser")
        for tr_tag in soup.find_all ("tr",attrs={"class":"fact_rope"}):
            tr_tags=tr_tags.find_all("td")
            temp_list=[]
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div",attrs={"class","value",})[0].contents[0])
                except:
                    temp_list.append("")
            new_planet_data.append(temp_list)
    except:
        time.sleep(1)
        scrap_more_data(hyerlink)

scrap()
for data in planet_data:
    scrap_more_data(data[5])
    print(f"{index+1} page done2")
final_planet_data=[]

for index,data in enumerate (planet_data):
    new_planet_data_element=new_planet_data_element[index]
    new_planet_data_element=[elem.replace("\n","")for elem in new_planet_data_element]
    new_planet_data_element=new_planet_data_element[:7]
    final_planet_data.append(data+new_planet_data_element)

with open ("final.csv","w") as f:
    csvwriter=csv.writer(headers)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_planet_data)