import random
import schedule
import time
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.globals import ThemeType
from openpyxl import load_workbook
import os
from bs4 import BeautifulSoup

# Function to generate random data and update the excel file
def update_excel():
    data = load_workbook('data_cities-dynamic.xlsx')
    table = data.active
    for i in range(2, 3801):  # B2 to B3800
        table['B' + str(i)] = random.randint(100, 10000)  # generate random number between 1 and 10000
    data.save('data_cities-dynamic.xlsx')

# Function to generate map
def generate_map():
    # Read the Excel file
    df = pd.read_excel('data_cities-dynamic.xlsx')

    # Convert the DataFrame to a list of tuples
    data = list(df.itertuples(index=False, name=None))

    c = (
        Map(init_opts=opts.InitOpts(page_title="PV Consumption Capacity Visualization Platform",bg_color="#FFFAFA",width="1500px", height="1000px", theme=ThemeType.WONDERLAND))
        # Map(init_opts=opts.InitOpts(bg_color="#FFFAFA", theme=ThemeType.ESSOS))
        .add(
            "Consumption Capacity",
            data,
            "china-cities",
            label_opts=opts.LabelOpts(is_show=False),
            is_map_symbol_show=False,
            
        )
        # # 设置坐标属性，显示省份名
        # .set_series_opts(
        # label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="PV Consumption Capacity Visualization Platform", subtitle="City Version"),
            visualmap_opts=opts.VisualMapOpts(
                max_=10000,
                range_color=["#FF0000", "#FFA500", "#FFFF00", "#27cc7f", "#eeeeee"],
                is_piecewise=True,
                pos_top='50%',  # Adjust this value
                pos_left='5%',  # Adjust this value
                pieces=[
                    {"min": 1, "max": 2000, "color": "#FF0000", "label": "Low consumption capacity"},
                    {"min": 201, "max": 4000, "color": "#FFA500", "label": "Medium-low consumption capacity"},
                    {"min": 401, "max": 6000, "color": "#FFFF00", "label": "Medium-high consumption capacity"},
                    {"min": 601, "max": 10000, "color": "#27cc7f", "label": "High consumption capacity"},
                    # No data，grey
                    {"min": -1000, "max": 0, "color": "#eeeeee", "label": "No data"}
                ]
            ),
        )
        .render("map_china_cities_dynamic.html")
    )
def add_auto_reload():
    with open("map_china_cities_dynamic.html", "r+") as f:
        soup = BeautifulSoup(f, "html.parser")

        # Add script for auto-reload and manual refresh
        script = soup.new_tag("script")
        script.string = """
        var autoReload = setInterval(function() { window.location.reload(); }, 1000);

        function startAutoReload() {
            autoReload = setInterval(function() { window.location.reload(); }, 1000);
        }

        function stopAutoReload() {
            clearInterval(autoReload);
        }

        function refreshPage() {
            stopAutoReload();
            window.location.reload();
        }
        """
        soup.body.append(script)

        # Create a div container for the buttons
        button_container = soup.new_tag("div")
        button_container['style'] = "position: absolute; left: 0; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column;"

        # Add buttons for start auto-reload, stop auto-reload, and manual refresh
        start_button = soup.new_tag("button", onclick="startAutoReload()")
        start_button.string = "Start Auto Reload"
        start_button['style'] = "background-color: #4CAF50; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 2px 1px; cursor: pointer;"
        button_container.append(start_button)

        stop_button = soup.new_tag("button", onclick="stopAutoReload()")
        stop_button.string = "Stop Auto Reload"
        stop_button['style'] = "background-color: #f44336; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 2px 1px; cursor: pointer;"
        button_container.append(stop_button)

        refresh_button = soup.new_tag("button", onclick="refreshPage()")
        refresh_button.string = "Manual Refresh"
        refresh_button['style'] = "background-color: #008CBA; color: white; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 2px 1px; cursor: pointer;"
        button_container.append(refresh_button)

        # Add the button container to the body
        soup.body.append(button_container)

        # Write back to file
        f.seek(0)
        f.write(str(soup))
        f.truncate()
# Function to update excel and generate map
def job():
    update_excel()
    generate_map()
    add_auto_reload() 

# Schedule job every 5 second
schedule.every(0.5).seconds.do(job)

# Keep running the script
while True:
    schedule.run_pending()
    time.sleep(0.5)