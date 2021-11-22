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
    def onebedroomhouses(self,other):
        assert isinstance(other,pd.DataFrame)
        temp1=pd.DataFrame()
        temp1['regionidzip']=other['regionidzip']
        temp1['taxvaluedollarcnt1']=other['taxvaluedollarcnt'].astype('int')
        temp1['bedroom1']=np.where(other['bedroomcnt']== 1, True, False)
        temp1['bedroom1'] = temp1[temp1['bedroom1'] == True]
        temp1.dropna(subset = ["bedroom1"], inplace=True)
        temp1['bedroom1']=1
        temp1.to_csv(r'./data/zillowHousing/onebedroom.csv',index=False)
    def twobedroomhouses(self,other):
        assert isinstance(other,pd.DataFrame)
        temp1=pd.DataFrame()
        temp1['regionidzip']=other['regionidzip']
        temp1['taxvaluedollarcnt2']=other['taxvaluedollarcnt'].astype('int')
        temp1['bedroom2']=np.where(other['bedroomcnt']== 2, True, False)
        temp1['bedroom2'] = temp1[temp1['bedroom2'] == True]
        temp1.dropna(subset = ["bedroom2"], inplace=True)
        temp1['bedroom2']=2
        temp1.to_csv(r'./data/zillowHousing/twobedroom.csv',index=False)
    def threebedroomhouses(self,other):
        assert isinstance(other,pd.DataFrame)
        temp1=pd.DataFrame()
        temp1['regionidzip']=other['regionidzip']
        temp1['taxvaluedollarcnt3']=other['taxvaluedollarcnt'].astype('int')
        temp1['bedroom3']=np.where(other['bedroomcnt']== 3, True, False)
        temp1['bedroom3'] = temp1[temp1['bedroom3'] == True]
        temp1.dropna(subset = ["bedroom3"], inplace=True)
        temp1['bedroom3']=3
        temp1.to_csv(r'./data/zillowHousing/threebedroom.csv',index=False)
'''csv=pd.read_csv('datastories_table.csv')
print(type(csv))
obj=Heatmap_Values()
obj.onebedroomhouses(csv)'''

'''obj=Heatmap_Values()
obj.price_vs_sizeOfHouse(csv)
obj.price_vs_yearBuilt(csv)
obj.price_vs_bedRoomCount(csv)
obj.sizeOfHouse_vs_bedRoomCount(csv)
#price_vs_sizeOfHouse(csv)'''