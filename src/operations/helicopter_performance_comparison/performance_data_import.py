import json
import os


class HelicopterDataImport(object):

    def __init__(self):

        self.data = {}

    def get_data(self):
        return self.data

    @staticmethod
    def import_data(data_type: str):
        cwd = os.getcwd()
        cwd = cwd.split('\\')

        data_folder = ''
        for folder in cwd:
            data_folder += folder + "\\"
            if folder == 'DSE2019':
                data_folder += "data\\operations_data"
                break

        with open(data_folder + '\\' + f'{data_type}.json') as file:
            data = json.load(file)

        return data


class ReferenceHelicopters(HelicopterDataImport):

    def __init__(self):

        super().__init__()

        self.data = self.import_data('Helicopter_performance')


class CL415StatData(HelicopterDataImport):

    def __init__(self):

        super().__init__()

        self.data = self.import_data('CL415_statistical_performance')


class CL415EstData(HelicopterDataImport):

    def __init__(self):

        super().__init__()

        self.data = self.import_data('CL415_estimated_performance')


class CL415CompData(HelicopterDataImport):

    def __init__(self):

        super().__init__()

        self.data = self.import_data('Aircraft_performance')




