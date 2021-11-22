from map_tool import Map, remove_upper_lower, fix_zipcode_type
from zipcode_mapping import Zipcode_Mapping
import pathlib
import pandas as pd
import numpy as np


def makeMap(lower=1, upper=99, mapName="House_Values.html"):
    print("Making map")

    zm = Zipcode_Mapping()
    assert zm.load_mapping(), "mapping can't be loaded"
    basicMap = Map(zipcode_map_zipcodes=list(zm.zipcodes.values()))
    print("loading dataset")
    zillowHousing = pathlib.Path(r'./data/zillowHousing/clean_data_2016.csv')
    zhData = pd.read_csv(zillowHousing)
    zhData['regionidzip'] = zhData['regionidzip'].astype('int')
    zhData['regionidzip'] = zhData['regionidzip'].map(zm.zipcodes)
    normMap = remove_upper_lower(zhData, 'taxvaluedollarcnt', lower, upper)
    print("calculating map data")

    mapData = zhData[['regionidzip', 'taxvaluedollarcnt']].dropna().groupby(by='regionidzip').mean().reset_index()
    mapData = pd.DataFrame(mapData)
    mapData['regionidzip'] = mapData['regionidzip'].astype('int')
    normMapData = normMap[['regionidzip', 'taxvaluedollarcnt']].dropna().groupby(by='regionidzip').mean().reset_index()
    normMapData = pd.DataFrame(normMapData)
    normMapData['regionidzip'] = normMapData['regionidzip'].astype('int')
    print("making map")
    m = basicMap.make_map([
        ["House values", mapData, 'regionidzip', 'taxvaluedollarcnt', "House Values", "YlGn"],
        ["House values outliers removed", normMapData, 'regionidzip', 'taxvaluedollarcnt',
         "House values outliers removed", "RdPu"]
    ], mapName)
    print("finished")
    return m

if __name__ == "__main__":
    #makeMap(1, 99, "House_Values_1.html")
    makeMap(5, 95, "House_Values_5.html")
    #makeMap(10, 90, "House_Values_10.html")
