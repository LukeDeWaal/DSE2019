#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 14:49:34 2019

@author: liesbethwijn
"""
import numpy as np
import os
import sys
#import matplotlib.pyplot as plt
#import pandas as pd

### Google Sheet Import ###
sys.path.insert(0, '/'.join(os.getcwd().split('/')[:-1]) + '/tools')
from GoogleSheetsImportMac import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID
data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()

C_rm=0.75
theta=4
GW= (data['Weights']['WL[N]'])/9.80665/2
GM= 2 #metacentric height
y_tip=(data['Aero']['Wing Span'])/2/.3

#righting moment to be counteracted by tip float
MR=C_rm*GW*(GM+GW**(1/3))*np.sin(np.radians(theta)) #righting moment

#volume of float needed
V_fl=MR/y_tip
#tipfloat dimensions

l_fl=(32*V_fl)**(1/3)*.3
b_fl=l_fl/4
d_fl=b_fl*0.5

print(l_fl,b_fl,d_fl)




