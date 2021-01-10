import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.charts import Line
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from pyecharts.charts import Bar3D
from pyecharts.charts import Geo
from pyecharts.globals import ChartType

# 负责数据的读取和整理
def read_do():
    init_data = pd.read_excel(r"F:\COVID-19\data.xlsx")   #读取指定路径的表格
    init_data = np.array(init_data)   #用numpy定义数组
    data_tip = ['累计确诊', '死亡', '治愈', '现有确诊', '累计确诊增量', '死亡增量', '治愈增量', '现有确诊增量']
    data_area = ['西藏', '澳门', '青海', '台湾', '香港', '贵州', '吉林', '新疆', '宁夏', '内蒙古', '甘肃', '天津', '山西', '辽宁', '黑龙江', '海南',
                 '河北', '陕西', '云南', '广西', '福建', '上海', '北京', '江苏', '四川', '山东', '江西', '重庆', '安徽', '湖南', '河南', '广东',
                 '浙江', '湖北']
    data_pre = []
    column = 1
    for index in data_tip:
        row = 0
        for area in data_area:
            info = [index, area, init_data[row][column]]   #将数据写进列表
            data_pre.append(info)
            row = row + 1
        column = column + 1
    return data_pre
    # print(data_pre)
data = read_do()

class Draw_map():
    def get_color(a, b, c):
        result = '#' + ''.join(map((lambda x: "%02x" % x), (a, b, c)))
        return result.upper()
    # 绘制中国疫情图表
    def to_map_china(self,area,variate,value,update_time):
        # 显示标识栏的颜色分段表示
        pieces = [
            {"max":99999999,"min":10000,"label":'>10000',"color":'#E64546'},
            {"max": 9999, "min": 1000, "label": '1000-9999', "color": '#F57567'},
            {"max": 999, "min": 100, "label": '100-999', "color": '#FF9985'},
            {"max": 99, "min": 10, "label": '10-99', "color": '#FFC4B3'},
            {"max": 9, "min": 1, "label": '1-9', "color": '#FFE5DB'},
            {"max": 0, "min": 0, "label": '0', "color": '#FFFFFF'},
        ]
        data_tip = ['累计确诊', '死亡', '治愈', '现有确诊', '累计确诊增量', '死亡增量', '治愈增量', '现有确诊增量']
        data_area = ['西藏', '澳门', '青海', '台湾', '香港', '贵州', '吉林', '新疆', '宁夏', '内蒙古', '甘肃', '天津', '山西', '辽宁', '黑龙江', '海南',
                     '河北', '陕西', '云南', '广西', '福建', '上海', '北京', '江苏', '四川', '山东', '江西', '重庆', '安徽', '湖南', '河南', '广东',
                     '浙江', '湖北']
        # 绘制地图
        map = (
            Map(init_opts=opts.InitOpts(width='800px', height='600px'))  # 初始化配置项，设置地图大小
                .add("累计确诊人数", [list(z) for z in zip(area, variate)], "china")
                .set_global_opts(
                title_opts=opts.TitleOpts(title="中国疫情地图分布", subtitle='截止%s 中国疫情分布情况' % (update_time),
                                          pos_left='center', pos_top='30px'),   #TitleOpts：标题设置
                visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True, pieces=pieces),
                # # max_：设置 visualMapPiecewise 所有取值区间中的最大值，is_piecewise设置数据是否连续，split_number设置为分段数，pices可自定义数据分段
            )
                .render("中国疫情地图.html")   # 展示提取后的效果
        )
        # 绘制地理坐标图
        geo = (
            Geo()
                .add_schema(maptype="china")   #地图类型
                .add(
                "累计确诊人数",
                [list(z) for z in zip(area, variate)],
                type_=ChartType.EFFECT_SCATTER,
            )
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))   # label_opts:标签配置项设置，is_show：是否显示视觉映射配置
                .set_global_opts(title_opts=opts.TitleOpts(title="中国疫情地图分布",subtitle='截止%s 中国疫情分布情况'%(update_time),
                                                           pos_left='center',pos_top='30px'),
                visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True, pieces=pieces),
                                 )
                .render("中国疫情新增情况.html")
        )
        # 绘制折线图
        line = (
            Line()
                .add_xaxis(area)   #添加x轴数值
                .add_yaxis("累计确诊人数",variate)   #添加y轴名称、数值
                .add_yaxis("累计治愈人数",value)
                .set_global_opts(title_opts=opts.TitleOpts(title="国内疫情情况"),
                                 xaxis_opts=opts.AxisOpts(axislabel_opts={"interval": "0", "rotate": "45"}),   #设置x轴数值分割间隔为0，且旋转45°
                                 yaxis_opts=opts.AxisOpts(type_='log', splitline_opts=opts.SplitLineOpts(is_show=True),
                                                          is_scale=True,)   #设置y轴数据类型为“log”，凸显分割线，不会强制包含零刻度
                                 )
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  #标签设置项
                .render("全国累计趋势折线图.html")
        )
        # 绘制柱状图
        bar = (
            Bar()
                .add_xaxis(area)
                .add_yaxis("累计确诊人数",variate,stack='stack1')   #若y轴设置项“stack”为同一个值，则显示为堆叠型柱状，反之，成分散型
                # .add_yaxis("累计治愈人数",value,stack='stack2')
                # .add_yaxis("累计死亡人数", value, stack='stack1')
                .add_yaxis("累计治愈人数", value, stack='stack1')
                .set_global_opts(title_opts=opts.TitleOpts(title="全国累计确诊治愈情况"),
                                 xaxis_opts=opts.AxisOpts(axislabel_opts={"interval":"0","rotate":"45"}),
                                 yaxis_opts=opts.AxisOpts(type_='log',splitline_opts=opts.SplitLineOpts(is_show=True),
                                                          is_scale=True,))
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .render("全国累计确诊治愈.html")
        )
        # 绘制饼状图
        pie = (
            Pie()
                .add(
                "",
                [list(z) for z in zip(area,variate)],
                radius=["40%", "75%","log"],   #设置圆环大小及数据类型
            )
                .set_global_opts(
                title_opts=opts.TitleOpts(title="国内疫情情况"),
                legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
                #图例配置项：图例列表的布局朝向为水平，图例组件离容器上侧的距离为15%，图例组件离容器左侧的距离为相对于容器高宽的20%
            )
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))   #设置标签形式
                .render("全国累计趋势饼状图.html")
        )
        # 绘制3D柱状图
        bar3d = (
            Bar3D()
                .add(
                "全国指标",
                data,
                label_opts=opts.LabelOpts(position='left'),
                yaxis3d_opts=opts.Axis3DOpts(data_area),
                xaxis3d_opts=opts.Axis3DOpts(data_tip, type_="category", max_=8, interval=0,),

                zaxis3d_opts=opts.Axis3DOpts(type_="value", min_=0),
                grid3d_opts=opts.Grid3DOpts(width="600", height="100",is_rotate=True)
                #设置三维笛卡尔坐标系组件在三维场景中的宽度，高度，以及是否自动旋转
            )
                .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(is_piecewise=True,pieces=pieces),
                title_opts=opts.TitleOpts(title="疫情指标"),
            )
                .render("疫情指标.html")
        )
    # 绘制中国各省份疫情地图
    def to_map_city(self,city, variate, province, update_time):
        pieces = [
            {"max": 99999999, "min": 10000, "label": "≥10000", "color": '#660208'},
            {"max": 9999, "min": 1000, "label": "1000-9999", "color":'#8C0D0D'},
            {"max": 999, "min": 500, "label": "500-999", "color":'#CC2929'},
            {"max": 499, "min": 100, "label": "100-499", "color":'#FF7B69'},
            {"max": 99, "min": 50, "label": "50-99", "color":'#FFAA85'},
            {"max": 49, "min": 10, "label": "10-49", "color":'#FFCAB3'},
            {"max": 9, "min": 1, "label": "1-9", "color":'#FFE4D9'},
            {"max": 0, "min": 0, "label": "0", "color": '#FFFFFF'},
        ]
        map = (
            Map(init_opts=opts.InitOpts(width='1000px', height='880px'))
                .add("累计确诊人数", [list(z) for z in zip(city, variate)], province)
                .set_global_opts(
                title_opts=opts.TitleOpts(title="%s地区疫情地图分布" % (province),
                                          subtitle='截止%s  %s省疫情分布情况' % (update_time, province), pos_left="center",
                                          pos_top="10px"),
                legend_opts=opts.LegendOpts(is_show=False),
                visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True,pieces=pieces,),
            )
                .render("./{}疫情地图.html".format(province))
        )
        # print(province)
        # print(city)
        # print(variate)

# read_do()
