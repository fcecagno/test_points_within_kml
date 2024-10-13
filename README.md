This is a very simple project that implements a small routine in Python to check if a list of locations are within any polygon described in a KML file.

Setup venv:

```
mkdir venv
python3 -m venv venv/
source venv/bin/activate
pip3 install -r requirements.txt
```

Generate geojson map from KML:
```
k2g ADA_SPGG_03092024.kml -sf ADA_SPGG_03092024.geojson .
```

Run the application with (see `example.csv`):

```
python3 test_points_within_kml.py <csv file with points> <kml file>
```

The command will output a `result.csv` file, which is the original file with a new column `index_right`. If it's empty or NaN, it means the point is not within any polygon. If it's an integer number, it means there was a match and point is within one of the polygons described in the KML file.
Also it will output a map with the KML areas and the points.
