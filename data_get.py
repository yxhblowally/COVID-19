import requests
from lxml import etree #解析数据
import re
import json

#创建一个类
class Get_data():
    #获取数据
    def get_data(self):
        response = requests.get('https://voice.baidu.com/act/newpneumonia/newpneumonia#tab4')
        with open('html.txt','w') as file:
            file.write(response.text)

    #提取更新时间
    def get_time(self):
        with open('html.txt','r') as file:
            text = file.read()
        time = re.findall('mapLastUpdatedTime":"(.*?)"',text)[0]
        #print(time)
        return time

    #解析数据
    def parse_data(self):
        with open('html.txt','r') as file:
            text = file.read()
        html = etree.HTML(text)
        result = html.xpath('//script[@type="application/json"]/text()')
        result = result[0]
        result = json.loads(result)   #将字符串转化为字典
        result_in = result['component'][0]['caseList']
        result_in = json.dumps(result_in)   #将python得到数据类型转化为字符串
        # result_out = result['component'][0]['globalList']
        # result_out = json.dumps(result_out)
        with open('data_in.json','w') as file:
            file.write(result_in)
        # with open('data_out.json','w') as file:
        #     file.write(result_out)
        print('数据已写入json文件...')

data = Get_data()
data.get_data()
data.get_time()
data.parse_data()