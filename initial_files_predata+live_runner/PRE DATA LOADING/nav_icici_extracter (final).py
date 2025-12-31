from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
driver=webdriver.Chrome()
import time
driver= webdriver.Chrome()
driver.get("https://www.nseindia.com/get-quotes/equity?symbol=GOLDIETF")
driver.maximize_window()
time.sleep(3)
inav= driver.find_element(By.XPATH,'//*[@id="iNavValue"]').text
close_price= driver.find_element(By.XPATH,'//*[@id="quoteLtp"]').text
time_date= driver.find_element(By.XPATH,'//*[@id="asondate"]').text
print(f"inav= {inav} & closeprice = {close_price} and date is {time_date}" )
time.sleep(100000)