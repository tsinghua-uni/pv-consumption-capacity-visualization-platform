from pyecharts import Map
import openpyxl

# Use openpyxl to read data from excel file
data = openpyxl.load_workbook('./data.xlsx')
table = data['Sheet1']
province = [cell.value for cell in table['A'][1:]]
num = [cell.value for cell in table['B'][1:]]

chinaMap = Map(width=2400, height=1200)
chinaMap.add(name="消纳能力",
# 1. Gradient color
            # attr=province,
            # value=num,
            # visual_range=[0, 239],
            # maptype='china',
            # is_visualmap=True)
# 2. 4 colors
# province
            attr=province,
            value=num,
            # If < 200 , color is red
            # If 200 < x < 400 , color is orange
            # If 400 < x < 600 , color is yellow
            # If x > 600 , color is green
            visual_range=[0, 600],
            visual_range_color=['#FF0000', '#FF7F00', '#FFFF00', '#00FF00'],
            maptype='china',
            is_visualmap=True,
            visual_text_color='#000')
chinaMap.render(path="中国地图.html")