from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pandas as pd
import os

SPREADSHEET_ID = '1VLmc3ztGtdGbx9eByuzozoL7C7KxIqqI5o5sgheA4SQ'  # <Your spreadsheet ID>
SHEET_NAMES = ['Weights', 'C&S', 'Aero', 'Structures', 'FPP', 'Operations', 'Internal']


class GoogleSheetsDataImport(object):

    def __init__(self, SPREADSHEET_ID: str = SPREADSHEET_ID, *pages):

        self.__sheet_id = SPREADSHEET_ID
        self.__pages = pages

        self.__sheets = {}
        self.__import_sheets()

        self.__dataframes = {key: self.__sheet_to_dataframe(value) for key, value in self.__sheets.items()}

    def get_data(self):
        return self.__dataframes

    def __import_sheets(self):

        scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'
        # Setup the Sheets API
        store = file.Storage('/'.join(os.getcwd().split('/')[:-1]) + '/tools/credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('/'.join(os.getcwd().split('/')[:-1]) + '/tools/client_secret.json', scopes)
            creds = tools.run_flow(flow, store)
        service = build('sheets', 'v4', http=creds.authorize(Http()))

        # Call the Sheets API
        for page in self.__pages:
            gsheet = service.spreadsheets().values().get(spreadsheetId=self.__sheet_id, range=page).execute()
            self.__sheets[page] = gsheet

    @staticmethod
    def __sheet_to_dataframe(gsheet):

        def istext(item: str):
            for char in item:
                if 65<= ord(char) <= 90 or 97 <= ord(char) <= 122:
                    return True
                else:
                    continue

        try:
            header = gsheet.get('values', [])[0]  # Assumes first line is header!

        except IndexError:
            return

        values = gsheet.get('values', [])[1:]  # Everything else is data.

        if not values:
            print('No data found.')
            return pd.Series(header)

        else:
            all_data = []
            for col_id, col_name in enumerate(header):
                column_data = []
                for row in values:
                    #print(col_id)
                    item = row[col_id]
                    #print(item)
                    if '[' in item:
                        item = [float(i) for i in item[1:-1].split(',')]

                    elif col_name == 'Date' or col_name == 'Notes':
                        pass

                    elif not istext(item):
                        item = float(item)

                    else:
                        pass

                    column_data.append(item)

                ds = pd.Series(data=column_data, name=col_name)
                all_data.append(ds)
            df = pd.concat(all_data, axis=1)
            return df.iloc[0]


if __name__ == '__main__':

    G = GoogleSheetsDataImport(SPREADSHEET_ID, 'Weights', 'C&S')
    data = G.get_data()
