from asyncio.windows_events import NULL
from operator import indexOf
from pickle import FALSE
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np

def RunAllDownloads(period, ticker):
            if (period == 'Trimestrais'):
                try:
                    download_and_rename('160_anchor', ticker)
                    time.sleep(0.5)
                    download_and_rename('135_anchor', ticker)
                    time.sleep(5)
                except:
                    try:
                        download_and_rename('78_anchor', ticker)
                        time.sleep(5)
                    except:
                        return None
            else:
                try:
                    download_and_rename('370_anchor', ticker)
                    time.sleep(0.5)
                    download_and_rename('345_anchor', ticker)
                    time.sleep(5)
                except:
                    try:
                        download_and_rename('278_anchor', ticker)
                        time.sleep(5)
                    except:
                        return None
    

def download_and_rename(id, ticker):
    try:    
        DRIVER.find_element(By.ID, id).click()
    except:
        return None
    try:
        if id == '160_anchor' or id == '370_anchor':
            DRIVER.find_element(By.TAG_NAME, 'button').click()
            time.sleep(5)
            files = os.listdir(PATH)
            for file in files:
                if file.endswith('pdf'):
                    old_file = file
            while not os.path.exists(PATH + old_file):
                time.sleep(2)      
            os.remove(PATH + old_file)
        else:
            DRIVER.find_element(By.TAG_NAME, 'button').click()
            WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.TAG_NAME, "button")))
            time.sleep(15)
            DRIVER.find_element(By.ID, id).click()
            files = os.listdir(PATH)
            for file in files:
                if file.endswith('pdf'):
                    old_file = file
            while not os.path.exists(PATH + old_file):
                time.sleep(2)    
            old_file = files[0]
            new_file = ticker + "-" + old_file
            os.rename(PATH + old_file, PATH + new_file)
            while not os.path.exists(PATH + new_file):
                time.sleep(1) 
            if (os.path.isdir(PATH + ticker)):
                shutil.move(PATH + new_file, PATH  + ticker)
                while not os.path.exists(PATH + ticker + "\\" + new_file):
                    time.sleep(1)
                DRIVER.find_element(By.ID, id).click()
            else:
                os.makedirs(PATH  + ticker)
                while not os.path.exists(PATH + ticker):
                    time.sleep(1) 
                shutil.move(PATH + new_file, PATH  + ticker)
                while not os.path.exists(PATH + ticker + "\\" + new_file):
                    time.sleep(1)
                DRIVER.find_element(By.ID, id).click()
    finally:
        DRIVER.find_element(By.ID, id).click()

        
def get_right_page_to_download(period, ticker):
            time.sleep(1)
            WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
            tab1 = DRIVER.window_handles[0]
            tab2 = DRIVER.window_handles[1]
            DRIVER.switch_to.window(tab2)
            DRIVER.find_element(By.ID, 'btnGeraRelatorioPDF').click()
            time.sleep(1)
            WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.ID, 'iFrameModal')))
            src2 = DRIVER.find_element(By.ID, "iFrameModal").get_attribute("src")
            DRIVER.get(src2)
            time.sleep(1)
            WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.ID, '0_anchor')))
            
            DRIVER.find_element(By.ID, '0_anchor').click()
            RunAllDownloads(period, ticker)


            DRIVER.close()
            DRIVER.switch_to.window(tab1)

def js_script1(driver):
    js = """
    const select = document.querySelector('#selectPage');
    var opt = document.createElement('option')
    opt.value = "3000";
    opt.innerHTML = "5";
    opt.id = "opcao3000";
    select.appendChild(opt);
    """
    driver.execute_script(js)
    driver.find_element(By.ID, 'opcao3000').click()

def SelectCompanyPage():
    try: 
        tabs = DRIVER.window_handles
        DRIVER.switch_to.window(tabs[0])
        DRIVER.get(URL)

        src = DRIVER.find_element(By.XPATH, "//iframe").get_attribute("src")
        DRIVER.get(src)

        xpathTodos = "//button[@class='btn btn-light btn-block mt-3']"
        DRIVER.find_element(By.XPATH, xpathTodos).click()
        WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
        time.sleep(1)
        tabsCount = len(tabs)
        while (tabsCount > 1):
            DRIVER.switch_to.window(tabs[tabsCount - 1])
            DRIVER.close()
            tabsCount = tabsCount - 1
    except: 
        print("Erro em: " + ERRO)
        tabs = DRIVER.window_handles
        DRIVER.switch_to.window(tabs[0])
        DRIVER.refresh()
        SelectCompanyPage()
        
