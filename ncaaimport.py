# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 17:27:56 2022

@author: Kiran Ferrini
"""


def ncaaimport(y):
    
    import pandas as pd
    
    if isinstance(y, pd.DataFrame):
        df = y
    else:    
        df = pd.read_fwf('https://wilson.engr.wisc.edu/rsfc/history/howell/cf'+str(y)+'gms.txt',
                     colspecs = [(0,10), (10,39), (39,42), (42,70), (70,73)],
                     names = ['date', 'awayteam', 'awayscore', 'hometeam', 'homescore'])
    
    df['tie'] = (df['awayscore'] == df['homescore']).astype(int)
    df['homewin'] = (df['awayscore'] < df['homescore']).astype(int)
    df['awaywin'] = (df['awayscore'] > df['homescore']).astype(int)
    df['pointdiffaway'] = df['awayscore'] - df['homescore']
    df['pointdiffhome'] = -1*df['pointdiffaway']
    df['homegames'] = df.groupby('hometeam')['homescore'].transform('count')
    df['awaygames'] = df.groupby('awayteam')['awayscore'].transform('count')


    adf = df.groupby('awayteam').agg({'awaygames':'count',
                                      'awaywin':'sum',
                                      'tie':'sum',
                                      'pointdiffaway': 'sum'})

    hdf = df.groupby('hometeam').agg({'homegames':'count',
                                      'homewin':'sum',
                                      'tie':'sum',
                                      'pointdiffhome': 'sum'})

    adf.reset_index(inplace = True)
    hdf.reset_index(inplace = True)

    odf = pd.merge(adf, hdf, left_on=('awayteam'), right_on=('hometeam'), how='outer')

    odf[['awaygames','awaywin','tie_x','tie_y','pointdiffaway',
         'homegames','homewin','pointdiffhome']] = odf[['awaygames','awaywin','tie_x','tie_y','pointdiffaway',
                                                        'homegames','homewin','pointdiffhome']].fillna(0)                                                    
                                   
                                                    
    odf['totalgames'] = odf['awaygames'] + odf['homegames']
    
    odf['team'] = odf['awayteam'].fillna(odf['hometeam'])
    odf['wins'] = odf['awaywin'] + odf['homewin']
    odf['ties'] = odf['tie_x'] + odf['tie_y']
    odf['losses'] = odf['totalgames'] - odf['wins'] - odf['ties']
    odf['pointdiff'] = odf['pointdiffaway'] + odf['pointdiffhome']


    odf.drop(odf.columns[0:11], axis=1, inplace=True)

    return odf



df = ncaaimport(2004)