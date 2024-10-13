import geopandas as gpd
from shapely.geometry import Point, Polygon, MultiPolygon
import shapely
import pandas as pd
from fiona.drvsupport import supported_drivers
import folium
import argparse
import json

parser = argparse.ArgumentParser(description='Process some points and map files.')
parser.add_argument('points_file', type=str, help='Path to the points CSV file')
parser.add_argument('map_file', type=str, help='Path to the KML map file')

args = parser.parse_args()

points_file = args.points_file
map_file = args.map_file

# read the points file
geo_locations = pd.read_csv(points_file, sep="\t")

# add points to the dataframe
geometric_points = []
for xy in zip(geo_locations['lng'], geo_locations['lat']):
    geometric_points.append(Point(xy))

# create a GeoDataFrame
geo_locations = gpd.GeoDataFrame(geo_locations,
                                 crs = {'init': 'epsg:4326'},
                                 geometry = geometric_points)

# read the map file
supported_drivers['KML'] = 'rw'
my_map = gpd.read_file(map_file, driver='KML')

# convert the map geometry to 2D
my_map.geometry = shapely.wkb.loads(
        shapely.wkb.dumps(my_map.geometry, output_dimension=2))

# run every point against every polygon of the map
df_out = gpd.sjoin(geo_locations, my_map, how='left', op='within')

# save the result to a CSV file
df_out.to_csv("result.csv", sep='\t', encoding='utf-8')

# create an area to plot
fig = folium.Map(width=1280, height=720)

# load the map in the geojson format
geo_json_map = json.load(open('ADA_SPGG_03092024.geojson'))
folium.Choropleth(
    geo_data = geo_json_map,
    fill_color = "steelblue",
    fill_opacity = 0.4,
    line_color = "steelblue",
    line_opacity = 0.9
).add_to(fig)

# add points to the map
for i in range(0, len(df_out)):
    lat = df_out['lat'].loc[i]
    lng = df_out['lng'].loc[i]
    check = not pd.isna(df_out['index_right'].loc[i])
    tooltip = df_out['tooltip'].loc[i]

    color = "green" if check else "red"
    folium.Marker((lat, lng), icon=folium.Icon(color=color), tooltip=tooltip).add_to(fig)

# save the map to a file
fig.save('map.html')
