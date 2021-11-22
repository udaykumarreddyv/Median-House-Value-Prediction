from map_tool import Map, remove_upper_lower, fix_zipcode_type
from zipcode_mapping import Zipcode_Mapping
import pathlib
import pandas as pd


def makeMap(lower, upper, mapName="HousingSeverity.html"):
    '''
    make a scenario that geographically maps information in LA county area
    value/sqft
    value/numBedrooms
    sqft/bedroomcount
    :return: folium map object
    '''
    print("Start Making Severity Map")
    # create map object and load in geojson data

    zm = Zipcode_Mapping()
    assert zm.load_mapping(), "mapping can't be loaded"
    severityMap = Map(zipcode_map_zipcodes=list(zm.zipcodes.values()))
    zillowHousing = pathlib.Path(r'./data/zillowHousing/clean_data_2016.csv')
    print("Loading dataset")
    zhData = pd.read_csv(zillowHousing)

    # fix the zillow zipcode mapping
    zhData['regionidzip'] = zhData['regionidzip'].astype('int')
    zhData['regionidzip'] = zhData['regionidzip'].map(zm.zipcodes)
    zhData = zhData[zhData['bedroomcnt'] != 0]

    print("calculating map data")
    # Calc price vs house size built
    zhData['priceVsHouseSize'] = zhData['taxvaluedollarcnt'] / zhData['calculatedfinishedsquarefeet']
    pVSF = remove_upper_lower(zhData, 'priceVsHouseSize', lower, upper)
    print("PVSF: ",len(pVSF))
    print("PVSF: ",pVSF['priceVsHouseSize'])
    # Calc prics vs squareft
    zhData['priceVsbedRoomCount'] = zhData['taxvaluedollarcnt'] / zhData['bedroomcnt']
    pVNB = remove_upper_lower(zhData, 'priceVsbedRoomCount', lower, upper)
    # calc squareft/bedrooms
    zhData['sizeOfHouseVsbedRoomCount'] = zhData['calculatedfinishedsquarefeet'] / zhData['bedroomcnt']
    sqVNB = remove_upper_lower(zhData, 'sizeOfHouseVsbedRoomCount', lower, upper)
    # generate data to map
    houseValueData = fix_zipcode_type(zhData[['regionidzip', 'taxvaluedollarcnt']], 'regionidzip')

    priceVsSize = fix_zipcode_type(zhData[['regionidzip', 'priceVsHouseSize']], 'regionidzip')
    normPriceVsSize = fix_zipcode_type(pVSF[['regionidzip', 'priceVsHouseSize']], 'regionidzip')

    priceVsBedrooms = fix_zipcode_type(zhData[['regionidzip', 'priceVsbedRoomCount']], 'regionidzip')
    normPriceVsBedrooms = fix_zipcode_type(pVNB[['regionidzip', 'priceVsbedRoomCount']], 'regionidzip')

    sizeVsBedrooms = fix_zipcode_type(zhData[['regionidzip', 'sizeOfHouseVsbedRoomCount']], 'regionidzip')
    normSizeVsBedrooms = fix_zipcode_type(sqVNB[['regionidzip', 'sizeOfHouseVsbedRoomCount']], 'regionidzip')

    print("Making map")
    m = severityMap.make_map([
        ["House Values", houseValueData, 'regionidzip', 'taxvaluedollarcnt', "House Values", "YlGn"],
        ["Value vs sq. ft", priceVsSize, 'regionidzip', 'priceVsHouseSize', "Value vs sq. ft", "RdPu"],
        ["Value vs sq. ft outliers removed", normPriceVsSize, 'regionidzip', 'priceVsHouseSize',
         "Value vs sq. ft outliers removed", "OrRd"],
        ["Value vs # Bedrooms", priceVsBedrooms, 'regionidzip', 'priceVsbedRoomCount', "Value vs # Bedrooms", 'PuBuGn'],
        ["Value vs # Bedrooms outliers removed", normPriceVsBedrooms, 'regionidzip', 'priceVsbedRoomCount',
         "Value vs # Bedrooms outliers removed", 'YlOrBr'],
        ["Sq. ft vs # Bedrooms", sizeVsBedrooms, 'regionidzip', 'sizeOfHouseVsbedRoomCount', 'Sq. ft vs # Bedrooms',
         'YlGnBu'],
        ["Sq. ft vs # Bedrooms outliers removed", normSizeVsBedrooms, 'regionidzip', 'sizeOfHouseVsbedRoomCount',
         'Sq. ft vs # Bedrooms outliers removed', 'BuGn'],

    ], mapName)
    print("finished")
    return m


if __name__ == "__main__":
    makeMap(lower=5,upper=95,mapName="HousingSeverity_5.html")
