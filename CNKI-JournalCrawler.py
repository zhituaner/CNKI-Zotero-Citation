#!/usr/bin/env python
# coding: utf-8

import re
import os
import time
import pyautogui
from pprint import pprint
from zhconv import convert
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

Journals={'殷都学刊':'https://navi.cnki.net/knavi/journals/YDXK/detail',
          '甲骨文与殷商史':'https://navi.cnki.net/knavi/journals/JGYS/detail',
          '古文字研究':'https://navi.cnki.net/knavi/journals/GYJW/detail',
          '出土文献与古文字研究':'https://navi.cnki.net/knavi/journals/CTWX/detail'}
journal_choice=pyautogui.confirm(title='CNKI-JournalCrawler',text='请选择需要爬虫的期刊（可修改字典Journals）：',buttons=list(Journals.keys()))
start=time.time()
journal_url=Journals[journal_choice]
journal_abbr=re.compile(r'journals/(.*?)/detail',re.S).findall(journal_url)[0]
print(f'《{journal_choice}》： {journal_url}')

opt=Options()
opt.add_argument('--headless')
opt.add_argument('--disable-gpu')
opt.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
web=Chrome(options=opt)
web.get(journal_url)

bs=BeautifulSoup(web.page_source)
results=[]
results.extend(bs.find_all('dl',attrs={'class':'s-dataList clearfix cur'}))
results.extend(bs.find_all('dl',attrs={'class':'s-dataList clearfix'}))

values=[]
for year in results:
    values.extend(re.compile(r'" value="(.*?)".*?</a>',re.S).findall(str(year)))
for i in range(len(values)):
    values[i]=f'https://navi.cnki.net/knavi/journals/{journal_abbr}/papers?yearIssue='+values[i]+'&pageIdx=0&pcode=CJFD,CCJD'
# pprint(values)

Data=[]
Count=1
for value in values:
    web.get(value)
    sc=web.page_source
    jls=re.compile(r'href=".*?">(.*?)</a>.*?<span class="author">(.*?)</span>',re.S).findall(web.page_source)
    for i in jls:
        Dict={}
        Dict['Count']=Count
        Dict['Title']=convert(i[0],'zh-hans')
        Author=convert(i[1],'zh-hans')
        if Author:
            Author=Author.replace('\n','')
            if Author[-1]==';':
                Author=Author[:-1]
            Author=Author.replace(';','；')
        Dict['Author']=Author
        Data.append(Dict)
        print(f'已加载：{Dict}',end='\r')
        Count+=1
    time.sleep(0.1)
web.quit()

savepath=f'X:/CNKI/【知网期刊】{journal_choice}.md'
with open (savepath,'w',encoding='utf-8') as f:
    f.write(f'## 【知网期刊】[{journal_choice}]({journal_url})（{len(Data)}）\n\n')
    f.write('### Time: '+time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime()))
    f.write('\n\n')
    f.write('|      | 标题 | 作者 |\n')
    f.write('| ---- | ---- | ---- |\n')
    for Dict in Data:
        Count=Dict['Count']
        Title=Dict['Title']
        Author=Dict['Author']
        f.write(f'| **{Count}** | {Title} | {Author} |\n')
print(f'\n获得文章{len(Data)}篇，已写入{os.path.abspath(savepath)}，程序总用时{round(time.time()-start,2)}秒。')
os.system(savepath)