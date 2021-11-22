from map_tool import Map, remove_upper_lower, fix_zipcode_type
from zipcode_mapping import Zipcode_Mapping
import pathlib
import pandas as pd
import values


def makeMap(lower=1,upper=99, mapName="BedroomCount.html"):
    print("Making map")
    zm = Zipcode_Mapping()
    assert zm.load_mapping(), "mapping can't be loaded"
    bedroomMap = Map(zipcode_map_zipcodes=list(zm.zipcodes.values()))
    print("loading dataset")
    zillowHousing = pathlib.Path(r'./datastories_table.csv')
    zhData = pd.read_csv(zillowHousing)
    zhData['regionidzip'] = zhData['regionidzip'].astype('int')
    zhData['regionidzip'] = zhData['regionidzip'].map(zm.zipcodes)
    print("calculating map values")
    oneBed = zhData[zhData['bedroomcnt'] == 1]
    normOneBed = remove_upper_lower(oneBed,'taxvaluedollarcnt',lower,upper)
    twoBed = zhData[zhData['bedroomcnt'] == 2]
    normTwoBed = remove_upper_lower(twoBed, 'taxvaluedollarcnt', lower, upper)
    threeBed = zhData[zhData['bedroomcnt'] == 3]
    normThreeBed = remove_upper_lower(threeBed, 'taxvaluedollarcnt', lower, upper)
    oneBedRoomData = fix_zipcode_type(oneBed[['regionidzip', 'taxvaluedollarcnt']], 'regionidzip')
    twoBedRoomData = fix_zipcode_type(twoBed[['regionidzip', 'taxvaluedollarcnt']], 'regionidzip')
    threeBedRoomData = fix_zipcode_type(threeBed[['regionidzip', 'taxvaluedollarcnt']], 'regionidzip')
    normOneBedRoomData = fix_zipcode_type(normOneBed[['regionidzip', 'taxvaluedollarcnt']], 'regionidzip')
    normTwoBedRoomData = fix_zipcode_type(normTwoBed[['regionidzip', 'taxvaluedollarcnt']], 'regionidzip')
    normThreeBedRoomData = fix_zipcode_type(normThreeBed[['regionidzip', 'taxvaluedollarcnt']], 'regionidzip')
    print("making map")
    m = bedroomMap.make_map([
        ["College Student", twoBedRoomData, 'regionidzip', 'taxvaluedollarcnt', "College Student", "YlGn"],
        ["College Student restricted outliers", normOneBedRoomData, 'regionidzip', 'taxvaluedollarcnt', "College Student restricted outliers", "RdPu"],
        ["Working Professional", oneBedRoomData, 'regionidzip', 'taxvaluedollarcnt', "Working Professional", "OrRd"],
        ["Working Professional restricted outliers", normTwoBedRoomData, 'regionidzip', 'taxvaluedollarcnt', "Working Professional restricted outliers", "PuBuGn"],
        ["Nuclear Family", threeBedRoomData, 'regionidzip', 'taxvaluedollarcnt', "Nuclear Family", "YlOrBr"],
        ["Nuclear Family restricted outliers", normThreeBedRoomData, 'regionidzip', 'taxvaluedollarcnt', "Nuclear Family restricted outliers", "YlGnBu"],
    ], mapName)
    print("finished")
    return m


if __name__ == "__main__":
    makeMap(lower=5,upper=95,mapName="BedroomCount_5.html")
