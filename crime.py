# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 21:29:31 2022

@author: Kiran Ferrini
"""

# Diff in Diff and Natural Experiment to see the effect of increased police on crime rate using London Terror Attacks
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf 

fulldata = pd.read_csv('london_crime.csv')

# crimerate (# crimes / borough population)
fulldata['crimerate'] = fulldata['crime']/fulldata['population'] 

# policerate (# police hours / borough population)
fulldata['policerate'] = fulldata['police']/fulldata['population']

# create log variables of: crimerate, policerate, emp, un, ymale, white
fulldata['lcrime']  = np.log(fulldata['crimerate'])
fulldata['lpolice'] = np.log(fulldata['policerate'])
fulldata['lemp']    = np.log(fulldata['emp'])
fulldata['lun']     = np.log(fulldata['un'])
fulldata['lymale']  = np.log(fulldata['ymale'])
fulldata['lwhite']  = np.log(fulldata['white'])

# log-log model
model1 = smf.ols('lcrime ~ lpolice + lemp + lun + lymale + lwhite', 
                 data=fulldata).fit()


# preparing diff df
year1data = fulldata[fulldata['week'] <= 52]
year2data = fulldata[fulldata['week'] > 52]
year1data.reset_index(drop=True, inplace=True)
year2data.reset_index(drop=True, inplace=True)

# creating diff df
diffdata = pd.DataFrame().assign(week=year1data['week'], 
                                 population=year1data['population'], 
                                 borough=year1data['borough'])

# adding differenced variables 
diffdata['dlcrime']  = year2data['lcrime']  - year1data['lcrime']
diffdata['dlpolice'] = year2data['lpolice'] - year1data['lpolice']
diffdata['dlemp']    = year2data['lemp']    - year1data['lemp']
diffdata['dlun']     = year2data['lun']     - year1data['lun']
diffdata['dlymale']  = year2data['lymale']  - year1data['lymale']
diffdata['dlwhite']  = year2data['lwhite']  - year1data['lwhite']

# log-log diff in diff with week fixed effects model
model2 = smf.ols('dlcrime ~ dlpolice + dlemp + dlun + dlymale + dlwhite + C(week)',
                 data=diffdata).fit()  

# Part 3

# create dummy variables for terrorist attacks (weeks 80-85, so now 28-33)
diffdata['sixweeks'] = ((diffdata['week'] > 27) & 
                        (diffdata['week'] < 34)
                        ).astype(int)

# for 6 weeks AND 5 specific boroughs 
diffdata['sixweeks_treat'] = (((diffdata['borough'] == 1)   |
                               (diffdata['borough'] == 2)   |
                               (diffdata['borough'] == 3)   |
                               (diffdata['borough'] == 6)   |
                               (diffdata['borough'] == 14)) &
                               (diffdata['sixweeks'] > 0)
                               ).astype(int)

# 3rd regression using natural experiment of terror reaction
model3 = smf.ols('dlcrime ~ sixweeks_treat + sixweeks + dlemp + dlun + dlymale + dlwhite + C(week)',
                 data=diffdata).fit()

