import json
import map_draw
import data_get

with open('data_in.json','r') as file:
    data_in = file.read()
    data_in = json.loads(data_in)   #将字符串类型转化为python数据类型（dict）
# 调用map_draw模块的Draw_map类
map = map_draw.Draw_map()
datas = data_get.Get_data()
datas.get_data()
update_time = datas.get_time()
datas.parse_data()
#中国疫情地图数据
def china_map():
    area = []
    confirmed = []
    crue = []
    curConfirm = []
    died = []
    for each in data_in:
        #print(each)
        #print('*'*50+'\n')
        area.append(each['area'])
        confirmed.append(each['confirmed'])
        crue.append(each['crued'])
        curConfirm.append(each['curConfirm'])
        died.append(each['died'])
    # print(area)
    # print(confirmed)
    map.to_map_china(area,confirmed,crue,update_time)

#省份疫情地图数据
def province_map():
    for each in data_in:
        city = []
        confirmeds = []
        province = each['area']
        for each_city in each['subList']:
            city.append(each_city['city']+"市")
            confirmeds.append(each_city['confirmed'])
            map.to_map_city(city,confirmeds,province,update_time)
        if province == '上海' or '北京' or '天津' or '重庆' or '香港':
            for each_city in each['subList']:
                city.append(each_city['city'])
                confirmeds.append(each_city['confirmed'])
                map.to_map_city(city,confirmeds,province,update_time)

china_map()
# province_map()
