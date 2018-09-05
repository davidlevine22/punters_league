import time
import re
import csv
import os

file = "settings/points_system.txt"
    #print file
f = open(file,"r")
point_set = eval(f.read())
#print point_set
Block_Points = point_set['Block']
Touchbacks_Points = point_set['Touchback']
Fair_Catches_Points = point_set['Fair_Catch']
Out_of_Bounds_Points = point_set['Out_of_Bounds']
Fifty_Points = point_set['Fifty']
Sixty_Points = point_set['Sixty']
Seventy_Points = point_set['Seventy']
Under_20_Points = point_set['Under_20']
Under_10_Points = point_set['Under_10']
Under_5_Points = point_set['Under_5']
Yd_Line_Points = point_set['Yd_Line']
holds_points = point_set['Hold']
miss_points = point_set['Miss']
first_down_points = point_set['First_Down']
touch_down_points = point_set['Touch_Down']
fumbles_points = point_set['Fumbles']
interceptions_points = point_set['Interceptions']
conduct_points = point_set['Conduct']
punt_avg_points = point_set['PuntAvg']
return_avg_points = point_set['ReturnAvg']

def run_points(year):


    def Punt_Avg(punt_yard, punt):
        try:
            points = (float(punt_yard)/float(punt)-45)*punt_avg_points
            return points
        except:
            points = 0
            return points

    def Return_Avg(return_yard, returns):
        try:
            points = -(float(return_yard)/float(returns)-9)*return_avg_points
            return points
        except:
            points  = 0
            return points

    def right(s, amount):
        return s[-amount:]

    #year = 2016
    year_string = str(year)+right(str(year+1),2)
    owd = os.getcwd()
    os.chdir("..")
    os.chdir("..")
    #print os.path.abspath(os.curdir)

    read_file = os.path.abspath(os.curdir) + '/data/season/season_{year}.csv'.format(year=year_string)
    os.chdir(owd)
    #print os.path.abspath(os.curdir)
    with open(read_file, "rb") as read_csv:
        write_file = 'data/points/punters_{year}.csv'.format(year=year_string)
        with open(write_file, "wb") as write_csv:


            #Returns_Avg_Points = 0

            outputWriter = csv.writer(write_csv, delimiter=',')

            header_row = list()
            header_row.append("Week")
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

            reader = csv.reader(read_csv)
            next(reader)
            for line in reader:

                week = line[0]
                punter = line[1]
                team = line[2]
                punts = line[3]
                punt_yards = line[4]
                blocks = line[5]
                touchbacks = line[6]
                fair_catches = line[7]
                out_of_bounds = line[8]
                fifty = line[9]
                sixty = line[10]
                seventy = line[11]
                under_20 = line[12]
                under_10 = line[13]
                under_5 = line[14]
                under_2 = line[15]
                returns = line[16]
                return_yards = line[17]
                holds = line[18]
                misses = line[19]
                first_downs = line[20]
                touchdowns = line[21]
                fumbles = line[22]
                interceptions = line[23]
                conduct = line[24]

                #print line

                total_points = int(blocks)*Block_Points + \
                               int(touchbacks)*Touchbacks_Points + \
                               int(fair_catches)*Fair_Catches_Points + \
                               int(out_of_bounds)*Out_of_Bounds_Points + \
                               int(fifty)*Fifty_Points + \
                               int(sixty)*Sixty_Points + \
                               int(seventy)*Seventy_Points + \
                               int(under_20)*Under_20_Points + \
                               int(under_10)*Under_10_Points + \
                               int(under_5)*Under_5_Points + \
                               int(under_2)*Yd_Line_Points + \
                               Punt_Avg(int(punt_yards), int(punts)) + \
                               Return_Avg(int(return_yards), int(returns)) + \
                               int(holds)*holds_points + \
                               int(misses)*miss_points + \
                               int(first_downs)*first_down_points + \
                               int(touchdowns)*touch_down_points + \
                               int(fumbles)*fumbles_points + \
                               int(interceptions)*interceptions_points + \
                               int(conduct)*conduct_points

                csv_data = list()
                #Convert date to string
                csv_data.append(week)
                csv_data.append(punter)
                csv_data.append(team)
                csv_data.append(int(blocks)*Block_Points)
                csv_data.append(int(touchbacks)*Touchbacks_Points)
                csv_data.append(int(fair_catches)*Fair_Catches_Points)
                csv_data.append(int(out_of_bounds)*Out_of_Bounds_Points)
                csv_data.append(int(fifty)*Fifty_Points)
                csv_data.append(int(sixty)*Sixty_Points)
                csv_data.append(int(seventy)*Seventy_Points)
                csv_data.append(int(under_20)*Under_20_Points)
                csv_data.append(int(under_10)*Under_10_Points)
                csv_data.append(int(under_5)*Under_5_Points)
                csv_data.append(int(under_2)*Yd_Line_Points)
                csv_data.append(Punt_Avg(int(punt_yards), int(punts)))
                csv_data.append(Return_Avg(int(return_yards), int(returns)))
                csv_data.append(int(holds)*holds_points)
                csv_data.append(int(misses)*miss_points)
                csv_data.append(int(first_downs)*first_down_points)
                csv_data.append(int(touchdowns)*touch_down_points)
                csv_data.append(int(fumbles)*fumbles_points)
                csv_data.append(int(interceptions)*interceptions_points)
                csv_data.append(int(conduct)*conduct_points)

                csv_data.append(total_points)

                outputWriter.writerow(csv_data)




    write_csv.close
    read_csv.close


run_points(2017)