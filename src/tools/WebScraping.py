import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from NumericalTools import multivariate_plane_fitting


def unit_conversion(engine_data: pd.DataFrame):

    engine_data['Power'] *= 0.7457  # shp to kW
    engine_data['SFC'] *= 0.6082773878418  # lb/shp-hr to kg/kw-hr
    engine_data['Diameter'] *= 0.0254  # inch to m
    engine_data['Length'] *= 0.0254  # inch to m
    engine_data['Weight'] *= 0.453592  # lb to kg


def import_engine_Data(which: str = 'civ'):

    if which == 'civ':
        link = 'http://www.jet-engine.net/civtsspec.html'

    elif which == 'mil':
        link = 'http://www.jet-engine.net/miltsspec.html'

    columns = ['Manufacturer', 'Model', 'Application(s)', 'Power', 'SFC', 'Airflow', 'OPR', 'Number', 'LPC', 'HPC', 'HPT', 'IPT', 'LPT', 'Length', 'Diameter', 'Weight']

    Engine_Data = pd.read_html(link)[1].iloc[7:, 1:17]
    Engine_Data.columns = columns
    Engine_Data.replace('-', np.NaN, inplace=True)
    Engine_Data.dropna(axis=0, subset=['Power', 'Weight', 'SFC'], inplace=True)

    Engine_Data.reset_index(drop=True, inplace=True)

    Engine_Data[['Power', 'SFC', 'Airflow', 'OPR', 'HPT', 'LPT', 'Length', 'Diameter', 'Weight']] = Engine_Data[['Power', 'SFC', 'Airflow', 'OPR', 'HPT', 'LPT', 'Length', 'Diameter', 'Weight']].astype('float64')

    unit_conversion(Engine_Data)

    return Engine_Data


def save_to_csv(dataframe: pd.DataFrame, filename: str, datafolder: str = r'C:\Users\LRdeWaal\Desktop\DSE2019\data\reference_engines'):

    dataframe.to_csv(datafolder + '\\' + filename)


def filter_values(df: pd.DataFrame, filter_ranges: dict):

    for column in filter_ranges.keys():
        df = df.loc[(df[column] >= filter_ranges[column][0]) & (df[column] <= filter_ranges[column][1])]

    return df


def extract_filtered_data(filter_dict: dict, dataframe: pd.DataFrame = None):

    if dataframe is None:
        civdata = import_engine_Data('civ')
        mildata = import_engine_Data('mil')

        # save_to_csv(civdata, 'civengines.csv')
        # save_to_csv(mildata, 'milengines.csv')

        data = pd.concat([civdata, mildata])

    else:
        data = dataframe

    filtered_data = filter_values(data, filter_dict)

    data = filtered_data.reset_index(drop=True)
    return data


if __name__ == '__main__':

    civdata = import_engine_Data('civ')
    mildata = import_engine_Data('mil')

    # save_to_csv(civdata, 'civengines.csv')
    # save_to_csv(mildata, 'milengines.csv')

    data = pd.concat([civdata, mildata])

    filtered_data = filter_values(data, {
        'Power': (1000, 2500),  # kW
        'Weight': (150, 550),   # kg
        'SFC': (0.15, 0.35)    # kg/kW-hr
    }
    )

    # data = np.array(filtered_data.reset_index()[['Power', 'Weight', 'SFC']])

    fig = plt.figure()

    multivariate_plane_fitting(data=np.array(mildata[['Power', 'Weight', 'SFC']]), order=2, colour='b', fig=fig)
    multivariate_plane_fitting(data=np.array(civdata[['Power', 'Weight', 'SFC']]), order=2, colour='r', fig=fig)
