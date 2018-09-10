import time
import re
import csv
import os
import pandas as pd


def right(s, amount):
        return s[-amount:]

def players(weeks, year):
    year_string = str(year)+right(str(year+1),2)
    read_file = 'data/points/punters_{year}.csv'.format(year=year_string)
    #print df
    write_file = 'data/points/players_{year}.csv'.format(year=year_string)
    with open(write_file, "wb") as write_csv:
        outputWriter = csv.writer(write_csv, delimiter=',')

        header_row = list()
        header_row.append("Week")
        header_row.append("Owner")
        header_row.append("Punter")
        header_row.append("Team")
        header_row.append("Blocks")
        header_row.append("Touchbacks")
        header_row.append("Fair Catches")
        header_row.append("Out-of_Bounds")
        header_row.append("50+")
        header_row.append("60+")
        header_row.append("70+")
        header_row.append("Under 20")
        header_row.append("Under 10")
        header_row.append("Under 5")
        header_row.append("1 Yd Line")
        header_row.append("Punt Avg")
        header_row.append("Return Avg")
        header_row.append("Holds")
        header_row.append("Misses")
        header_row.append("First Downs")
        header_row.append("Touchdowns")
        header_row.append("Fumbles")
        header_row.append("Interceptions")
        header_row.append("Conduct")
        header_row.append("Total Points")
        outputWriter.writerow(header_row)


        for i in weeks:
            df = pd.read_csv(read_file)
            df = df[df['Week'] == i]
            df = df.values.tolist()

            try:
                file = "roster/{year_number}/week{week_number}.txt".format(week_number=i, year_number = year)
                #print file
                f = open(file,"r")
                owner_set = eval(f.read())
                #print owner_set
                owner_set = dict((v,k) for k,v in owner_set.iteritems())


            except:
                owner_set = dict()
                #print owner_set

            for line in df:

                week = line[0]
                punter = line[1]
                team = line[2]
                blocks = line[3]
                touchbacks = line[4]
                fair_catches = line[5]
                out_of_bounds = line[6]
                fifty = line[7]
                sixty = line[8]
                seventy = line[9]
                under_20 = line[10]
                under_10 = line[11]
                under_5 = line[12]
                under_2 = line[13]
                punt_avg = line[14]
                return_avg = line[15]
                holds = line[16]
                misses = line[17]
                first_downs = line[18]
                touchdowns = line[19]
                fumbles = line[20]
                interceptions = line[21]
                conduct = line[22]
                total_points = line[23]

                owner = owner_set.get(str(punter), "Free Agent")
                #print owner
                csv_data = list()
                #Convert date to string
                csv_data.append(week)
                csv_data.append(owner)
                csv_data.append(punter)
                csv_data.append(team)
                csv_data.append(blocks)
                csv_data.append(touchbacks)
                csv_data.append(fair_catches)
                csv_data.append(out_of_bounds)
                csv_data.append(fifty)
                csv_data.append(sixty)
                csv_data.append(seventy)
                csv_data.append(under_20)
                csv_data.append(under_10)
                csv_data.append(under_5)
                csv_data.append(under_2)
                csv_data.append(punt_avg)
                csv_data.append(return_avg)
                csv_data.append(holds)
                csv_data.append(misses)
                csv_data.append(first_downs)
                csv_data.append(touchdowns)
                csv_data.append(fumbles)
                csv_data.append(interceptions)
                csv_data.append(conduct)
                csv_data.append(total_points)

                outputWriter.writerow(csv_data)

            #print owner



    write_csv.close
    #read_csv.close


week_season = range(1,2)
players(week_season, 2018)