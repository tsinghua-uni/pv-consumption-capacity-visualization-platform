from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk
import random
import schedule
import time
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.globals import ThemeType
from openpyxl import load_workbook
import webbrowser

# Global flag to control the updating and generation
running = True

# Function to generate random data and update the excel file
def update_excel():
    if running:
        data = load_workbook('data_cities-dynamic.xlsx')
        table = data.active
        for i in range(2, 3801):  # B2 to B3800
            table['B' + str(i)] = random.randint(100, 10000)  # generate random number between 1 and 10000
        data.save('data_cities-dynamic.xlsx')

# Function to generate map
def generate_map():
    if running:
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
                title_opts=opts.TitleOpts(title="光伏消纳能力可视化平台（城市版）"),
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
            .render("map_china_cities_dynamic.html")
        )

# Function to start the updating and generation
def start():
    global running
    running = True
    webbrowser.open('map_china_cities_dynamic.html')

# Function to stop the updating and generation
def stop():
    global running
    running = False

# Function to resume the updating and generation
def resume():
    global running
    running = True

# Create a new ThemedTk window
window = ThemedTk(theme="arc")
window.title("Visualization system")

# Set the window size
window.geometry('800x600')

# Create a style
style = ttk.Style(window)
style.configure('TButton', font=('Arial', 20), borderwidth='4')

# Create a button for starting the updating and generation
btn_start = ttk.Button(window, text="Start", command=start)
btn_start.pack(pady=20)

# Create a button for stopping the updating and generation
btn_stop = ttk.Button(window, text="Stop", command=stop)
btn_stop.pack(pady=20)

# Create a button for resuming the updating and generation
btn_resume = ttk.Button(window, text="Resume", command=resume)
btn_resume.pack(pady=20)

# Run the Tkinter event loop
window.mainloop()