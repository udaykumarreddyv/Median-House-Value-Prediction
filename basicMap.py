from map_tool import Map
from zipcode_mapping import Zipcode_Mapping
import pathlib
import pandas as pd
import values

if __name__ == "__main__":
    basicMap = Map()
    zm = Zipcode_Mapping()
    assert zm.load_mapping(), "mapping can't be loaded"
    zillowHousing = pathlib.Path(r'./data/zillowHousing/clean_data_2016.csv')
    zhData = pd.read_csv(zillowHousing)
    
    #Creation of heat Map values csvs to use further
    HeatValues=values.Heatmap_Values()
    HeatValues.price_vs_sizeOfHouse(zhData)
    HeatValues.price_vs_yearBuilt(zhData)
    HeatValues.price_vs_bedRoomCount(zhData)
    HeatValues.sizeOfHouse_vs_bedRoomCount(zhData)

    
    zhData['regionidzip'] = zhData['regionidzip'].astype('int')
    zhData['regionidzip'] = zhData['regionidzip'].map(zm.zipcodes)
    #normalize data
    zhData['taxvaluedollarcnt'] = ((zhData['taxvaluedollarcnt']-zhData['taxvaluedollarcnt'].min())/
                                   (zhData['taxvaluedollarcnt'].max()-zhData['taxvaluedollarcnt'].min()))
    # zhData[['regionidzip','taxvaluedollarcnt']]
    mapData = zhData[['regionidzip', 'taxvaluedollarcnt']].dropna().groupby(by='regionidzip').mean().reset_index()
    mapData = pd.DataFrame(mapData)
    mapData['regionidzip'] = mapData['regionidzip'].astype('int')

    ############################price vs house size##########################################
    zillowHousing1 = pathlib.Path(r'./data/zillowHousing/pricevssizeofHouse.csv')
    zhData1 = pd.read_csv(zillowHousing1)
    zhData1['regionidzip'] = zhData1['regionidzip'].astype('int')
    zhData1['regionidzip'] = zhData1['regionidzip'].map(zm.zipcodes)
    #normalize data
    zhData1['priceVsHouseSize'] = ((zhData1['priceVsHouseSize']-zhData1['priceVsHouseSize'].min())/
                                 (zhData1['priceVsHouseSize'].max()-zhData1['priceVsHouseSize'].min()))
    #zhData1[['regionidzip','priceVsHouseSize']]

    mapData1 = zhData1[['regionidzip', 'priceVsHouseSize']].dropna().groupby(by='regionidzip').mean().reset_index()
    mapData1 = pd.DataFrame(mapData1)
    mapData1['regionidzip'] = mapData1['regionidzip'].astype('int')

    ###########################price vs Year Built##############################################
    zillowHousing2 = pathlib.Path(r'./data/zillowHousing/pricevsYearBuilt.csv')
    zhData2 = pd.read_csv(zillowHousing2)
    zhData2['regionidzip'] = zhData2['regionidzip'].astype('int')
    zhData2['regionidzip'] = zhData2['regionidzip'].map(zm.zipcodes)
    #normalize data
    zhData2['priceVsYearBuilt'] = ((zhData2['priceVsYearBuilt']-zhData2['priceVsYearBuilt'].min())/
                                 (zhData2['priceVsYearBuilt'].max()-zhData2['priceVsYearBuilt'].min()))
   

    mapData2 = zhData2[['regionidzip', 'priceVsYearBuilt']].dropna().groupby(by='regionidzip').mean().reset_index()
    mapData2 = pd.DataFrame(mapData2)
    mapData2['regionidzip'] = mapData2['regionidzip'].astype('int')

    ###########################price vs Year Built##############################################
    zillowHousing2 = pathlib.Path(r'./data/zillowHousing/pricevsbedroomcount.csv')
    zhData2 = pd.read_csv(zillowHousing2)
    zhData2['regionidzip'] = zhData2['regionidzip'].astype('int')
    zhData2['regionidzip'] = zhData2['regionidzip'].map(zm.zipcodes)
    #normalize data
    zhData2['priceVsbedRoomCount'] = ((zhData2['priceVsbedRoomCount']-zhData2['priceVsbedRoomCount'].min())/
                                 (zhData2['priceVsbedRoomCount'].max()-zhData2['priceVsbedRoomCount'].min()))
   

    mapData3 = zhData2[['regionidzip', 'priceVsbedRoomCount']].dropna().groupby(by='regionidzip').mean().reset_index()
    mapData3 = pd.DataFrame(mapData3)
    mapData3['regionidzip'] = mapData3['regionidzip'].astype('int')

    ###########################sizeofhouse vs bedroomcount##############################################
    zillowHousing2 = pathlib.Path(r'./data/zillowHousing/sizeofhousevsbedroomcount.csv')
    zhData2 = pd.read_csv(zillowHousing2)
    zhData2['regionidzip'] = zhData2['regionidzip'].astype('int')
    zhData2['regionidzip'] = zhData2['regionidzip'].map(zm.zipcodes)
    #normalize data
    zhData2['sizeOfHouseVsbedRoomCount'] = ((zhData2['sizeOfHouseVsbedRoomCount']-zhData2['sizeOfHouseVsbedRoomCount'].min())/
                                 (zhData2['sizeOfHouseVsbedRoomCount'].max()-zhData2['sizeOfHouseVsbedRoomCount'].min()))
   

    mapData4 = zhData2[['regionidzip', 'sizeOfHouseVsbedRoomCount']].dropna().groupby(by='regionidzip').mean().reset_index()
    mapData4 = pd.DataFrame(mapData4)
    mapData4['regionidzip'] = mapData4['regionidzip'].astype('int')


##############################3     Map Creation #############################################
    basicMap.make_map([["housevalues", mapData, 'regionidzip', 'taxvaluedollarcnt',"housevalues","YlGn"],
                       ["sizeofhouse", mapData1, 'regionidzip', 'priceVsHouseSize',"sizeofhousevsprice","RdPu"],
                       ["priceVsYearBuilt", mapData2, 'regionidzip', 'priceVsYearBuilt',"priceVsYearBuilt","OrRd"],
                       ["priceVsbedRoomCount", mapData3, 'regionidzip', 'priceVsbedRoomCount',"priceVsbedRoomCount","PuBuGn"],
                       ["sizeOfHouseVsbedRoomCount", mapData4, 'regionidzip', 'sizeOfHouseVsbedRoomCount',"sizeOfHouseVsbedRoomCount","YlOrBr"]], "House_Values.html")
    