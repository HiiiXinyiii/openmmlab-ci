import sys

from selenium import webdriver
from time import sleep
 

def test_lang_switcher():
    """Checking whether lang changed or not if lang-swithcer clicked
    """
    chrome_driver = webdriver.Chrome()
    
    chrome_driver.get()
    chrome_driver.maximize_window()
    chrome_driver.close()

