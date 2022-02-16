#!/usr/bin/env python
# coding: utf-8

from os import path
from pyperclip import copy
from pandas import read_csv
from pyautogui import confirm,prompt

# 【1】指定路径
path_in='我的文库.csv' # 由Zotero导出的文献数据源，放在程序同级目录下（或指定路径）
path_out='Library.csv' # 删除无用信息（极易导致报错）并另存

# 【2】编写函数，处理数据【核心在本部分Citation()函数】
def Library(): # 删除Zotero导出.csv文件中的无用列，并另存
    data=read_csv(path_in,encoding='UTF-8-sig')
    data_new=data.drop(['Key','ISBN','ISSN','DOI','Abstract Note','Date Added','Date Modified','Access Date','Number Of Volumes',
                        'Journal Abbreviation','Short Title','Series','Series Number','Series Text','Series Title','Rights',
                        'Archive','Archive Location','Library Catalog','Call Number','Extra','Notes','File Attachments',
                        'Link Attachments','Manual Tags','Automatic Tags','Artwork Size','Filing Date','Application Number',
                        'Assignee','Issuing Authority','Country','Meeting Name','Conference Name','Court','References',
                        'Reporter','Legal Status','Priority Numbers','Programming Language','Version','System','Code',
                        'Code Number','Section','Session','Committee','History','Legislative Body','Editor','Series Editor',
                        'Translator','Contributor','Attorney Agent','Book Author','Cast Member','Commenter','Composer',
                        'Cosponsor','Counsel','Interviewer','Producer','Recipient','Reviewed Author','Scriptwriter','Words By',
                        'Guest','Number','Edition','Running Time','Scale','Medium','Language','Num Pages'],axis=1)
    data_new.to_csv(path_out,index=0,encoding='UTF-8-sig')
    print(f'已简化【{path.abspath(path_in)}】并另存为【{path_out}】。')

def Data(): # 读取Library.csv并生成列表datals，其每个元素即为各个存储文献信息的字典
    ls,datals=[],[]
    with open(path_out,encoding='UTF-8-sig') as f:
        for line in f:
            line=line.strip().split(',')
            ls.append(line)
    lt=ls[0];del ls[0]
    for i in range(len(ls)):
        dx={}
        for j in range(len(lt)):
            dx[lt[j]]=ls[i][j]
        datals.append(dx)
    print(f'成功读取【{path.abspath(path_out)}】并生成数据源datals。')
    print(f'检索文献字典可用索引：{lt}')
    return datals

# ★【核心】在Citation()函数中根据文献类型自定义引文格式
# 以下提供Zotero【文献类型】和每条文献信息的【字典索引】
# ★文献类型：书籍【'book'】；图书章节【'bookSection'】；期刊文章【'journalArticle'】；学位论文【'thesis'】；
        # 报纸文章【'newspaperArticle'】；网页【'webpage'】；百科全书文章【'encyclopediaArticle'】；会议论文【'conferencePaper'】
def Citation():
# ★字典索引：
    # （通用）文献类型【'Item Type'】；出版年份【'Publication Year'】；作者【'Author'】；标题【'Title'】；页码【'Pages'】
    ItemType=data['Item Type'] # 以下：值为空时以醒目的“【】”代替，从而提示修改
    PublicationYear=int(eval(data['Publication Year'])) if data['Publication Year'] else '【】'
    Author=data['Author'] if data['Author'] else '【】'
    Title=data['Title']
    Pages=data['Pages'] if data['Pages'] else '【】'
    # ★（期刊文章、报纸文章、会议论文类）期刊名【'Publication Title'】；卷【'Volume'】；期【'Issue'】
    if ItemType in ['journalArticle','newspaperArticle','conferencePaper']:
        PublicationTitle=data['Publication Title'] if data['Publication Title'] else '【】'
        Volume=int(eval(data['Volume'])) if data['Volume'] else '【】'
        Issue=int(eval(data['Issue'])) if data['Issue'] else '【】'
        citation=f'{Author}：《{Title}》，《{PublicationTitle}》{PublicationYear}年第{Issue}期。'
    # ★（书籍、图书章节类）出版社【'Publisher'】；出版地【'Place'】
    elif ItemType in ['book','bookSection']:
        Publisher=data['Publisher'] if data['Publisher'] else '【】'
        Place=data['Place'] if data['Place'] else '【】'
        citation=f'{Author}：《{Title}》，{Place}：{Publisher}，{PublicationYear}年，第{Pages}页。'
    # ★（网页、百科全书类）网页链接【'Url'】；网页日期【'Date'】
    elif ItemType in ['webpage','encyclopediaArticle']:
        Url=data['Url'] if data['Url'] else '【】'
        Date=data['Date'] if data['Date'] else '【】'
        citation=f'{Author}：《{Title}》，{Author} {Url}，{Date}。'
    # ★（学位论文类）硕士or博士【'Type'】
    elif ItemType in ['thesis']:
        Type=data['Type'] if data['Type'] else '【】'
        citation=f'{Author}：《{Title}》，{Type}，{PublicationYear}年，第{Pages}页。'
    else:
        print(f'该类型【{ItemType}】暂时无法识别，请添加到分支结构中！')
    copy(citation)
    print(f'{count}【引文】{citation}（已复制到剪切板）')
    
# 【3】调用函数，得到结果（自动复制到剪切板）
if confirm(title='Citation',text=f'是否已更新【{path_in}】？',buttons=['是','否'])=='是':
    Library()
datals=Data()
input_title=prompt(title='Citation',text='请输入文献标题：')
count=1
while input_title !='': # 直接回车可结束运行
    result=[] # 以列表长度判断特殊情况：无此文献或存在重名
    for i in datals: # i是存储文献信息的字典，其索引已打印
        if i['Title']==input_title:
            result.append(i)
    if result==[]:
        print(f'【异常】检索“{input_title}”无结果！')
    elif len(result)>1:
        result_authors=[j['Author'] for j in result]
        result_check=confirm(title='Citation',text=f'检索【{input_title}】得到多个结果，请选择作者：',buttons=result_authors)
        for x in result:
            if x['Author']==result_check:
                print(f'{count}【文献】{data}')
                Citation()
                count+=1
    else:
        data=result[0]
        print(f'{count}【文献】{data}')
        Citation()
        count+=1
    input_title=prompt(title='Citation',text='请输入文献标题：')
else:
    print(f'程序正常退出，共检索有效文献{count-1}篇。')
