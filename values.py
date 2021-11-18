#creating different values for the map
import numpy as np
import pandas as pd


class Heatmap_Values:
    def price_vs_sizeOfHouse(self,other):
        '''This method gives ratio bw Prices and Size of Houses'''
        assert isinstance(other,pd.DataFrame)
        other['priceVsHouseSize']=other['taxvaluedollarcnt']/other['calculatedfinishedsquarefeet']
        temp=pd.DataFrame()
        temp['priceVsHouseSize']=other['priceVsHouseSize']
        temp['regionidzip']=other['regionidzip']
        temp.to_csv(r'./data/zillowHousing/pricevssizeofHouse.csv',index=False)
        
    def price_vs_yearBuilt(self,other):
        '''This method gives ratio bw Prices and Year Built'''
        assert isinstance(other,pd.DataFrame)
        other['priceVsYearBuilt']=other['taxvaluedollarcnt']/other['yearbuilt']
        temp=pd.DataFrame()
        temp['priceVsYearBuilt']=other['priceVsYearBuilt']
        temp['regionidzip']=other['regionidzip']
        temp.to_csv(r'./data/zillowHousing/pricevsYearBuilt.csv',index=False)
    
    def price_vs_bedRoomCount(self,other):
        '''This method gives ratio bw Prices and BedRoom Count'''
        assert isinstance(other,pd.DataFrame)
        other['priceVsbedRoomCount']=other['bedroomcnt']/other['taxvaluedollarcnt']
        temp=pd.DataFrame()
        temp['priceVsbedRoomCount']=other['priceVsbedRoomCount']
        temp['regionidzip']=other['regionidzip']
        temp.to_csv(r'./data/zillowHousing/pricevsbedroomcount.csv',index=False)

    def sizeOfHouse_vs_bedRoomCount(self,other):
        '''This method gives ratio bw Prices and Year Built'''
        assert isinstance(other,pd.DataFrame)
        other['sizeOfHouseVsbedRoomCount']=other['bedroomcnt']/other['calculatedfinishedsquarefeet']
        temp=pd.DataFrame()
        temp['sizeOfHouseVsbedRoomCount']=other['sizeOfHouseVsbedRoomCount']
        temp['regionidzip']=other['regionidzip']
        temp.to_csv(r'./data/zillowHousing/sizeofhousevsbedroomcount.csv',index=False)
'''
csv=pd.read_csv(r'./data/zillowHousing/clean_data_2016.csv')
print(type(csv))
obj=Heatmap_Values()
obj.price_vs_sizeOfHouse(csv)
obj.price_vs_yearBuilt(csv)
obj.price_vs_bedRoomCount(csv)
obj.sizeOfHouse_vs_bedRoomCount(csv)
#price_vs_sizeOfHouse(csv)'''