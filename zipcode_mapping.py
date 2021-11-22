import geopy # Version 2.2.0
from time import sleep
import pickle
import pandas as pd
import pathlib


class Zipcode_Mapping:
    '''
    Use this class to load and save the zipcode mapping from the zillow dataset to
    example usage:
    zm = Zipcode_Mapping()
    zm.create_mapping(zhLatLong)
    zm.save_mapping()
    zm.zipcodes
    '''

    def __init__(self):
        '''
        load constants for internal use
        '''
        self._geolocator = geopy.Nominatim(user_agent='zillow-data-validation')
        self.zipcodes = None
        pass

    def _get_zipcode(self, df):
        '''
        query Nominatim API via geopy to get closest zipcode to the lat long calculated
        :param df: pd.DataFrame with columns ['latitude','longitude'] and row index: 'regionidzip'
        '''
        # Due to Nominatim TOS we must not query more than once per second
        sleep(1.01)
        location = self._geolocator.reverse((df['latitude'], df['longitude']))
        if ((location is not None) and
                (location.raw is not None) and
                ('address' in location.raw.keys()) and
                ('postcode' in location.raw['address'].keys())):
            return ((df.name), int(location.raw['address']['postcode'][:5]))
        else:
            return (df.name, None)

    def save_mapping(self, fname="zipcode_mapping.pickle"):
        '''
        :param fname: name of new file
        '''
        assert isinstance(fname, (pathlib.Path, str))
        if isinstance(fname, str):
            fname = pathlib.Path(fname)
        with open(fname, 'wb') as f:
            pickle.dump(self.zipcodes, f)

        pass

    def create_mapping(self, df):
        '''
        :param df: pd.DataFrame with columns ['latitude','longitude'] and row index: 'regionidzip'
        '''
        assert isinstance(df, pd.DataFrame)
        self.zipcodes = df.apply(self._get_zipcode, axis=1)
        self.zipcodes = {i[0]: i[1] for i in self.zipcodes.values}

    def load_mapping(self, fname="zipcode_mapping.pickle"):
        '''
        warning, the fname file will be unpickled. this data can come from anywhere and can be malicious
        The dict is of the form WrongZip:RealZip
        :param fname: name of pickle file
        '''
        assert isinstance(fname, (pathlib.Path, str))
        if isinstance(fname, str):
            fname = pathlib.Path(fname)

        if fname.exists():
            with open(fname, 'rb') as f:
                self.zipcodes = pickle.load(f)
                return True
        else:
            return False
