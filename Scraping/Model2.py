from selenium import webdriver
import time
import ListScrape as c
import threading
import numpy as np
import pandas as pd

def getData(self):
	count = 0
	freq = ['1d','1wk','1mo']
	for company in piece:
		for dur in freq:
			url = 'https://finance.yahoo.com/quote/'+company+'/history?period1=1431887400&period2=1558117800&interval='+dur+'&filter=history&frequency='+dur
			option = webdriver.ChromeOptions() 
			option.add_argument("--incognito")
			if dur == '1d':
				option.add_experimental_option("prefs",{"download.default_directory":"D:\Scraping\Download\Daily"})
			elif dur == '1wk':
				option.add_experimental_option("prefs",{"download.default_directory":"D:\Scraping\Download\Weekly"})
			else:
				option.add_experimental_option("prefs",{"download.default_directory":"D:\Scraping\Download\Monthly"})

			browser = webdriver.Chrome(r"C:\Users\Asus\Downloads\chromedriver.exe",chrome_options=option)
			browser.get(url)
			browser.maximize_window()
			browser.find_element_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a').click()
			time.sleep(10)
			browser.quit()  
        
slices = [c.tickers[x: x+10] for x in range(0, len(c.tickers), 10)]
print (slices)
for piece in slices[11:20]:
    threading.Thread(target=getData, args=[piece]).start()