# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 14:59:25 2022

Examples of using SQL within Python -- Also creates a function for automating frequently used queries

@author: kiranferrini
"""

import sqlite3
import pandas as pd

con = sqlite3.connect('northwind.db')

d1 = pd.read_sql_query("select * from Orders where ShipCountry = 'USA'", con)
d2 = pd.read_sql_query("select distinct Country from Customer", con)
d3 = pd.read_sql_query("select Country, count(Country) as TotalCustomers "+
                        "from Customer group by Country having TotalCustomers > 1 "+
                        "order by TotalCustomers desc", con) 
d4 = pd.read_sql_query("select Orders.Id from Orders join Customer on Orders.CustomerId = Customer.Id "+
                        "where Orders.ShipCountry != Customer.Country", con) 
d5 = pd.read_sql_query("select OrderId, sum((1-Discount)*UnitPrice*Quantity) as TotalRevenue from OrderDetail group by OrderId", con)
d6 = pd.read_sql_query("select OrderDetail.OrderId, OrderDate, sum((1-Discount)*UnitPrice*Quantity) as TotalRevenue from OrderDetail "+
                        "join Orders on OrderDetail.OrderId = Orders.Id join Customer on Orders.CustomerId = Customer.Id "+
                        "group by OrderDetail.OrderId having Customer.Country = 'USA'", con)
d7 = pd.read_sql_query("select CompanyName from Orders join Customer on Orders.CustomerId = Customer.Id where ShipCity = 'Eugene' group by CompanyName", con)
d8 = pd.read_sql_query("select distinct CompanyName from Customer where Id in (select CustomerId from Orders where ShipCity = 'Eugene' group by CustomerId having count(CustomerId) > 1)", con)

d8 = pd.read_sql_query("SELECT distinct Customer.CompanyName from Orders JOIN Customer on Customer.Id=Orders.CustomerId where ShipCity='Eugene' group by Orders.CustomerId HAVING count(Orders.CustomerId)>1",con)
con.close()

def orderlookup(city, country):
    if isinstance(city, str) and isinstance(country, str):
        pass
    else: 
        raise TypeError("invalid input type")
        
    import sqlite3
    import pandas as pd
    con = sqlite3.connect('northwind.db')
    df = pd.read_sql_query("select * from Orders where ShipCity = '"+city+"' and ShipCountry = '"+country+"'" , con)
    con.close()
    if df.empty:
        return('No Results')
    else:
        return df
    

    




