from geo_json_data import geo_json_data
import pathlib
import folium  # Version 0.12.0


class Map:
    '''
    Use this to make visualizations on a geo_json based dataset
    '''

    def __init__(self, geojson_file_path=str(r'./data/State-zip-code-GeoJSON/')):
        assert isinstance(geojson_file_path, (pathlib.Path, str)),"geojson file path must be appropriate type"
        if isinstance(geojson_file_path, str):
            geojson_file_path = pathlib.Path(geojson_file_path)
        assert geojson_file_path.exists(),"file path must exist"+str(geojson_file_path)
        if not geojson_file_path.is_file():
            self.geodata = geo_json_data(fname=list(geojson_file_path.glob('*.json')))
        else:
            self.geodata = geo_json_data(fname=geojson_file_path)
        pass

    def make_map(self, listOfMaps,mapTitle):
        '''
        make and save the folium map
        :param listOfMaps: list[list[layerTitleStr,pd.DataFrame,zipcodeColumnStr,valueColumnStr]] unique zipcodes
        :return:
        '''
        assert isinstance(listOfMaps,list)
        
        m =folium.Map(location=[48, -102], zoom_start=3)
        # This assumes that the ordering in zipcodes is consistent (which it is because they are ordered lists
        for mapping in listOfMaps:
            assert isinstance(mapping,list)
            print(mapping[0],mapping[2],mapping[3],mapping[4],mapping[5])
            layerTitle = mapping[0]
            filteredGeodata = self.geodata[mapping[1][mapping[2]].values]
            mapping[1]['regionidzip'] = mapping[1]['regionidzip'].astype(str)
            #mapVals = [mapping[1][i] for i in filteredGeodata.zipcodes]


            folium.Choropleth(
                # geo_data=geodata[zhZips['regionidzip'].unique()].dataJson,
                geo_data=filteredGeodata.dataJson,
                name=mapping[4],
                data=mapping[1],
                columns=[mapping[2], mapping[3]],
                key_on="feature.properties.ZCTA5CE10",
                fill_color=mapping[5],
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name=layerTitle,
            ).add_to(m)
        folium.LayerControl().add_to(m)
        m.save(mapTitle)
