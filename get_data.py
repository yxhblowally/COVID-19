import requests
from lxml import etree
import json
import openpyxl
url = "https://voice.baidu.com/act/newpneumonia/newpneumonia"
response = requests.get(url)
#print(response.text)
html = etree.HTML(response.text)   #生成HTML对象
result = html.xpath('//script[@type="application/json"]/text()')
#print(result[0])
result = result[0]
result = json.loads(result)   #json.loads()方法可以将字符串转化为python数据类型
#print(result)
wb = openpyxl.Workbook()   #创建工作簿
ws = wb.active   #在这个工作簿下创建工作表
ws.title = "国内疫情"
ws.append(['省份','累计确诊','死亡','治愈','现有确诊','累计确诊增量','死亡增量','治愈增量','现有确诊增量'])   #在工作表中添加数据
result_in = result['component'][0]['caseList']
result_out = result['component'][0]['globalList']
# print(result_out)
for each in result_in:
    #print(each)
    #print('*'*50+'\n')
   temp_list = [each['area'],each['confirmed'],each['died'],each['crued'],each['curConfirm'],each['confirmedRelative'],
              each['diedRelative'],each['curedRelative'],each['curConfirmRelative']]
    #为了防止出现空表格，将空表格赋值为“0”
   for i in range(len(temp_list)):
       if temp_list[i] == '':
           temp_list[i] = '0'
   ws.append(temp_list)
for each in result_out:
    sheet_title = each['area']
    ws_out = wb.create_sheet(sheet_title)   #创建新的工作表
    ws_out.append(['国家','累计确诊','死亡','治愈','现有确诊','累计确诊增量'])
    for country in each['subList']:
        temp_list = [country['country'],country['confirmed'],country['died'],country['crued'],country['curConfirm'],
                     country['confirmedRelative']]
        ws_out.append(temp_list)

wb.save('./data.xlsx')

'''
area -->省份/直辖市/特别行政区等
city -->城市
confirmed -->累计确诊人数
died -->死亡人数
crued -->治愈人数
confirmedRelative -->累计确诊的增量
curedRelative -->累计治愈的增量
curConfirmedRelative -->现有确诊的增量
curConfirm -->现有确诊人数
diedRelative -->死亡的增量
'''
