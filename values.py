#creating different values for the map
import numpy as np
import pandas as pd


class Heatmap_Values:
    def price_vs_sizeOfHouse(self,other):
        '''This method gives ratio bw Prices and Size of Houses'''
        assert isinstance(other,pd.DataFrame)
        other['priceVsHouseSize']=other['taxvaluedollarcnt']/other['calculatedfinishedsquarefeet']
        other.to_csv(r'./data/zillowHousing/clean_data_2016.csv',index=False)
        
    def price_vs_yearBuilt(self,other):
        '''This method gives ratio bw Prices and Year Built'''
        assert isinstance(other,pd.DataFrame)
        other['priceVsYearBuilt']=other['taxvaluedollarcnt']/other['yearbuilt']
        other.to_csv(r'./data/zillowHousing/clean_data_2016.csv',index=False)
    
    def price_vs_bedRoomCount(self,other):
        '''This method gives ratio bw Prices and BedRoom Count'''
        assert isinstance(other,pd.DataFrame)
        other['priceVsbedRoomCount']=other['bedroomcnt']/other['taxvaluedollarcnt']
        other.to_csv(r'./data/zillowHousing/clean_data_2016.csv',index=False)

    def sizeOfHouse_vs_bedRoomCount(self,other):
        '''This method gives ratio bw Prices and Year Built'''
        assert isinstance(other,pd.DataFrame)
        other['sizeOfHouseVsbedRoomCount']=other['bedroomcnt']/other['calculatedfinishedsquarefeet']
        other.to_csv(r'./data/zillowHousing/clean_data_2016.csv',index=False)
'''
csv=pd.read_csv(r'./data/zillowHousing/clean_data_2016.csv')
print(type(csv))
obj=Heatmap_Values()
obj.price_vs_sizeOfHouse(csv)
obj.price_vs_yearBuilt(csv)
obj.price_vs_bedRoomCount(csv)
obj.sizeOfHouse_vs_bedRoomCount(csv)
#price_vs_sizeOfHouse(csv)'''