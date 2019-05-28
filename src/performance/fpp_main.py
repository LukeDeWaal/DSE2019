#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 16:08:54 2019

@author: Leanne
"""

import pandas as pd
import numpy as np

excel_file = 'fpp_parameters.xlsx'
parameters = pd.read_excel(excel_file)

print(parameters)

# print(parameters.shape)
for i in range(2):
    parameters.insert(loc=2, column= f'Test_{i}', value = [0,1,2,3,4,5], allow_duplicates=True)

print(parameters)

parameters.to_excel(excel_file, index=False)
