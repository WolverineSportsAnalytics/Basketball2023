# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 19:38:40 2023
@author: djmcd
"""

import requests
from bs4 import BeautifulSoup
import mysql.connector
import time


# Returns a list of the link ID for each men's basketball team on basketball reference
def getTeamLinks():
    links = []
    url = requests.get("https://www.sports-reference.com/cbb/schools/")
    soup = BeautifulSoup(url.text, "html.parser")
    main = soup.find("div", attrs={"id": "all_NCAAM_schools"})
    section = main.find("div", attrs={"id": "div_NCAAM_schools"})
    table = section.find("tbody").find_all("tr")

    for row in table:
        nameRow = str(row.find("td", attrs={"data-stat": "school_name"}))
        trimmedRow = nameRow[50:]
        for i in range(len(trimmedRow)):
            if (trimmedRow[i] == ">"):
                link = trimmedRow[:i - 1]
                links.append(link)
                break

    return links


# Requires a year to start from and a year to end from
# Returns a list of all year link IDs between those two dates (both dates inclusive)
def getYearLinks(start_year, current_year):
    links = []
    for i in range((current_year - start_year) + 1):
        year = start_year + i
        yearLink = str(year) + ".html"
        links.append(yearLink)

    return links


# Requires two lists, one of team link stubs and one of year link stubs
# Returns a list of every combination of team and year link stubs
def getLinkEndings(team_links, year_links):
    links = []
    for team_link in team_links:
        for year_link in year_links:
            link = team_link + year_link
            links.append(link)

    return links


# Requires a list of valid link_endings
# Returns a list of full links
def getLinks(link_endings):
    links = []
    for link_ending in link_endings:
        link = "https://www.sports-reference.com" + link_ending
        links.append(link)

    return links


# Requires a valid link to a year page for a college team on basketball reference
# Returns the stats from the first table (all rows) in a single list, with the team as the first item
def readPage(link):
    url = requests.get(link)
    soup = BeautifulSoup(url.text, "html.parser")
    team = "NO_NAME"

    # Get team name from the link
    trimmedLink = link[45:]
    for i in range(len(trimmedLink)):
        if (trimmedLink[i] == "/"):
            team = trimmedLink[:i]
            break
    team = formatTeamName(team)

    try:
        test = soup.find("div", attrs={"id": "all_per_game_team"})
        test.find("div", attrs={"id": "div_season-total_per_game"})
    except:
        print("Could not find the page for: " + str(link))
        return

    per_game_section = soup.find("div", attrs={"id": "all_per_game_team"})
    per_game_container = per_game_section.find("div", attrs={"id": "div_season-total_per_game"})
    per_game_table = per_game_container.find("table")
    per_game_body = per_game_table.find("tbody")
    per_game_rows = per_game_body.find_all("tr")
    per_game_stats = per_game_rows[0]
    per_game_ranks = per_game_rows[1]
    per_game_opp_stats = per_game_rows[2]
    per_game_opp_ranks = per_game_rows[3]
    rows = [per_game_stats, per_game_ranks, per_game_opp_stats, per_game_opp_ranks]

    lists = []
    lists.append(team)
    for i in range(len(rows)):
        columns = rows[i].find_all("td")
        fg = columns[2].text
        fgA = columns[3].text
        fgPCT = columns[4].text
        twopt = columns[5].text
        twoptA = columns[6].text
        twoptPCT = columns[7].text
        threept = columns[8].text
        threeptA = columns[9].text
        threeptPCT = columns[10].text
        ft = columns[11].text
        ftA = columns[12].text
        ftPCT = columns[13].text
        orb = columns[14].text
        drb = columns[15].text
        trb = columns[16].text
        ast = columns[17].text
        stl = columns[18].text
        blk = columns[19].text
        tov = columns[20].text
        pf = columns[21].text
        pts = columns[22].text

        if (i % 2):
            fg = trimRank(fg)
            fgA = trimRank(fgA)
            fgPCT = trimRank(fgPCT)
            twopt = trimRank(twopt)
            twoptA = trimRank(twoptA)
            twoptPCT = trimRank(twoptPCT)
            threept = trimRank(threept)
            threeptA = trimRank(threeptA)
            threeptPCT = trimRank(threeptPCT)
            ft = trimRank(ft)
            ftA = trimRank(ftA)
            ftPCT = trimRank(ftPCT)
            orb = trimRank(orb)
            drb = trimRank(drb)
            trb = trimRank(trb)
            ast = trimRank(ast)
            stl = trimRank(stl)
            blk = trimRank(blk)
            tov = trimRank(tov)
            pf = trimRank(pf)
            pts = trimRank(pts)

        lists.append(fg)
        lists.append(fgA)
        lists.append(fgPCT)
        lists.append(twopt)
        lists.append(twoptA)
        lists.append(twoptPCT)
        lists.append(threept)
        lists.append(threeptA)
        lists.append(threeptPCT)
        lists.append(ft)
        lists.append(ftA)
        lists.append(ftPCT)
        lists.append(orb)
        lists.append(drb)
        lists.append(trb)
        lists.append(ast)
        lists.append(stl)
        lists.append(blk)
        lists.append(tov)
        lists.append(pf)
        lists.append(pts)
    return lists


# Requires a rank in the format of a number with a two letter suffix
# Returns just the number
def trimRank(rank):
    return rank[:-2]


# Requires a valid table name in the March-Madness-2023 database with correct columns
# and a list of valid links to sports reference pages for basketball teams
# Adds the stats for each team to the specified table in the database
def fillTable(table, links):
    cnx = mysql.connector.connect(user="wsa",
                                  host="34.68.250.121",
                                  database="March-Madness-2023",
                                  password="LeBron>MJ!")
    cursor = cnx.cursor(buffered=True)

    tableExists = False
    cursor.execute("SHOW TABLES")
    for x in cursor:
        if (table in x):
            tableExists = True

    if (tableExists):
        for link in links:
            print("Attempting to add data for: " + str(link))

            data = readPage(link)

            if ((data is None) == False):
                print("Adding: " + str(data[0]))

                types = list(range(85))
                for index, stat in enumerate(data):
                    if stat in ('', None):
                        types[index] = "NULL"
                        data[index] = "NULL"
                    else:
                        types[index] = '%s'
                        data[index] = "'" + data[index] + "'"

                statement = "INSERT INTO " + str(
                    table) + '''(Team, FG, FGA, FGpct, 2PT, 2PTA, 2PTpct, 3PT, 3PTA, 3PTpct, FT, FTA, FTpct, ORB, DRB, TRB, AST, STL, BLK, TOV, PF, PTS, FG_RANK, FGA_RANK, FGpct_RANK, 2PT_RANK, 2PTA_RANK, 2PTpct_RANK, 3PT_RANK, 3PTA_RANK, 3PTpct_RANK, FT_RANK, FTA_RANK, FTpct_RANK, ORB_RANK, DRB_RANK, TRB_RANK, AST_RANK, STL_RANK, BLK_RANK, TOV_RANK, PF_RANK, PTS_RANK, OPP_FG, OPP_FGA, OPP_FGpct, OPP_2PT, OPP_2PTA, OPP_2PTpct, OPP_3PT, OPP_3PTA, OPP_3PTpct, OPP_FT, OPP_FTA, OPP_FTpct, OPP_ORB, OPP_DRB, OPP_TRB, OPP_AST, OPP_STL, OPP_BLK, OPP_TOV, OPP_PF, OPP_PTS, OPP_FG_RANK, OPP_FGA_RANK, OPP_FGpct_RANK, OPP_2PT_RANK, OPP_2PTA_RANK, OPP_2PTpct_RANK, OPP_3PT_RANK, OPP_3PTA_RANK, OPP_3PTpct_RANK, OPP_FT_RANK, OPP_FTA_RANK, OPP_FTpct_RANK, OPP_ORB_RANK, OPP_DRB_RANK, OPP_TRB_RANK, OPP_AST_RANK, OPP_STL_RANK, OPP_BLK_RANK, OPP_TOV_RANK, OPP_PF_RANK, OPP_PTS_RANK) VALUES ( ''' + data[0] +''', ''' + data[1] +''', ''' + data[2]+''', ''' + data[3]+''', ''' + data[4]+''', ''' + data[5]+''', ''' + data[6]+''', ''' + data[7]+''', ''' + data[8]+''', ''' + data[9]+''', ''' + data[10]+''', ''' + data[11]+''', ''' + data[12]+''', ''' + data[13]+''', ''' + data[14]+''', ''' + data[15]+''', ''' + data[16]+''', ''' + data[17]+''', ''' + data[18]+''', ''' + data[19]+''', ''' + data[20]+''', ''' + data[21]+''', ''' + data[22]+''', ''' + data[23]+''', ''' + data[24]+''', ''' + data[25]+''', ''' + data[26]+''', ''' + data[27]+''', ''' + data[28]+''', ''' + data[29]+''', ''' + data[30]+''', ''' + data[31]+''', ''' + data[32]+''', ''' + data[33]+''', ''' + data[34]+''', ''' + data[35]+''', ''' + data[36]+''', ''' + data[37]+''', ''' + data[38]+''', ''' + data[39]+''', ''' + data[40]+''', ''' + data[41]+''', ''' + data[42]+''', ''' + data[43]+''', ''' + data[44]+''', ''' + data[45]+''', ''' + data[46]+''', ''' + data[47]+''', ''' + data[48]+''', ''' + data[49]+''', ''' + data[50]+''', ''' + data[51]+''', ''' + data[52]+''', ''' + data[53]+''', ''' + data[54]+''', ''' + data[55]+''', ''' + data[56]+''', ''' + data[57]+''', ''' + data[58]+''', ''' + data[59]+''', ''' + data[60]+''', ''' + data[61]+''', ''' + data[62]+''', ''' + data[63]+''', ''' + data[64]+''', ''' + data[65]+''', ''' + data[66]+''', ''' + data[67]+''', ''' + data[68]+''', ''' + data[69]+''', ''' + data[70]+''', ''' + data[71]+''', ''' + data[72] +''', ''' + data[73]+''', ''' + data[74]+''', ''' + data[75]+''', ''' + data[76]+''', ''' + data[77]+''', ''' + data[78]+''', ''' + data[79]+''', ''' + data[80]+''', ''' + data[81]+''', ''' + data[82]+''', ''' + data[83]+''', ''' + data[84]+ ''')'''
                cursor.execute(statement)
                cnx.commit()
                print("Added: " + str(data[0]))


                print("Pausing the program for 4 seconds to avoid Cloudflare protection")
                time.sleep(4)

        cnx.close()
    else:
        print("Table not recognized. Check formatting.")


# Requires a team name in the format created in ReadPage (from a Basketball Reference link)
# Returns the name of the team with the formatting desired for our tables
def formatTeamName(team):
    team = team.capitalize()
    teamList = list(team)
    for i in range(len(teamList)):
        # Tests to ensure length hasn't changed and i hasn't gone out of range.
        try:
            teamList[i]
        except:
            break

        # Searches for a dash, replaces it with a space
        if (teamList[i] == "-"):
            teamList[i] = " "
            try:
                teamList[i + 1] = teamList[i + 1].capitalize()
            except:
                print("Unexpected team name (contained dash as the final char.)")
                break

            # Searches for "state" after a dash, replace it with "St."
            try:
                if ("".join(teamList[i + 1:i + 6]) == "State"):
                    teamList[i + 3] = "."
                    del teamList[i + 4:i + 6]
            except:
                pass

    team = "".join(teamList)
    return team


# Requires a valid year (int) and a valid table name in the WSA SQL database (string)
# Modifies: fills that table with the data of every school from that year
def scrapeYear(year, table):
    years = getYearLinks(year, year)
    teams = getTeamLinks()
    endings = getLinkEndings(teams, years)
    link_list = getLinks(endings)
    fillTable(table, link_list)

# Please don't run this with a year that has already been filled -- it will duplicate the table.
# To fill a table, create the table in the SQL database (if it hasn't already been created) using
# the formatting of the other tables ([YEAR]_Stats)
# Then just run the command scrapeYear([YEAR], [TABLE NAME]) and let it run for 20-30 minutes.
# scrapeYear(2009, "2009_Stats")
