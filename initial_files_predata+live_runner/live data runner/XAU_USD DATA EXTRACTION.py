from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
driver=webdriver.Chrome()
import time
driver.get("https://web.metatrader.app/terminal?lang=en")
driver.maximize_window()
time.sleep(1)
login=driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div/form/div[1]/span/input")
login.send_keys("99455769")
password=driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div/form/div[1]/div[4]/div[1]/div/span/input")
password.send_keys("ErY@B1Ba")

driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div/form/div[2]/div/button").click()
time.sleep(5)
settings=driver.find_element(By.XPATH,"/html/body/div/div[1]/div[1]/div/div/div")
settings.click()
time.sleep(1)
light_or_dark=driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/div[1]/div[2]/div/button[2]')
light_or_dark.click()
time.sleep(1)
search=driver.find_element(By.XPATH,"/html/body/div/div[4]/div/label/input")
search.send_keys("XAUUSD")
XAUUSD=driver.find_element(By.XPATH,'/html/body/div/div[4]/div/div[2]/div/div/div/div/button')
XAUUSD.click()
time.sleep(1)
buy_button= driver.find_element(By.XPATH,"/html/body/div/div[1]/div[2]/div[5]/div")
buy_button.click()
time.sleep(1)

while True:
    price= driver.find_element(By.XPATH,"/html/body/div/div[3]/div/div[2]/div/div[2]/div[2]/div[1]").text

    print(price)
time.sleep(100000)