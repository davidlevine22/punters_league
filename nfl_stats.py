import nflgame
import time
import re
import csv

def run_stats_import(week_number, year):


    def left(s, amount):
        return s[:amount]

    def right(s, amount):
        return s[-amount:]

    def mid(s, offset, amount):
        return s[offset:offset+amount]


    #season = [2]
    #season = range(1,3)

    #year = 2016
    year_string = str(year)+right(str(year+1),2)

    #print("Week, Owner, Punter, Team, Punts, Punt Yards, Blocks, Touchbacks, Fair Catches, Out-of_Bounds, 50+, 60+, 70+, Under 20, Under 10, Under 5, 1 Yd Line, Returns, Return Yards")
    open_file = 'data/season/season_{year}.csv'.format(year=year_string)
    with open(open_file, "wb") as data_csv:
        outputWriter = csv.writer(data_csv, delimiter=',')
        header_row = list()
        header_row.append("Week")
        header_row.append("Owner")
        header_row.append("Punter")
        header_row.append("Team")
        header_row.append("Punts")
        header_row.append("Punt Yards")
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
        header_row.append("Returns")
        header_row.append("Return Yards")
        outputWriter.writerow(header_row)

        for week in week_number:
            try:
                file = "roster/week{week_number}.txt".format(week_number=week)
                #print file
                f = open(file,"r")
                owner_set = eval(f.read())
                owner_set = dict((v,k) for k,v in owner_set.iteritems())

            except:
                owner_set = dict()

            games = nflgame.games(year, week=week)
            stats = nflgame.combine_max_stats(games)
            plays = nflgame.combine_plays(games)

            for player in stats.punting():

                punt_name = player
                team = player.team
                punt_yards = player.punting_yds
                punt_blocks = player.punting_blk
                punt_under_20s = player.punting_i20
                punt_count = player.punting_tot
                punt_touch_back = player.punting_touchback
                punt_downs = player.puntret_downed
                punts_under_20 = 0
                punts_under_10 = 0
                punts_under_5 = 0
                punts_under_2 = 0
                out_of_bounds = 0
                fair_catch = 0
                punts_over_50 = 0
                punts_over_60 = 0
                punts_over_70 = 0
                returns = 0

                plays = nflgame.combine_plays(games)
                #play = ''

                return_list = []

                for play in plays:
                    if str(punt_name) in str(play) and "punts" in str(play) and "No Play" not in str(play):
                        #description = play
                        #print play
                        punts_character = str(play).find("punts")
                        punts_string = str(play)[int(punts_character):]
                        comma_character = punts_string.find(",")
                        yard_line = punts_string[:int(comma_character)]
                        yard_line = right(yard_line,2)
                        try:
                            yard_line = (re.findall('\d+', yard_line))#[0]
                            yard_line = int(yard_line[0])
                            touch_back = 0
                        except:
                            yard_line = 0
                            touch_back = 1
                        #print yard_line
                        return_yards =  int(play.puntret_yds)
                        return_list.append(return_yards)
                        punt_length = int(play.punting_yds)
                        #print punt_length
                        if yard_line + return_yards <20 and yard_line + return_yards > 0:
                            punts_under_20 = punts_under_20 + 1
                        if yard_line + return_yards <10 and yard_line + return_yards > 0:
                            punts_under_10 = punts_under_10 + 1
                        if yard_line + return_yards <5 and yard_line + return_yards > 0:
                            punts_under_5 = punts_under_5 + 1
                        if yard_line + return_yards <2 and yard_line + return_yards > 0:
                            punts_under_2 = punts_under_2 + 1
                        if "out of bounds" in str(punts_string):
                            out_of_bounds = out_of_bounds + 1
                        if "fair catch" in str(punts_string):
                            fair_catch = fair_catch + 1
                        if punt_length >= 50:
                            punts_over_50 = punts_over_50 = punts_over_50 + 1
                        if punt_length >= 60:
                            punts_over_60 = punts_over_60 = punts_over_60 + 1
                        if punt_length >= 70:
                            punts_over_70 = punts_over_70 = punts_over_70 + 1
                        if "out of bounds" not in str(punts_string) and "fair catch" not in str(punts_string) \
                            and touch_back == 0 and "downed" not in str(play):
                            returns = returns + 1

                    else:
                        continue

                #print return_list
                total_return_yards = sum(return_list)

                owner = owner_set.get(str(player), "Free Agent")
                #print owner

                time.sleep(1)

                # print(str(week) +", " + str(owner) +", "   + str(punt_name) +", " +  \
                #      str(team) + ", " + str(punt_count) +", " + str(punt_yards) +", " + \
                #      str(punt_blocks) +", " + str(punt_touch_back) +", " + str(fair_catch) +", " + \
                #      str(out_of_bounds) +", " + str(punts_over_50) +", " + str(punts_over_60) +", " + \
                #      str(punts_over_70) +", " + str(punt_under_20s) +", " + str(punts_under_10) +", " + \
                #      str(punts_under_5) +", " + str(punts_under_2) +", " + str(returns) +", " + \
                #      str(total_return_yards))

                csv_data = list()
                #Convert date to string
                csv_data.append(week)
                csv_data.append(str(owner))
                csv_data.append(str(punt_name))
                csv_data.append(str(team))
                csv_data.append(punt_count)
                csv_data.append(punt_yards)
                csv_data.append(punt_blocks)
                csv_data.append(punt_touch_back)
                csv_data.append(fair_catch)
                csv_data.append(out_of_bounds)
                csv_data.append(punts_over_50)
                csv_data.append(punts_over_60)
                csv_data.append(punts_over_70)
                csv_data.append(punt_under_20s)
                csv_data.append(punts_under_10)
                csv_data.append(punts_under_5)
                csv_data.append(punts_under_2)
                csv_data.append(returns)
                csv_data.append(total_return_yards)

                outputWriter.writerow(csv_data)

    data_csv.close