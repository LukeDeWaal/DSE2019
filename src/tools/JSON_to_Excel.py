import json
import pandas as pd
import numpy as np


class Converter(object):

    def __init__(self, json_file: str):

        self.__json = json_file
        self.__raw_data = None
        self.__data = {}

        self.__extract_JSON_data()
        self.__process_JSON_data()
        self.__dump_into_excel()

    def get_data(self):
        return self.__data, self.__raw_data


    def __extract_JSON_data(self):

        with open(self.__json, 'r') as file:
            self.__raw_data = json.load(file)

    @staticmethod
    def recursive_dict_extractor(raw_dict: dict, processed_dict: dict, outer_key: str = None):

        for key, value in raw_dict.items():

            print(outer_key)

            if type(value) != dict:
                if outer_key is None:
                    processed_dict[key] = value

                else:
                    processed_dict[f"{outer_key}_{key}"] = value

            else:
                if outer_key is not None:
                    key = outer_key + key
                Converter.recursive_dict_extractor(value, processed_dict, outer_key=key)

    def __process_JSON_data(self):

        self.recursive_dict_extractor(self.__raw_data, self.__data)

    def __dump_into_excel(self):

        self.__data = pd.DataFrame.from_dict(self.__data)



if __name__ == '__main__':

    C = Converter(r'C:\Users\LRdeWaal\Desktop\DSE2019\data\Class II Data\twin_engine_estimate.json')
    a = C.get_data()
