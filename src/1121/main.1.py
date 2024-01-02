import random
import schedule
import time
from pyecharts import Map
import openpyxl

# Function to generate random data and update the excel file
def update_excel():
    data = openpyxl.load_workbook('./data-dynamic.xlsx')
    table = data['Sheet1']
    for i in range(2, 36):  # B2 to B36
        table['B' + str(i)] = random.randint(1, 1000)  # generate random number between 1 and 1000
    data.save('./data-dynamic.xlsx')

# Function to generate map
def generate_map():
    # Use openpyxl to read data from excel file
    data = openpyxl.load_workbook('./data-dynamic.xlsx')
    table = data['Sheet1']
    province = [cell.value for cell in table['A'][1:]]
    num = [cell.value for cell in table['B'][1:]]

    chinaMap = Map(width=1200, height=600)
    chinaMap.add(name="消纳能力",
                attr=province,
                value=num,
                visual_range=[0, 600],
                visual_range_color=['#FF0000', '#FF7F00', '#FFFF00', '#00FF00'],
                maptype='china',
                is_visualmap=True,
                visual_text_color='#000')
    chinaMap.render(path="中国动态地图.html")

# Function to update excel and generate map
def job():
    update_excel()
    generate_map()

# Schedule job every 2 seconds
schedule.every(1).seconds.do(job)

# Keep running the script
while True:
    schedule.run_pending()
    # time.sleep(1)