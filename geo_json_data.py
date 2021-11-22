import pathlib
import json
import copy
import numpy as np


class geo_json_data():
    def __init__(self, fname: pathlib.Path = None, dataJson: json = None):
        '''
        :param fname:fname is a pathlib.Path or a list of pathlib.Paths
        :param dataJson: a json containing geojson information
        '''
        assert fname != None or dataJson != None, "need either fname or dataJson"

        if fname != None:
            assert isinstance(fname, (pathlib.Path, list)), "fname msut be path or list of paths"
            if isinstance(fname, pathlib.Path):

                assert fname.exists() and not fname.is_dir(), "fname file must exist"
                self.filePath = fname
                with open(fname, 'rt') as f:
                    self.dataJson = json.load(f)
            elif isinstance(fname, list):
                assert len(fname) > 0
                self.filePath = fname
                assert fname[0].exists() and not fname[0].is_dir(), "first path must exist "
                with open(fname[0], 'rt') as f:
                    self.dataJson = json.load(f)
                for i in fname[1:]:
                    assert isinstance(i, pathlib.Path), "must be list of path objects"
                    assert i.exists() and not i.is_dir(), "path must exist"
                    with open(i, 'rt') as f:
                        temp = json.load(f)['features']
                        self.dataJson['features'] = self.dataJson['features'] + temp

        elif dataJson != None:
            self.dataJson = dataJson
        else:
            # this shouldn't be possible
            pass

        self.zipcodes = {int(self.dataJson['features'][idx]['properties']['ZCTA5CE10']): idx
                         for idx in range(len(self.dataJson['features']))}
        pass

    def __getitem__(self, zipcode):
        '''
        zipcode is a int,tuple, or list of zipcodes
        If any item in zipcodes is in our lsit we will return a geo_json_data object,
        or will return None if zipcode is not in geodata list
        exmaple usage:
        #geo_json_data[zipcode]
        #geo_json_data[[zipcode1,zipcode2]]
        '''
        # this should return a geo_json_data object containing the specified keys
        assert isinstance(zipcode,
                          (list, tuple, int, np.ndarray)), "indexer must be of type list,tuple, or int, not: " + str(
            type(zipcode))
        if isinstance(zipcode, (list, tuple, np.ndarray)):
            temp = copy.deepcopy(self.dataJson)

            temp['features'] = [temp['features'][self.zipcodes[i]] for i in zipcode if i in self.zipcodes]
            if len(temp['features']) == 0:
                return None
            else:
                return geo_json_data(dataJson=temp)
        elif isinstance(zipcode, int):
            if zipcode in self.zipcodes:
                temp = copy.deepcopy(self.dataJson)
                temp['features'] = [temp['features'][self.zipcodes[zipcode]]]
                return geo_json_data(dataJson=temp)
            return None
        return None
        # should not get to this point
        pass

    def __add__(self, other):
        '''
        adding two geo_json_data concatenates their zipcodes together
        '''
        assert isinstance(other, geo_json_data), "addition must be between geo_json_data objects"
        temp = copy.deepcopy(self.dataJson)
        out = [i for i in temp['features']]
        for i in other.dataJson['features']:
            if i not in out:
                out.append(i)

        temp['features'] = out
        return geo_json_data(dataJson=temp)