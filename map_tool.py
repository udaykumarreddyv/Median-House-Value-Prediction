from geo_json_data import geo_json_data
from zipcode_mapping import Zipcode_Mapping
import pathlib
import folium  # Version 0.12.0
import numpy as np
import pandas as pd

class Map:
    '''
    Use this to make visualizations on a geo_json based dataset
    '''

    def __init__(self, geojson_file_path=str(r'./data/State-zip-code-GeoJSON/'),zipcode_map_zipcodes=None):
        assert isinstance(geojson_file_path, (pathlib.Path, str)),"geojson file path must be appropriate type"
        if isinstance(geojson_file_path, str):
            geojson_file_path = pathlib.Path(geojson_file_path)
        assert geojson_file_path.exists(),"file path must exist"+str(geojson_file_path)
        if not geojson_file_path.is_file():
            self.geodata = geo_json_data(fname=list(geojson_file_path.glob('*.json')))
        else:
            self.geodata = geo_json_data(fname=geojson_file_path)
        if zipcode_map_zipcodes is not None:
            self.geodata = self.geodata[zipcode_map_zipcodes]

    def make_map(self, listOfMaps,mapTitle):
        '''
        make and save the folium map
        :param listOfMaps: list[list[layerTitleStr,pd.DataFrame,zipcodeColumnStr,valueColumnStr]] unique zipcodes
        :return:
        '''
        assert isinstance(listOfMaps,list)
        
        m =folium.Map(location=[34.0522, -118.2437], zoom_start=10, zoom_control=True)
        base_map = folium.FeatureGroup(name='Basemap', overlay=True, control=False)
        folium.TileLayer(tiles='OpenStreetMap').add_to(base_map)
        base_map.add_to(m)
        # This assumes that the ordering in zipcodes is consistent (which it is because they are ordered lists
        for idx, mapping in enumerate(listOfMaps):
            assert isinstance(mapping,list)
            layerTitle = mapping[0]
            mapping[1]['regionidzip'] = mapping[1]['regionidzip'].astype(int)
            filteredGeodata = self.geodata[mapping[1]['regionidzip'].values]
            mapping[1]['regionidzip'] = mapping[1]['regionidzip'].astype(str)
            assert filteredGeodata is not None, "There are no matching zipcodes in layer "+str(idx)
            folium.Choropleth(
                # geo_data=geodata[zhZips['regionidzip'].unique()].dataJson,
                geo_data=filteredGeodata.dataJson,
                name=mapping[4],
                data=mapping[1],
                columns=['regionidzip', mapping[3]],
                key_on="feature.properties.ZCTA5CE10",
                fill_color=mapping[5],
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name=layerTitle,
                overlay=False
            ).add_to(m)
        folium.LayerControl().add_to(m)
        m.save(mapTitle)
        return m

def remove_upper_lower(df,fieldName,lower,upper):
    ulimit = np.percentile(df[fieldName].values, upper)
    llimit = np.percentile(df[fieldName].values, lower)
    normMap = df[df[fieldName] <= ulimit]
    normMap = normMap[normMap[fieldName] >= llimit]
    return normMap

def fix_zipcode_type(dfSeries, zipcodeColumnName):
    '''
    changes the zipcode type back to int for
    :param dfSeries: pd.series objecct containing data
    :param zipcodeColumnName: column containing zipcodes
    :return:
    '''
    outDF = dfSeries.dropna().groupby(
        by=zipcodeColumnName).mean().reset_index()
    outDF = pd.DataFrame(outDF)
    outDF[zipcodeColumnName] = outDF[zipcodeColumnName].astype('int')
    return outDF

