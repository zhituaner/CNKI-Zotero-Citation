# `Customize Zotero Citation.py`

## 编写目的

Zotero可以在Word中非常方便地插入引文，这是基于styles文件夹下的`.csl`样式文件实现的。然而，引文样式多种多样，在某些情况下无法从网上找到相应的`.csl`文件，也缺乏修改已有`.csl`文件所需的知识储备。**故【基于Zotero导出的文献库】编写此程序，通过修改源码，我们可以自定义任意引文格式，从而更加灵活地实现随写随引。**

## 使用说明

1. 使用Python第三方库：**os**、**pandas**、**pyperclip**、**pyautogui**；
2. 建议使用前先确认无法找到所需`.csl`文件，像`GB/T 7714-2015`这样常用的格式还是可以找到的；
3. 导出Zotero文献库`我的文库.csv`，将其放在本文件夹内，或在源码中修改路径`path_in`；
4. 【**核心：自定义引文样式**】位于源码第二部分中的`Citation()`函数，**可在注释提示下修改为所需样式**；
5. 运行程序后将使用`pyautogui.prompt`接受输入（直接回车可退出程序），输入**文献标题**即可检索，并将生成的引文**自动复制到剪切板**。

## 版本更新

### v2.0（当前）

1. **封装函数**：各司其职，易于修改；
2. **优化检索**：（仍以标题检索）增加**查无结果**和**多个结果**时的处理机制，后者使用`pyautogui.confirm`弹窗供使用者选择文献作者；
3. **增加注释**：集中于程序核心的`Citation()`函数，便于在其提示下按需修改源码；
4. **优化输出**：主要为在打印引文前**增加打印存储文献信息的字典**；在程序运行初**增加打印可供检索该字典的键**。

# `CNKI to Zotero.py`

注：写完此程序后不久，我突然发现**Zotero6.0-beta的Zotero Connector已支持批量导出知网文献**。哎，就当是练手了qaq……（2022.2.18补充）

## 编写目的

**将所需:white_check_mark:知网文献自动化、批量导入Zotero。**（“所需”指检索结果页中，复选框处于勾选状态√的文献；目前尚未发现将知网文献批量导入Zotero的方法）

## 使用说明

1. 使用Python第三方库：**os**、**sys**、**selenium**【核心】、**pyautogui**；
2. **当前仅支持Chrome**；此处**不含selenium浏览器驱动**，请根据**浏览器版本**自行下载【[**Chrome**](http://chromedriver.storage.googleapis.com/index.html)；[**Firefox**](https://github.com/mozilla/geckodriver/releases/)；[**IE**](http://selenium-release.storage.googleapis.com/index.html)】，并将其放在**Python安装目录**下（或添加至**环境变量**）；
3. 其他具体事项，在运行中使用`pyautogui.confirm`**弹窗提示**；
4. 为使**Zotero Connector**完整识别文献信息，本程序在`SaveToZotero()`函数内使用较多`time.sleep`~~（事实上手动操作也得等啊）~~，以确保使用**“Save to Zotero(CNKI)”**选项导出（否则会导出网页）。对运行时间的优化主要集中于此。
5. 你需要做的**只是**打开Zotero、手动检索、勾选所需文献，程序将检测所选☑文献并自动导入Zotero。**在所需文献较多时尤为省事**。~~（可以挂着程序先去干饭嘛）~~
6. 经测试，**批量导出成功率接近100%**。少数异常情况下会导出为网页，尝试手动导出后基本上依然如此，推测问题应该不在程序。
