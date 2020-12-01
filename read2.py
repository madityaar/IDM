# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 20:38:02 2020

@author: madit
"""

import pandas as pd

df_value = pd.read_csv('dataset.csv', delimiter =";",skip_blank_lines=True)
df_label = pd.read_csv('dataset_label.csv', delimiter =";",skip_blank_lines=True, index_col=False,header=None)

df_labeled= pd.concat([df_label,df_value['Bojongsoang'].rename(columns={'values'})], axis=1)
df_labeled.columns=['label','index']

print(df_value['Sukapura'][slice(0, 10)])