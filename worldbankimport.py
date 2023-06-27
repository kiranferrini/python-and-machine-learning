# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 12:20:59 2022

@author: Kiran Ferrini
"""

from bs4 import BeautifulSoup
import urllib.request as url
import pandas as pd

def worldbankimport(country, indic):
    if isinstance(country, list) and isinstance(indic, list):
        pass
    else: 
        return 'inputs must be lists'
    for c in country:
        if isinstance(c, str):
            pass
        else:
            raise TypeError('country input list can only contain strings')
    for i in indic:
        if isinstance(i, str):
            pass
        else:
            raise TypeError('indicator input list can only contain strings')
    
    
    
    urlstring = 'https://api.worldbank.org/v2/country/'+";".join(country)+'/indicator/'+";".join(indic)+'?source=2'
    req = url.Request(urlstring)
    file = url.urlopen(req)    
    soup = BeautifulSoup(file, "lxml")
    xhtag = soup.find_all(True, recursive = False)[0]
    xbtag = xhtag.find_all(True, recursive = False)[0]
    xtag = xbtag.find_all(True, recursive = False)[0]
    
    if xtag.name == 'wb:error':
        raise ValueError(xtag.find_all(True, recursive = False)[0]['key'] + ': ' + xtag.find_all(True, recursive = False)[0].text)
    
    totalpages = int(xtag['pages'])
    
    rowlist = []
    
    for i in range(1, totalpages+1, 1):
        urlstring = 'https://api.worldbank.org/v2/country/'+";".join(country)+'/indicator/'+";".join(indic)+'?source=2&page='+str(i)
        req = url.Request(urlstring)
        file = url.urlopen(req)    
        soup = BeautifulSoup(file, "lxml")
        xhtag = soup.find_all(True, recursive = False)[0]
        xbtag = xhtag.find_all(True, recursive = False)[0]
        xtag = xbtag.find_all(True, recursive = False)[0]
        xtags = xtag.find_all(True, recursive = False)
        for i in range(len(xtags)):
            row = xtags[i]
            cells = row.find_all(True, recursive = False)
            rowdict = {}
            for j in range(len(cells)):
                if 'id' in cells[j].attrs:
                    rowdict[str(cells[j].name + 'id')] = str(cells[j]['id'])
                rowdict[str(cells[j].name)] = str(cells[j].string)
            rowlist.append(rowdict)
       
    df = pd.DataFrame.from_records(rowlist)
    
    return df
    
            
df1 = worldbankimport(['CHN','USA'], ['NY.GDP.PCAP.CD','EG.ELC.ACCS.RU.ZS'])
    
   
    

