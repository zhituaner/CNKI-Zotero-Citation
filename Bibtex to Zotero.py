#!/usr/bin/env python
# coding: utf-8

import re
import os
import time
import pyperclip
import pyautogui
from pprint import pprint
from zhconv import convert
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

start_bib=time.time()
url=pyperclip.paste()
print(f'文献详情页 {url}')
try:
    url_obj=re.compile(r'dbname=(.*?)&filename=(.*?)&',re.S)
    url_result=url_obj.findall(url)
    assert url_result !=[]
    dbname,filename=url_result[0][0],url_result[0][1]
except:
    try:
        url_obj=re.compile(r'filename=(.*?)&dbname=(.*?)&',re.S)
        url_result=url_obj.findall(url)
        assert url_result !=[]
        dbname,filename=url_result[0][1],url_result[0][0]
    except:
        url_obj=re.compile(r'filename=(.*?)&dbcode=.*?&dbname=(.*?)&',re.S)
        url_result=url_obj.findall(url)
        assert url_result !=[]
        dbname,filename=url_result[0][1],url_result[0][0]
# print(url_result)
assert url_result !=[]

opt=Options()
opt.add_argument('--headless')
opt.add_argument('--disable-gpu')
opt.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
web_bib=Chrome(options=opt)
# web_bib.maximize_window()

url_info=f'https://kns.cnki.net/kns8/manage/export?filename={filename}&dbname={dbname}'
print(f'文献信息页 {url_info}')
web_bib.get(url_info)
WebDriverWait(web_bib,15,0.5).until(lambda x:x.find_element(By.LINK_TEXT,'自定义'))
web_bib.find_element(By.LINK_TEXT,'自定义').click()
WebDriverWait(web_bib,15,0.5).until(lambda x:x.find_element(By.LINK_TEXT,'全选'))
web_bib.find_element(By.LINK_TEXT,'全选').click()
web_bib.find_element(By.LINK_TEXT,'预览').click()
time.sleep(1)
info=web_bib.find_element(By.CLASS_NAME,'literature-list').get_attribute('innerHTML')
web_bib.quit()
# pprint(info)

info=convert(info,'zh-hans')
try: # 题名
    obj_title=re.compile(r'Title-题名:(.*?)<br>',re.S)
    title=obj_title.findall(info)[0].replace(' ','')
except:
    title=''
try: # 作者【注意多个作者的情况！】
    obj_author=re.compile(r'Author-作者:(.*?)<br>',re.S)
    author=obj_author.findall(info)[0].replace(' ','')
    if author.count(';')<=1:
        author=author.replace(';','')
    else: # 多个作者：author应当形如 {{常玉芝} and {王曾瑜}}
        templs=author.split(';')
        author=''
        for j in range(len(templs),-1,-1):
            if j=='\n' or j=='':
                del templs[j]
        for i in templs:
            i=i.replace(' ','')
            i=i.replace('\n','')
            author+=('{'+i+'} and ')
        author=author[:-5]
#     print(f'作者：author（用于检查）')
except:
    author=''
try: # 文献来源（期刊名）
    obj_source=re.compile(r'Source-文献来源:(.*?)<br>',re.S)
    source=obj_source.findall(info)[0].replace(' ','')
except:
    source=''
try: # 摘要
    obj_summary=re.compile(r'Summary-摘要:(.*?)<br>',re.S)
    summary=obj_summary.findall(info)[0].replace(' ','').replace('&lt;正&gt;','')
except:
    summary=''
try: # 年
    obj_year=re.compile(r'Year-年:(.*?)<br>',re.S)
    year=obj_year.findall(info)[0].replace(' ','')
except:
    pubtime=''
try: # 卷
    obj_volume=re.compile(r'Volume-卷:(.*?)<br>',re.S)
    volume=obj_volume.findall(info)[0].replace(' ','')
except:
    volume=''
try: # 期
    obj_period=re.compile(r'Period-期:(.*?)<br>',re.S)
    period=obj_period.findall(info)[0].replace(' ','')
except:
    period=''
try: # 页码
    obj_pagecount=re.compile(r'PageCount-页码:(.*?)<br>',re.S)
    pagecount=obj_pagecount.findall(info)[0].replace(' ','')
except:
    period=''

# bibtex='''@article{title = {%s},author = {%s},year = {%s},journal = {%s},volume = {%s},number = {%s},\
# pages = {%s},url = {%s},abstract = {%s}}''' %(title,author,year,source,volume,period,pagecount,url,summary)
# 以上Bibtex有一定概率识别失败，可能为缩进原因
bibtex='''@article{
    title = {%s},
    author = {%s},
    year = {%s},
    journal = {%s},
    volume = {%s},
    number = {%s},
    pages = {%s},
    url = {%s},
    abstract = {%s}
}''' %(title,author,year,source,volume,period,pagecount,url,summary)
print(bibtex)
os.system('D:/Softwares/Zotero/zotero.exe')
pyperclip.copy(bibtex)
time.sleep(0.5) # 应确保Zotero提前打开
pyautogui.keyDown('ctrl'); pyautogui.keyDown('shift'); pyautogui.keyDown('alt'); pyautogui.keyDown('i')
pyautogui.keyUp('i'); pyautogui.keyUp('alt'); pyautogui.keyUp('shift'); pyautogui.keyUp('ctrl') # 千万别忘了w
end_bib=time.time()
print(f'理论上已导入{author}：《{title}》，用时{round(end_bib-start_bib,2)}秒。（如未成功导入，请手动按快捷键Ctrl+Shift+Alt+I）')
