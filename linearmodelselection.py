# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 14:15:17 2022

Forward and Backwards stepwise algorithms for linear model selection

author: kiranferrini
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import (cross_val_score, KFold)


def forward(X,y):
    candidates = {}
    klist = []
    klist.extend(range(0, X.shape[1]))
    bestlist = []
    while len(klist) > 0:
        pdict = {}
        for k in klist:
            plist = bestlist.copy()
            plist.append(k)
            scores = cross_val_score(LinearRegression(),X.iloc[:,plist],y,cv=KFold(5,shuffle=True,random_state=0),scoring="neg_mean_squared_error")
            pdict[np.mean(scores)] = k 
        i = pdict[max(pdict)]
        mse = max(pdict)
        bestlist.append(i)
        candidates[mse] = bestlist.copy()
        klist.remove(i)
    best = max(candidates)
    variables = candidates[best]
    model = LinearRegression()
    model.fit(X.iloc[:,variables],y)
    model.coef_
    rl = [variables, model.coef_]
    return rl


def backward(X,y):
    candidates = {}
    klist = []
    klist.extend(range(0, X.shape[1]))
    candidates[np.mean(cross_val_score(LinearRegression(),X,y,cv=KFold(5,shuffle=True,random_state=0),scoring="neg_mean_squared_error"))] = klist.copy()
    while len(klist) > 1: 
        pdict = {}
        for k in klist:
            plist = klist.copy()
            plist.remove(k)
            scores = cross_val_score(LinearRegression(),X.iloc[:,plist],y,cv=KFold(5,shuffle=True,random_state=0),scoring="neg_mean_squared_error")
            pdict[np.mean(scores)] = k
        i = pdict[max(pdict)]
        mse = max(pdict)
        klist.remove(i)
        candidates[mse] = klist.copy()
    best = max(candidates)
    variables = candidates[best]
    model = LinearRegression()
    model.fit(X.iloc[:,variables],y)
    model.coef_
    rl = [variables, model.coef_]
    return rl









        




        