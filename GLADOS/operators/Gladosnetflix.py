import pathlib
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pathlib
import os
class GladosNetflix():
    def __init__(self,email,password,movie):
        os.chdir(pathlib.Path(__file__).parent.resolve())
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)
        self.driver_path = path_parent + r'\chromedriver.exe'
        self.Email=email
        self.Password=password
        self.Movie=movie
    def Glados_netflix(self):
        options = webdriver.ChromeOptions() 
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("user-data-dir=C:\\Path") #Path to your chrome profile
        driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=options)
        driver.maximize_window()
        driver.get("https://www.netflix.com/tr/login")
        #username
        driver.find_element_by_name("userLoginId").send_keys(self.Email)
        #password
        driver.find_element_by_name("password").send_keys(self.Password)
        #click login
        driver.find_element_by_css_selector("button[data-uia=login-submit-button]").send_keys(Keys.ENTER)
        time.sleep(4)
        #Profile Selection
        #profile = driver.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[2]/div/div/ul/li[1]/div/a/div/div')
        #driver.find_element_by_link_text("Nipponsensei").click(Keys.ENTER)
        
        #time.sleep(3)
        #driver.find_element_by_xpath('//*[@id="main-view"]/div/span/div/div/div/div/div/div[2]/div/div/div[3]/a/button').click()
        #Choose yourself
        """      #driver.find_element_by_xpath('//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div/div/div/div[1]/div/button/span').click()
            searchTab =  driver.find_element_by_name("Ara")
            searchTab.click()
            time.sleep(3)
            inputElement = driver.find_element_by_name("searchInput")
            inputElement.send_keys(text)
            inputElement.submit()
            time.sleep(2) """
        
        #driver.find_element_by_css_selector('input[data-uia= "search-box-input"]').send_keys(title)
        #driver.find_element_by_css_selector(" #searchInput > div.ptrack-content").send_keys(title)
        #Enter in the search field
        #driver.find_element_by_css_selector("#title-card-0-0 > div.ptrack-content").click()
        #time.sleep(2)
        #driver.find_element_by_css_selector("#pane-Overview > div > div > div > div.ptrack-content > div > div.jawbone-actions > a.playLink.isToolkit > button").click()
        #Click play
        #driver.quit()
