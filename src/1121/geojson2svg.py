import geopandas as gpd
import matplotlib.pyplot as plt

geojson_file = './file.geojson'
gdf = gpd.read_file(geojson_file)

fig, ax = plt.subplots(figsize=(10, 10))
gdf.plot(ax=ax)

svg_file = './file.svg'
plt.savefig(svg_file, format='svg')
