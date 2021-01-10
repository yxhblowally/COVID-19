import openpyxl  #对EXCEL表格的数据进行提取
from wordcloud import WordCloud  #绘制词云

wb = openpyxl.load_workbook('data.xlsx')   #读取数据
ws = wb['国内疫情']   #获取工作表
freequency_in = {}  #创建一个字典
for row in ws.values:
    #print(row)   #打印工作表中的每一个值
    if row[0] == '省份':
        pass
    else:
        freequency_in[row[0]] = float(row[1])

#print(freequency_in)
# wordcloud = WordCloud(font_path="C:\Windows\Fonts\STXINGKA.TTF",background_color="white",width=1920,
#                       height=1080)  #字体文件路径的填写,指定背景颜色,生成图片的宽度、高度
# wordcloud.generate_from_frequencies(freequency_in)   #根据确诊病例的数目生成词云
# wordcloud.to_file('wordcloud.png')   #保存词云

freequency_out = {}
sheet_name = wb.sheetnames
for each in sheet_name:
    if "洲" in each:
        ws = wb[each]
        for row in ws.values:
            if row[0] == '国家':
                pass
            else:
                freequency_out[row[0]]= float(row[1])
#print(freequency_out)

#定义一个函数
def generate_pic(freequency,name):
    wordcloud = WordCloud(font_path="C:\Windows\Fonts\STXINGKA.TTF",background_color="white",width=1920,
                          height=1080)  #字体文件路径的填写,指定背景颜色,生成图片的宽度、高度
    wordcloud.generate_from_frequencies(freequency)   #根据确诊病例的数目生成词云
    wordcloud.to_file('%s.png'%(name))       #保存词云

print('词云图正在更新...')
generate_pic(freequency_in,'国内疫情词云图')
generate_pic(freequency_out,'世界疫情词云图')