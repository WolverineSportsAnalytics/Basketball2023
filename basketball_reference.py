#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 11:35:51 2023

@author: kushal
"""

import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
        
        url = requests.get ("https://www.sports-reference.com/cbb/seasons/2023-school-stats.html")
        
        soup = BeautifulSoup(url.text, 'html.parser')
        

        teamStatTable = soup.find("div", attrs = {'id':'div_basic_school_stats'}).find("table").find("tbody")
        
        teamRows = teamStatTable.find_all("tr")
        
        
        for row in teamRows[:20]:
            if((row.has_attr("class"))):
                x=5
            else:
            
               columns = row.find_all("td")
               name = columns[0].text
               wins = int (columns[2].text)
               losses = int (columns[3].text)
              #SOS = int (columns[6].text)
               ptsFor = int (columns[17].text)
               ptsAllowed = int (columns[18].text)
               blocks = int (columns[34].text)
               turnovers = int(columns[35].text)
               three_point_pct = float (columns[26].text)
               offensive_reb = int(columns[30].text)
               
               
               stats = [name, wins, losses, ptsFor, ptsAllowed, blocks, turnovers, three_point_pct, offensive_reb]
          
               print (stats)
          
      
           
      
        
      
        
      
