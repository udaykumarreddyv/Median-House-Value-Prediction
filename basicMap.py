from map_tool import Map
from zipcode_mapping import Zipcode_Mapping
import pathlib
import pandas as pd

if __name__ == "__main__":
    basicMap = Map()
    zm = Zipcode_Mapping()
    assert zm.load_mapping(), "mapping can't be loaded"
    zillowHousing = pathlib.Path(r'./data/zillowHousing/clean_data_2016.csv')
    zhData = pd.read_csv(zillowHousing)
    zhData['regionidzip'] = zhData['regionidzip'].astype('int')
    zhData['regionidzip'] = zhData['regionidzip'].map(zm.zipcodes)
    #normalize data
    zhData['taxvaluedollarcnt'] = ((zhData['taxvaluedollarcnt']-zhData['taxvaluedollarcnt'].min())/
                                   (zhData['taxvaluedollarcnt'].max()-zhData['taxvaluedollarcnt'].min()))
    # zhData[['regionidzip','taxvaluedollarcnt']]
    mapData = zhData[['regionidzip', 'taxvaluedollarcnt']].dropna().groupby(by='regionidzip').mean().reset_index()
    mapData = pd.DataFrame(mapData)
    mapData['regionidzip'] = mapData['regionidzip'].astype('int')
    basicMap.make_map([["house values", mapData, 'regionidzip', 'taxvaluedollarcnt']], "House_Values.html")
