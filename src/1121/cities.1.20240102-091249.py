from flask import Flask, render_template, request
import threading
import random
import schedule
import time
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.globals import ThemeType
from openpyxl import load_workbook

app = Flask(__name__)

# Flag to control the job execution
job_running = False

# Job thread
job_thread = None

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
        Map(init_opts=opts.InitOpts(width="1200px", height="600px", theme=ThemeType.WHITE))
        .add(
            "消纳能力",
            data,
            "china-cities",
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-中国地图（带城市）"),
            visualmap_opts=opts.VisualMapOpts(
                max_=10000,
                range_color=["#FF0000", "#FFA500", "#FFFF00", "#008000"],
                is_piecewise=True,
                pieces=[
                    {"min": 1, "max": 2000, "color": "#FF0000"},
                    {"min": 201, "max": 4000, "color": "#FFA500"},
                    {"min": 401, "max": 6000, "color": "#FFFF00"},
                    {"min": 601, "max": 10000, "color": "#008000"}
                ]
            ),
        )
        .render("templates/map_china_cities_dynamic.html")
    )

# Function to update excel and generate map
def job():
    while job_running:
        update_excel()
        generate_map()
        time.sleep(1)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global job_running, job_thread
    if not job_running:
        job_running = True
        job_thread = threading.Thread(target=job)
        job_thread.start()
    return 'Job started'

@app.route('/stop', methods=['POST'])
def stop():
    global job_running
    if job_running:
        job_running = False
        job_thread.join()
    return 'Job stopped'

if __name__ == '__main__':
    app.run(debug=True)