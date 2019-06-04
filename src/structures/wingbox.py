#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 13:40:27 2019

@author: liesbethwijn
"""
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import pandas as pd

### Google Sheet Import ###
sys.path.insert(0, '/'.join(os.getcwd().split('/')[:-1]) + '/tools')
from GoogleSheetsImportMac import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID
data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()

#wingbox
MAC = data['Aero']['Wing chord']
coordinates = pd.read_fwf('wingboxdimensions', names=['x', 'y'])
h_right=coordinates['y'][1]-coordinates['y'][0]
h_left=coordinates['y'][3]-coordinates['y'][2]
print(abs(h_right),abs(h_left))


