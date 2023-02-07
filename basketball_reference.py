# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 20:20:33 2023

@author: jwken
"""

import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
        
        url = requests.get ("https://www.sports-reference.com/cbb/seasons/2023-school-stats.html")
        
        soup = BeautifulSoup(url.text, 'html.parser')
        

        teamStatTable = soup.find("div", attrs = {'id':'div_basic_school_stats'}).find("table").find("tbody")
        
        teamRows = teamStatTable.find_all("tr")
        
        
        for row in teamRows[:399]:
            
            if((row.has_attr("class"))):
                x = 4
            else:
                
                columns = row.find_all("td")
                name = columns[0].text
                wins = int (columns[2].text)
                losses = int (columns[3].text)
               #SOS = int (columns[6].text)
                ptsFor = int (columns[17].text)
                ptsAllowed = int (columns[18].text)
                three_pct = float (columns[26].text)
                offensive_rebounds = int (columns[30].text)
                turnovers = int (columns[35].text)
                
            
                stats = [name, wins, losses, ptsFor, ptsAllowed, three_pct, turnovers, offensive_rebounds]
                print (stats)
                
            
         
           
           