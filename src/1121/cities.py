import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.globals import ThemeType

# Read the Excel file
df = pd.read_excel('data_cities.xlsx')

# Convert the DataFrame to a list of tuples
data = list(df.itertuples(index=False, name=None))

c = (
    Map(init_opts=opts.InitOpts(width="2000px", height="1000px", theme=ThemeType.WHITE))

    .add(
        "消纳能力",
        data,
        "china-cities",
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Map-中国地图（带城市）"),
        visualmap_opts=opts.VisualMapOpts(),
    )
    .render("map_china_cities.html")
)