def SelectBalanceForAll():
    for x in range(NUMBER, 2257):
        try:   
            time.sleep(1)
            js_script1(DRIVER)
            time.sleep(2)
            WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
            cards = DRIVER.find_elements(By.CLASS_NAME, CLASSCARD)
            while (len(cards) == 0):
                cards = DRIVER.find_elements(By.CLASS_NAME, CLASSCARD)      
            cards[x].click()
            time.sleep(1)
            WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'select')))
            urlSplit = DRIVER.current_url.split('/')
            ticker = urlSplit[6]
            ERRO = ticker + " " + str(x)
            selectionOptions = DRIVER.find_element(By.TAG_NAME,'select').find_elements(By.TAG_NAME, 'option')
            for option in selectionOptions:
                if option.accessible_name == 'Relatórios Estruturados':
                    option.click()
                    WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h3')))
                    time.sleep(2)
                    yearOptions = len(DRIVER.find_element(By.ID, 'selectYear').find_elements(By.TAG_NAME, 'option'))
                    for yearOption in range(0, 12):
                        DRIVER.find_element(By.ID, 'selectYear').find_elements(By.TAG_NAME, 'option')[yearOption].click()
                        WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'select')))
                        time.sleep(2)
                        textsClicklable = DRIVER.find_elements(By.TAG_NAME, 'a')            
                        for textClickable in textsClicklable:
                            time.sleep(1)
                            if 'Trimestrais' in textClickable.accessible_name:
                                WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'select')))
                                textClickable.click()
                                get_right_page_to_download('Trimestrais', ticker)
                            elif 'Financeiras' in textClickable.accessible_name:
                                WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'select')))
                                textClickable.click()
                                get_right_page_to_download('Financeiras', ticker)          
            SelectCompanyPage()
        except:
            print("Erro em: " + ERRO)
            SelectCompanyPage()
            
def SelectCompanyPageForOne(Company):
    time.sleep(1)
    js_script1(DRIVER)
    time.sleep(2)
    WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
    cards = DRIVER.find_elements(By.CLASS_NAME, CLASSCARD)
    while (len(cards) == 0):
        cards = DRIVER.find_elements(By.CLASS_NAME, CLASSCARD)
        
    for card in cards:
        y = card.find_element(By.TAG_NAME, 'h5').accessible_name
        if (y == Company):                
            try:   
                card.click()
                time.sleep(1)
                WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'select')))
                urlSplit = DRIVER.current_url.split('/')
                ticker = urlSplit[6]
                ERRO = Company
                selectionOptions = DRIVER.find_element(By.TAG_NAME,'select').find_elements(By.TAG_NAME, 'option')
                for option in selectionOptions:
                    if option.accessible_name == 'Relatórios Estruturados':
                        option.click()
                        WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h3')))
                        time.sleep(2)
                        yearOptions = len(DRIVER.find_element(By.ID, 'selectYear').find_elements(By.TAG_NAME, 'option'))
                        for yearOption in range(0, 12):
                            DRIVER.find_element(By.ID, 'selectYear').find_elements(By.TAG_NAME, 'option')[yearOption].click()
                            WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'select')))
                            time.sleep(2)
                            textsClicklable = DRIVER.find_elements(By.TAG_NAME, 'a')            
                            for textClickable in textsClicklable:
                                time.sleep(1)
                                if 'Trimestrais' in textClickable.accessible_name:
                                    WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'select')))
                                    textClickable.click()
                                    get_right_page_to_download('Trimestrais', ticker)
                                elif 'Financeiras' in textClickable.accessible_name:
                                    WebDriverWait(DRIVER, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'select')))
                                    textClickable.click()
                                    get_right_page_to_download('Financeiras', ticker)          
                SelectCompanyPage()
            except:
                print("Erro em: " + ERRO)
                SelectCompanyPage()
        

    
   
ERRO = "fora da página da empresa"
PATH = input("Digite o caminho a ser salvo: ")   
while (not os.path.exists(PATH)):    
    PATH = input("Digite o caminho a ser salvo: ")
PATH = PATH + "\\"
URL = "https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/empresas-listadas.htm"
options = Options()
pathGoogle = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
prefs = {'download.default_directory' : PATH}
prefs2 = {'profile.default_content_setting_values.automatic_downloads': 1}
prefs.update(prefs)
options.add_argument("start-maximized")
options.add_experimental_option('prefs', prefs)
OPTION = input("Para baixar tudo digite 1, para baixar por empresa digite 2: ")

if (OPTION == "1"):
    NUMBER = int(input("Número de onde parou: "))   
    DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    CLASSCARD = "card-body"
    SelectCompanyPage()
    SelectBalanceForAll()
    
elif (OPTION == "2"):
    NUMBER = 2256
    Company = input("Ticker: ").upper()
    DRIVER = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    CLASSCARD = "card-body"
    SelectCompanyPage()
    SelectCompanyPageForOne(Company)
    
    
        


