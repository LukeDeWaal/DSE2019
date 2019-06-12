#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 14:48:07 2019

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

rho_w=1000 
g=9.80665
W_to= (data['Weights']['WTO [N]'])
Delta_V=W_to/rho_w/g
F_b=Delta_V

K_hull=1.4
L_hw=9/0.3084
V_hull=K_hull*np.sqrt(L_hw)*0.5444

