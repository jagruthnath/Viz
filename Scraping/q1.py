from requests import get
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from ListScrape import *
import numpy as np
import pandas as pd
import threading

def getData(self):
    option = webdriver.ChromeOptions()
    option.add_argument("- incognito")

    browser = webdriver.Chrome(r"C:\Users\Asus\Downloads\chromedriver.exe",chrome_options=option)
    count = 0
    freq = ['1d','1wk','1mo']

    # days_df = pd.DataFrame()
    # weeks_df = pd.DataFrame()
    # months_df = pd.DataFrame()

    for ele in piece:
        for dur in freq:
            count += 1
            url = 'https://finance.yahoo.com/quote/'+ele+'/history?period1=1431887400&period2=1558117800&interval='+dur+'&filter=history&frequency='+dur
            
            browser.get(url)
            #response = get(url)
            #print(response)
            
            
            lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            match=False
            while(match==False):
                lastCount = lenOfPage
                time.sleep(10)
                lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                if lastCount==lenOfPage:
                    match=True
            
            # Now that the page is fully scrolled, grab the source code.
            source_data = browser.page_source
            
            # Throw your source into BeautifulSoup and start parsing!
            #bs_data = bs(source_data)
            html_soup = BeautifulSoup(source_data, 'html.parser')
            
            data = html_soup.find_all('tr')
            print(ele)
            print(len(data))
            
            Date = []
            Open = []
            High = []
            Low = []
            Close = []
            Adj_close = []
            Volume=[]
            
            
            for temp in data:
                if temp.find('td', class_ = 'Py(10px) Ta(start) Pend(10px)')  is not None:
                    
                    t = temp.find_all('td', class_ = 'Py(10px) Pstart(10px)')
                    if len(t) != 0 and t[0].text != '-':
                        Date.append(temp.find('td', class_ = 'Py(10px) Ta(start) Pend(10px)').text)
                        Open.append(t[0].text)
                        High.append(t[1].text)
                        Low.append(t[2].text)
                        Close.append(t[3].text)
                        Adj_close.append(t[4].text)
                        Volume.append(t[5].text)
            
            # if freq == '1d':
            #     days_df = pd.DataFrame({'Symbol':ele,'Date': Date,'Adj Close':Adj_close})
            # if freq == '1wk':
            #     weeks_df = pd.DataFrame({'Symbol':ele,'Date': Date,'Adj Close':Adj_close})
            # if freq == '1mo':
            #     months_df = pd.DataFrame({'Symbol':ele,'Date': Date,'Adj Close':Adj_close})

            stock = pd.DataFrame({'Date': Date,'Open':Open,'High':High
                                  'Close':Adj_close})
        
            stock['Close']=stock['Close'].where(stock['Close']!=0, np.nan) 
            stock["Close"] = stock["Close"].astype('float')        
            daily_pc = stock['Close'] / stock['Close'].shift(1) - 1
            stock["daily_pc"] = -daily_pc
            
            name = 'D:\\Scraping\\Download\\1000Days_'+ele+dur
            stock.to_csv(name+'.csv')
            # days_df.to_csv('D:\\DADV\\Scrape\\Download\\exam_days.csv')
            # weeks_df.to_csv('D:\\DADV\\Scrape\\Download\\exam_weeks.csv')
            # months_df.to_csv('D:\\DADV\\Scrape\\Download\\exam_months.csv')

slices = [tickers[x: x+50] for x in range(0, len(tickers), 10)]

print (slices)
for piece in slices[0:2]:
    threading.Thread(target=getData, args=[piece]).start()