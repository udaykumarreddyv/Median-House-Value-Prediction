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

  
    #normalize data
    zhData['priceVsHouseSize'] = ((zhData['priceVsHouseSize']-zhData['priceVsHouseSize'].min())/
                                 (zhData['priceVsHouseSize'].max()-zhData['priceVsHouseSize'].min()))
    #zhData1[['regionidzip','priceVsHouseSize']]

    mapData1 = zhData[['regionidzip', 'priceVsHouseSize']].dropna().groupby(by='regionidzip').mean().reset_index()
    mapData1 = pd.DataFrame(mapData1)
    mapData1['regionidzip'] = mapData1['regionidzip'].astype('int')

    ###########################price vs Year Built##############################################
   
    

    #normalize data
    zhData['priceVsYearBuilt'] = ((zhData['priceVsYearBuilt']-zhData['priceVsYearBuilt'].min())/
                                 (zhData['priceVsYearBuilt'].max()-zhData['priceVsYearBuilt'].min()))
   

    mapData2 = zhData[['regionidzip', 'priceVsYearBuilt']].dropna().groupby(by='regionidzip').mean().reset_index()
    mapData2 = pd.DataFrame(mapData2)
    mapData2['regionidzip'] = mapData2['regionidzip'].astype('int')

    ###########################price vs Year Built##############################################
    #zhData['regionidzip'] = zhData['regionidzip'].astype('int')
    #zhData['regionidzip'] = zhData['regionidzip'].map(zm.zipcodes)
    #normalize data
    zhData['priceVsbedRoomCount'] = ((zhData['priceVsbedRoomCount']-zhData['priceVsbedRoomCount'].min())/
                                 (zhData['priceVsbedRoomCount'].max()-zhData['priceVsbedRoomCount'].min()))
   

    mapData3 = zhData[['regionidzip', 'priceVsbedRoomCount']].dropna().groupby(by='regionidzip').mean().reset_index()
    mapData3 = pd.DataFrame(mapData3)
    mapData3['regionidzip'] = mapData3['regionidzip'].astype('int')

    ###########################sizeofhouse vs bedroomcount##############################################

    #zhData['regionidzip'] = zhData['regionidzip'].astype('int')
    #zhData['regionidzip'] = zhData['regionidzip'].map(zm.zipcodes)
    #normalize data
    zhData['sizeOfHouseVsbedRoomCount'] = ((zhData['sizeOfHouseVsbedRoomCount']-zhData['sizeOfHouseVsbedRoomCount'].min())/
                                 (zhData['sizeOfHouseVsbedRoomCount'].max()-zhData['sizeOfHouseVsbedRoomCount'].min()))
   
    mapData4 = zhData[['regionidzip', 'sizeOfHouseVsbedRoomCount']].dropna().groupby(by='regionidzip').mean().reset_index()
    mapData4 = pd.DataFrame(mapData4)
    mapData4['regionidzip'] = mapData4['regionidzip'].astype('int')


##############################3     Map Creation #############################################
    basicMap.make_map([["housevalues", mapData, 'regionidzip', 'taxvaluedollarcnt',"housevalues","YlGn"],
                       ["sizeofhouse", mapData1, 'regionidzip', 'priceVsHouseSize',"sizeofhousevsprice","RdPu"],
                       ["priceVsYearBuilt", mapData2, 'regionidzip', 'priceVsYearBuilt',"priceVsYearBuilt","OrRd"],
                       ["priceVsbedRoomCount", mapData3, 'regionidzip', 'priceVsbedRoomCount',"priceVsbedRoomCount","PuBuGn"],
                       ["sizeOfHouseVsbedRoomCount", mapData4, 'regionidzip', 'sizeOfHouseVsbedRoomCount',"sizeOfHouseVsbedRoomCount","YlOrBr"]], "House_Values.html")
    