from selenium import webdriver
from time import sleep 
from selenium .webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument('-private')

driver = webdriver.Firefox(options=options)
driver.get('https://the-internet.herokuapp.com/')

elemento = driver.find_element(By.NAME, 'div')
print(elemento.txt)

input('pressione ENTER')
driver.quit()


