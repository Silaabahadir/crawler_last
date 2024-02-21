from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By

DRIVER_PATH = "/home/sila/Downloads/chromedriver-linux64(1)/chromedriver-linux64"
const_row = ['', '', '', '', '', '']

options=webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

driver.get('https://akademik.yok.gov.tr/AkademikArama/AkademisyenArama?islem=vrIE273vN0X7kdp6t8ylhh7WEh1kCPL2n3CV9jaCAcheEQelTm-XyRhBW_4oLHrN')

df = pd.read_csv("veriler.csv")
page_end = False
page_number = 0
while True:
    page_number += 1
    link_list = driver.find_element(By.CLASS_NAME,"pagination")
    try:
        active_link = link_list.find_element(By.LINK_TEXT,str(page_number))
    except:
        try:
            active_link = link_list.find_element(By.LINK_TEXT,"»")
        except:
            break
        
    
    driver.get(active_link.get_attribute("href"))
    
    author_div = driver.find_element(By.ID,"authorlistTb")
        
    a_list = author_div.find_elements(By.TAG_NAME,"a")
        
    a_list_last = [elm.text for elm in a_list if elm.text != '']
        
    h6_list = author_div.find_elements(By.TAG_NAME,"h6")
        
    h6_list_last = [elm.text for elm in h6_list]
        
    h6_index = 0
    try:
        for text in a_list_last:
            if text.isupper() and text!="TIP":
                df.loc[len(df)] = const_row
                df.loc[len(df) - 1]["Adi_Soyadi"] = text
                df.loc[len(df) - 1]["Unvan"] = h6_list_last[h6_index]
                df.loc[len(df) - 1]["Uni_Bolum_ABD"] = h6_list_last[h6_index + 1]
                h6_index += 2

            elif text.find("Alanı") >= 0 or text.find("Mimarlık-Planlama-Tasarım")>= 0:
                df.loc[len(df) - 1]["Alani"] = text

            elif text.find("[at]") >= 0:
                df.loc[len(df) - 1]["email"] = text
            else:
                df.loc[len(df) - 1]["Konular"] += text + ","
    except:
        continue
df.to_csv("son.csv")

