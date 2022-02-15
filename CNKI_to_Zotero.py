#!/usr/bin/env python
# coding: utf-8

import os
import time
import pyautogui
from sys import exit
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

start=time.time()
# # 【0】打开Zotero，选择将要导入的文件夹
# os.system('D:/Softwares/Zotero/zotero.exe')

# 【1】配置浏览器参数：ZoteroConnector插件、无图加载、窗口最大化、缩放1.2倍
opt=Options()
opt.add_extension('Zotero Connector.crx') 
opt.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
print('请保持即将弹出的浏览器窗口在最前端，否则会报错NoSuchElementException。')
web=Chrome(options=opt)
web.maximize_window()
web.execute_script('document.body.style.zoom="1.2"')
web.get('https://kns.cnki.net/kns8/defaultresult/index')
bottom_xpath='/html/body/div[5]/div[2]/div[2]' # 【搜索结果页】底端xpath，后续可作为判断是否加载完毕的依据
bottom_xpath_child='/html/body/div[4]/div[2]/div[2]' # 【文献详情页】底端xpath，后续可作为判断是否加载完毕的依据

# 【2】断点，手动检索→继续运行，得到总结果数nums和总页数pages
start_interval=time.time()    
alert=pyautogui.confirm(title='CNKI',text='''1、检索并选择需要导入Zotero的文献；\n2、确保每页显示【50】条结果，以免后续报错；
3、确保【Zotero】处于打开状态，并切换至需要导入文献的分类；\n4、【回到首页】点击继续。''',buttons=['继续','取消'])
end_interval=time.time()
if alert=='取消':
    web.quit()
    print('已关闭浏览器，程序终止运行。')
    exit()
try: # 得到结果总数、总页数
    WebDriverWait(web,15,0.05).until(lambda x:x.find_element(By.XPATH,'//*[@id="countPageDiv"]/span[1]/em'))
    nums=eval(web.find_element(By.XPATH,'//*[@id="countPageDiv"]/span[1]/em').text)
    if isinstance(nums,tuple): # 当结果数≥1000时，获取的nums为元组，形如(1,144)
        nums=eval(''.join([str(i) for i in nums]))
except Exception as e: # nums形如(5,027)时，会因数字以0开头而报错，此时手动输入最为简便
    nums=eval(pyautogui.prompt(title='CNKI',text=''''【错误】'+repr(e)\n请手动输入结果总数：'''))
pages=1 if nums<=50 else eval(web.find_element(By.XPATH,'//*[@id="countPageDiv"]/span[2]').text.split('/')[1])
print(f'共找到{nums}条结果，共{pages}页。即将开始遍历，并将选中的文献导入Zotero……')
saved=0

# 【3】编写函数：翻页、导入Zotero（此部分为保证导入成功，应用较多time.sleep）
def GoToNextPage(): # 此前已判断当前页不是最后一页
    WebDriverWait(web,15,0.05).until(lambda x:x.find_element(By.LINK_TEXT,'下一页'))
    try:
        web.find_element(By.LINK_TEXT,'下一页').click()
    except:
        web.find_element(By.XPATH,'//*[@id="PageNext"]').click()
    time.sleep(1)
    WebDriverWait(web,15,0.05).until(lambda x:x.find_element(By.XPATH,bottom_xpath)) # 翻页后等待页面底端加载

def SaveToZotero(): # 此前已判断复选框□为选中状态☑，并得到对应的文献标题title
    WebDriverWait(web,15,0.05).until(lambda x:x.find_element(By.LINK_TEXT,title))
    try: # 【搜索结果页】→【文献详情页】
        web.find_element(By.LINK_TEXT,title).click()
    except:
        web.find_element(By.XPATH,title_xpath).click()
    web.switch_to.window(web.window_handles[-1])
    WebDriverWait(web,15,0.05).until(lambda x:x.find_element(By.XPATH,bottom_xpath_child)) # 等待页面底端加载完毕
#     此处需要等待Zotero Connector反应，等待的时间很玄学
    time.sleep(3) if saved<10 else time.sleep(1.5)
    pyautogui.moveTo(x/2,y/2) # 将鼠标移动到屏幕中央
    pyautogui.click(button='right')
    pyautogui.press('down',7) # “Save to Zotero”选项
    time.sleep(1.5)
    pyautogui.press(['right','enter','enter']) # 正常为“Save to Zotero(CNKI)”，不正常为保存网页
    time.sleep(0.5)
    web.close() # 【文献详情页】→【搜索结果页】
    web.switch_to.window(web.window_handles[0])
    
# 【4】遍历导入、异常处理
x,y=pyautogui.size()
error_page=[]
for page in range(pages):
    current_page=page+1
    paper_nums=50 if current_page<pages else nums-50*(pages-1) # 每页文献数量paper_nums，特殊情况：共一页；多页的最后一页
    try:
        if not current_page==pages:
            WebDriverWait(web,15,0.05).until(lambda x:x.find_element(By.LINK_TEXT,'下一页'))
        for i in range(paper_nums):
            paper_order=i+1 # 每页的第几篇文献
            checkbox_xpath=f'//*[@id="gridTable"]/table/tbody/tr[{paper_order}]/td[1]/input'
            WebDriverWait(web,15,0.05).until(lambda x:x.find_element(By.XPATH,checkbox_xpath))
            if web.find_element(By.XPATH,checkbox_xpath).is_selected(): # 选中文献时
                title_xpath=f'//*[@id="gridTable"]/table/tbody/tr[{paper_order}]/td[2]/a'
                WebDriverWait(web,15,0.05).until(lambda x:x.find_element(By.XPATH,title_xpath))
                title=web.find_element(By.XPATH,title_xpath).text
                order=paper_order=paper_order+50*(current_page-1) # 结果总数中的第几篇文献
                print(f'第{current_page}页·第{order}篇：{title}')
                SaveToZotero()
                saved+=1 # 最终得到导入Zotero的文献总数
    except Exception as e:
        print(f'【错误：第{current_page}页】{e}')
        error_page.append(current_page)
        continue
    if current_page<pages:
        GoToNextPage()
if not error_page:
    web.close()
else:
    print(f'第{error_page}页加载失败！')
print(f'导入Zotero【{saved}】篇文献，程序共用时{round((time.time()-start-(end_interval-start_interval))/60,2)}分钟。')