import pandas as pd
import numpy as np
import os
import params as pa
import time
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from Crawl import extract_data as extract
pd.set_option('display.Width', 5000)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)


def driversetting(DownloadPath):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {"download.default_directory": pa.DownloadPath,
                                              "download.prompt_for_download": False,
                                              "download.directory_upgrade": True,
                                              "safebrowsing_for_trusted_source_enabled": False,
                                              "safebrowsing.enabled": False})

    #options.add_argument("headless") # 켜두면 크롬창이 뜨지않고 실행됨
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shn-usage')
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(pa.waitseconds)

    return driver


def gen(TargetDay,Farm):#TargetDay, Farm, Method

    driver = driversetting(pa.DownloadPath)

    driver.get(pa.HYOSUNG)
    print('run website')
    time.sleep(pa.waitseconds)




    driver.find_element(By.XPATH, '//*[@id="Txt_1"]').send_keys('jarasolar')
    driver.find_element(By.XPATH, '//*[@id="Txt_2"]').send_keys('abcd1234')
    driver.find_element(By.XPATH, '//*[@id="imageField"]').click()

    print('login')
    time.sleep(pa.waitseconds)

    # 팝업닫기
    driver.find_element(By.XPATH, '//*[@id="popupContainer"]/div/div/div/div[2]/button[1]').click()



    driver.find_element(By.XPATH, '//*[@id="form1"]/div[4]/div[1]/div/ul[2]/a[5]/li').click()
    print('Satistical Report')
    time.sleep(pa.waitseconds)

    #16MW
    driver.find_element(By.XPATH, '//*[@id="SrTop_cbo_plant"]/option['+ str(Farm) + ']').click()
    print('Select Farm')
    time.sleep(pa.waitseconds)

    #Date Clear
    driver.find_element(By.XPATH, '//*[@id="txt_Calendar"]').clear()
   #time.sleep(pa.waitseconds)

    # Date Input
    driver.find_element(By.XPATH, '//*[@id="txt_Calendar"]').send_keys(TargetDay)
    print('Put new date')
    time.sleep(pa.waitseconds)

    # Close the calender
    driver.find_element(By.XPATH, '//*[@id="txt_Calendar"]').send_keys(Keys.ENTER)
    print('Close the calender')
    time.sleep(pa.waitseconds)

    # Search
    driver.find_element(By.XPATH, '//*[@id="submitbtn"]').click()
    print('Search')
    time.sleep(pa.waitseconds)

    # Download

    driver.find_element(By.XPATH, '//*[@id="exldownbtn"]').click()

    print('Download')

    time.sleep(pa.waitseconds)
    driver.quit() # 드라이버종료
    print('quit driver')





    # 다운로드한 파일명 html로 바꾸기
    print("rename file")
    today_date_str = datetime.date.today().strftime("%Y-%m-%d")
    downloaded_filename = "TimeData_" + today_date_str + ".xls"
    downloaded_file_path = os.path.join(pa.DownloadPath, downloaded_filename)  # 다운로드한 파일 경로 및 이름
    new_file_name = os.path.join(pa.DownloadPath, "TimeData_"+TargetDay+".html")  # 새 파일 이름 및 경로
    os.rename(downloaded_file_path, new_file_name)

    # html에서 데이터뽑아서 데이터프레임만들기
    Data = extract.extract_data_from_html(os.path.join(downloaded_file_path,new_file_name))
    # 파일 사용 후 삭제
    # os.remove(new_file_name)
    print("file deleted")
    driver.service.process.send_signal("SIGTERM")
    driver.service.process.terminate()

    return Data

if __name__ == '__main__':

    Farm =1
    TargetDay = '2023-03-03'
    gen(TargetDay, Farm)