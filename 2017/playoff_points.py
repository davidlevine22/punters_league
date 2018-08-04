import nflgame
import time
import re
import csv
import pandas as pd

def run_playoff_points(weeks, year):


    def Punt_Avg(punt_yard, punt):
        try:
            points = (float(punt_yard)/float(punt)-45)*.1
            return points
        except:
            points = 0
            return points

    def Return_Avg(return_yard, returns):
        try:
            points = -(float(return_yard)/float(returns)-9)*.10
            return points
        except:
            points  = 0
            return points

    def right(s, amount):
        return s[-amount:]

    #year = 2016
    year_string = str(year)+right(str(year+1),2)
    data_set = []
    read_file = 'data/points/season_{year}.csv'.format(year=year_string)
    with open(read_file, "rb") as read_csv:

        reader = csv.reader(read_csv)
        headers = reader.next()
        #next(reader)
        #
        for line in reader:
            data_set.append(line)

    read_csv.close()

    df = pd.DataFrame(data_set).convert_objects(convert_numeric=True)
    df = df[df[0] <= max(weeks)]
    result = df.groupby([1]).sum()
    result = list(map(tuple, result.itertuples(index=True)))
    result = sorted(result, key=lambda x: x[17], reverse=True)

    season_standing = []
    rankings = 1

    for player in result:
        if player[0] <> 'Free Agent':
            #print player
            season_standing.append(player[0])

    ranking_dictionary = dict(enumerate(season_standing, start = 1))
    ranking_dictionary = dict((v,k) for k,v in ranking_dictionary.iteritems())

    playoffs = [15, 16, 17]
    #print playoffs

    def playoff_stats(regular_season_week):
        playoff_week = 'quarterfinals' if regular_season_week == playoffs[0] else 'semifinals' if regular_season_week == playoffs[1] else 'finals' if regular_season_week == playoffs[2] else 'broken'
        read_file = 'data/season/season_{year}.csv'.format(year=year_string)
        with open(read_file, "rb") as read_csv:
            write_file = 'data/points/{playoff_week}_{year}.csv'.format(playoff_week= playoff_week, year=year_string)
            with open(write_file, "wb") as write_csv:
                Block_Points = -2
                Touchbacks_Points = .4
                Fair_Catches_Points = .25
                Out_of_Bounds_Points = .15
                Fifty_Points = 1
                Sixty_Points = .75
                Seventy_Points = .5
                Under_20_Points = 1
                Under_10_Points = .75
                Under_5_Points = .5
                Yd_Line_Points = .25
                holds_points = .1
                miss_points = -.5
                #Returns_Avg_Points = 0

                outputWriter = csv.writer(write_csv, delimiter=',')

                header_row = list()
                header_row.append("Week")
                header_row.append("Seed")
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
                header_row.append("Bonus Points")
                header_row.append("Total Points")

                outputWriter.writerow(header_row)

                reader = csv.reader(read_csv)
                next(reader)
                for line in reader:

                    #print line
                    try:
                        week = line[0]
                        owner = line[1]
                        seed = ranking_dictionary.get(str(owner), "Broken")
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
                        holds = line[19]
                        misses = line[20]
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
                                       int(misses)*miss_points

                        bonus_points = 4 if seed == 1 and regular_season_week == 15 else 3 if seed == 2 and regular_season_week == 15 else 2 if seed == 3 and regular_season_week == 15 else 1 if seed == 4 and regular_season_week == 15 else 0
                        total_points = total_points + bonus_points
                        #print week

                        if week == str(regular_season_week) and owner <> 'Free Agent':
                            csv_data = list()
                            #Convert date to string
                            csv_data.append(week)
                            csv_data.append(seed)
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
                            csv_data.append(int(holds)*holds_points)
                            csv_data.append(int(misses)*miss_points)
                            csv_data.append(bonus_points)
                            csv_data.append(total_points)
                            outputWriter.writerow(csv_data)

                    except:
                        continue




                #Punt_Avg_Points = Punt_Avg(200,40)
        write_csv.close
        read_csv.close

    for i in playoffs:
        if i < max(weeks):
            playoff_stats(i)

run_playoff_points([1,18], 2017)