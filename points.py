import nflgame
import time
import re
import csv

def run_points(year):


    def Punt_Avg(punt_yard, punt):
        try:
            points = (float(punt_yard)/float(punt)-45)*.1
            return points
        except:
            points = 0
            return points

    def Return_Avg(return_yard, returns):
        try:
            points = (float(return_yard)/float(returns)-9)*.10
            return points
        except:
            points  = 0
            return points

    def right(s, amount):
        return s[-amount:]

    #year = 2016
    year_string = str(year)+right(str(year+1),2)

    read_file = 'data/season/season_{year}.csv'.format(year=year_string)
    with open(read_file, "rb") as read_csv:
        write_file = 'data/points/season_{year}.csv'.format(year=year_string)
        with open(write_file, "wb") as write_csv:
            Block_Points = -2
            Touchbacks_Points = .4
            Fair_Catches_Points = .25
            Out_of_Bounds_Points = .15
            Fifty_Points = 1
            Sixty_Points = 1.25
            Seventy_Points = 1.5
            Under_20_Points = 1
            Under_10_Points = .75
            Under_5_Points = .5
            Yd_Line_Points = .25
            #Returns_Avg_Points = 0

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
            header_row.append("Total Points")

            outputWriter.writerow(header_row)

            reader = csv.reader(read_csv)
            next(reader)
            for line in reader:

                week = line[0]
                owner = line[1]
                punter = line[2]
                team = line[3]
                punts = line[4]
                punt_yards = line[5]
                blocks = line[6]
                touchbacks = line[7]
                fair_catches = line[8]
                out_of_bounds = line[9]
                fifty = line[10]
                sixty = line[11]
                seventy = line[12]
                under_20 = line[13]
                under_10 = line[14]
                under_5 = line[15]
                under_2 = line[16]
                returns = line[17]
                return_yards = line[18]
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
                               Return_Avg(int(return_yards), int(returns))

                csv_data = list()
                #Convert date to string
                csv_data.append(week)
                csv_data.append(owner)
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
                csv_data.append(total_points)

                outputWriter.writerow(csv_data)




            #Punt_Avg_Points = Punt_Avg(200,40)
    write_csv.close
    read_csv.close