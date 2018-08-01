from collections import Counter
from os import path
import pandas as pd
from pyecharts import Geo, Line, Bar, Overlap
import jieba
from scipy.misc import imread
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt


# 获取当前文件路径
# __file__ 为当前文件, 在ide中运行此行会报错,可改为
# d = path.dirname('.')
d = path.dirname(__file__)

tomato_com = pd.read_csv('tomato.csv')
grouped = tomato_com.groupby(['city'])
grouped_pct=grouped['score'] #tip_pct列
city_com = grouped_pct.agg(['mean','count'])
city_com.reset_index(inplace=True)
city_com['mean'] = round(city_com['mean'],2)

# 热力图
data=[(city_com['city'][i],city_com['count'][i]) for i in range(0,
      city_com.shape[0])]
geo = Geo('《西虹市首富》全国热力图', title_color="#fff",
         title_pos="center", width=1200,
         height=600, background_color='#404a59')
while True:
    try:
        attr, value = geo.cast(data)
        geo.add("", attr, value, type="heatmap", visual_range=[0, 200], visual_text_color="#fff", is_visualmap=True)
        geo.render('西虹市首富全国热力图.html')
        break
    except ValueError as e:
        e = str(e)
        e = e.split("No coordinate is specified for ")[1]
        i = attr.index(e)
        v = value[i]
        node = (e, v)
        data.remove(node)
        print("{0} is removed.".format(node))

# 折线图+柱形图组合
city_main = city_com.sort_values('count',ascending=False)[0:20]
attr = city_main['city']
v1=city_main['count']
v2=city_main['mean']
line = Line("主要城市评分")
line.add("城市", attr, v2, is_stack=True,xaxis_rotate=30,yaxis_min=4.2,
        mark_point=['min','max'],xaxis_interval =0,line_color='lightblue',
        line_width=4,mark_point_textcolor='black',mark_point_color='lightblue',
        is_splitline_show=False)
bar = Bar("主要城市评论数")
bar.add("城市", attr, v1, is_stack=True,xaxis_rotate=30,yaxis_min=4.2,
        xaxis_interval =0,is_splitline_show=False)
overlap = Overlap()
# 默认不新增 x y 轴，并且 x y 轴的索引都为 0
overlap.add(bar)
overlap.add(line, yaxis_index=1, is_add_yaxis=True)
overlap.render('主要城市评论数_平均分.html')


# 词云
tomato_str =  ' '.join(tomato_com['comment'])
words_list = []
word_generator = jieba.cut_for_search(tomato_str)
for word in word_generator:
   words_list.append(word)
words_list = [k for k in words_list if len(k)>1]
back_color = imread('tomato.jpg')  # 解析该图片
wc = WordCloud(background_color='white',  # 背景颜色
              max_words=200,  # 最大词数
              mask=back_color,  # 以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
              max_font_size=300,  # 显示字体的最大值
              stopwords=STOPWORDS.add('苟利国'),  # 使用内置的屏蔽词，再添加'苟利国'
              font_path="C:/Windows/Fonts/STFANGSO.ttf",
              random_state=42,  # 为每个词返回一个PIL颜色
              # width=1000,  # 图片的宽
              # height=860  #图片的长
              )
tomato_count = Counter(words_list)
wc.generate_from_frequencies(tomato_count)
# 基于彩色图像生成相应彩色
image_colors = ImageColorGenerator(back_color)
# 绘制词云
plt.figure()
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis('off')
wc.to_file(path.join(d, "词云.png"))
