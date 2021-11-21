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

    zhData['priceVsbedRoomCount'] = ((zhData['priceVsbedRoomCount']-zhData['priceVsbedRoomCount'].min())/
                                 (zhData['priceVsbedRoomCount'].max()-zhData['priceVsbedRoomCount'].min()))
   

    mapData3 = zhData[['regionidzip', 'priceVsbedRoomCount']].dropna().groupby(by='regionidzip').mean().reset_index()
    mapData3 = pd.DataFrame(mapData3)
    mapData3['regionidzip'] = mapData3['regionidzip'].astype('int')

    ###########################sizeofhouse vs bedroomcount##############################################

    zhData['sizeOfHouseVsbedRoomCount'] = ((zhData['sizeOfHouseVsbedRoomCount']-zhData['sizeOfHouseVsbedRoomCount'].min())/
                                 (zhData['sizeOfHouseVsbedRoomCount'].max()-zhData['sizeOfHouseVsbedRoomCount'].min()))
   
    mapData4 = zhData[['regionidzip', 'sizeOfHouseVsbedRoomCount']].dropna().groupby(by='regionidzip').mean().reset_index()
    mapData4 = pd.DataFrame(mapData4)
    mapData4['regionidzip'] = mapData4['regionidzip'].astype('int')
#####################one bedroom prices###############################
    zhData=pd.read_csv(zillowHousing)
    HeatValues.onebedroomhouses(zhData)
    zillowHousing1 = pathlib.Path(r'./data/zillowHousing/onebedroom.csv',index=False)
    zhData=pd.read_csv(zillowHousing1)
    print(type(zhData))
    zhData['regionidzip'] = zhData['regionidzip'].astype('int')
    zhData['regionidzip'] = zhData['regionidzip'].map(zm.zipcodes)
    zhData['taxvaluedollarcnt1'] = ((zhData['taxvaluedollarcnt1']-zhData['taxvaluedollarcnt1'].min())/
                                (zhData['taxvaluedollarcnt1'].max()-zhData['taxvaluedollarcnt1'].min()))
   
    mapData5 = zhData[['regionidzip', 'taxvaluedollarcnt1']].dropna().groupby(by='regionidzip').mean().reset_index()
    mapData5 = pd.DataFrame(mapData5)
    mapData5['regionidzip'] = mapData5['regionidzip'].astype('int')
    #############two bedroom prices##################################
    zhData=pd.read_csv(zillowHousing)
    HeatValues.twobedroomhouses(zhData)
    zillowHousing1 = pathlib.Path(r'./data/zillowHousing/twobedroom.csv',index=False)
    zhData=pd.read_csv(zillowHousing1)
    zhData['regionidzip'] = zhData['regionidzip'].astype('int')
    zhData['regionidzip'] = zhData['regionidzip'].map(zm.zipcodes)
    zhData['taxvaluedollarcnt2'] = ((zhData['taxvaluedollarcnt2']-zhData['taxvaluedollarcnt2'].min())/
                                 (zhData['taxvaluedollarcnt2'].max()-zhData['taxvaluedollarcnt2'].min()))
   
    mapData6 = zhData[['regionidzip', 'taxvaluedollarcnt2']].dropna().groupby(by='regionidzip').mean().reset_index()
    mapData6 = pd.DataFrame(mapData6)
    mapData6['regionidzip'] = mapData6['regionidzip'].astype('int')

    
    #############three bedroom prices##################################
    zhData=pd.read_csv(zillowHousing)
    HeatValues.threebedroomhouses(zhData)
    zillowHousing1 = pathlib.Path(r'./data/zillowHousing/threebedroom.csv',index=False)
    zhData=pd.read_csv(zillowHousing1)
    zhData['regionidzip'] = zhData['regionidzip'].astype('int')
    zhData['regionidzip'] = zhData['regionidzip'].map(zm.zipcodes)
    zhData['taxvaluedollarcnt3'] = ((zhData['taxvaluedollarcnt3']-zhData['taxvaluedollarcnt3'].min())/
                                 (zhData['taxvaluedollarcnt3'].max()-zhData['taxvaluedollarcnt3'].min()))
   
    mapData7 = zhData[['regionidzip', 'taxvaluedollarcnt3']].dropna().groupby(by='regionidzip').mean().reset_index()
    mapData7 = pd.DataFrame(mapData7)
    mapData7['regionidzip'] = mapData7['regionidzip'].astype('int')

##############################3     Map Creation #############################################
    basicMap.make_map([["housevalues", mapData, 'regionidzip', 'taxvaluedollarcnt',"housevalues","YlGn"],
                       ["sizeofhouse", mapData1, 'regionidzip', 'priceVsHouseSize',"sizeofhousevsprice","RdPu"],
                       ["priceVsYearBuilt", mapData2, 'regionidzip', 'priceVsYearBuilt',"priceVsYearBuilt","OrRd"],
                       ["priceVsbedRoomCount", mapData3, 'regionidzip', 'priceVsbedRoomCount',"priceVsbedRoomCount","PuBuGn"],
                       ["sizeOfHouseVsbedRoomCount", mapData4, 'regionidzip', 'sizeOfHouseVsbedRoomCount',"sizeOfHouseVsbedRoomCount","YlOrBr"],
                       ["One Bedroom prices", mapData5, 'regionidzip', 'taxvaluedollarcnt1',"One Bedroom prices","RdPu"],
                       ["Two Bedroom prices", mapData6, 'regionidzip', 'taxvaluedollarcnt2',"Two Bedroom prices","YlOrBr"],
                       ["Three Bedroom prices", mapData7, 'regionidzip', 'taxvaluedollarcnt3',"Three Bedroom prices","PuBuGn"]], "Heat_Maps_Comparisons.html")
    