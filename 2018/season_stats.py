import nflgame
import time
import re
import csv

def run_stats_import(week, year):


    def left(s, amount):
        return s[:amount]

    def right(s, amount):
        return s[-amount:]

    def mid(s, offset, amount):
        return s[offset:offset+amount]

    year_string = str(year)+right(str(year+1),2)

    #print("Week, Owner, Punter, Team, Punts, Punt Yards, Blocks, Touchbacks, Fair Catches, Out-of_Bounds, 50+, 60+, 70+, Under 20, Under 10, Under 5, 1 Yd Line, Returns, Return Yards")
    open_file = 'data/season/season_{year}.csv'.format(year=year_string)
    with open(open_file, "wb") as data_csv:
        outputWriter = csv.writer(data_csv, delimiter=',')
        header_row = list()
        header_row.append("Week")
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
        header_row.append("Holds")
        header_row.append("Misses")
        header_row.append("First Downs")
        header_row.append("TD")
        header_row.append("Fumbles")
        header_row.append("Int")
        header_row.append("Conduct")
        outputWriter.writerow(header_row)

        for i in week:
            print("Week " + str(i))
            kind = 'REG' if i <= 17 else 'POST'
            woke = i if i <=17 else i-17
            #print kind
            #print woke
            games = nflgame.games(year, week=i)
            #print year
            stats = nflgame.combine_max_stats(games)
            plays = nflgame.combine_plays(games)

            #print games

            for player in stats.punting():
                    #print week

                punt_name = player
                team = player.team
                punt_yards = player.punting_yds
                punt_under_20s = player.punting_i20
                punt_blocks = player.punting_blk
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
                holds = 0
                misses = 0
                fumbles = 0
                interceptions = 0
                first_downs = 0
                passing_yds = 0
                passing_tds = 0
                rushing_yds = 0
                rushing_tds = 0
                touchdowns = 0
                conduct = 0

                for passing in stats.passing():
                    if passing == player:
                        passing_yds = passing.passing_yds
                        passing_tds = passing.passing_tds

                    else:
                        passing_yds = 0
                        passing_tds = 0

                    #print passing_yards
                    #print passing_tds

                for rushing in stats.rushing():
                    if rushing == player:
                        rushing_yds = rushing.rushing_yds
                        rushing_tds = rushing.rushing_tds
                    else:
                        rushing_yds = 0
                        rushing_tds = 0

                    #print rushing_yards
                    #print rushing_tds

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
                            punts_over_50 = punts_over_50 + 1
                        if punt_length >= 60:
                            punts_over_60 = punts_over_60 + 1
                        if punt_length >= 70:
                            punts_over_70 = punts_over_70 + 1
                        if "out of bounds" not in str(punts_string) and "fair catch" not in str(punts_string) \
                            and touch_back == 0 and "downed" not in str(play):
                            returns = returns + 1

                    elif str(punt_name) in str(play) and ("holder" in str(play) or "Holder" in str(play)) and "No Play" not in str(play):
                        #print play

                        if "is GOOD" in str(play):
                            holds = holds + 1

                        elif "is No Good" in str(play):
                            #print play
                            misses = misses + 1

                    elif str(punt_name) in str(play) and "Punt formation" in str(play) and "No Play" not in str(play) and "Delay of Game" not in str(play):
                        print str(play)
                        first_down_character = str(play).find("and")
                        remaining_string = str(play)[int(first_down_character)+4:]
                        parentheses_character = remaining_string.find(")")
                        remaining_string = remaining_string[:parentheses_character]
                        yards_remaining = remaining_string

                        yards_character = str(play).find("for ")
                        remaining_string = str(play)[int(yards_character)+4:]
                        yards_character = remaining_string.find("yards")
                        remaining_string = remaining_string[:yards_character]
                        yards_gained = remaining_string

                        #print yards_remaining
                        #print yards_gained

                        if "PENALTY" in str(play) and "Unsportsmanlike Conduct" in str(play):
                            if "PENALTY on {team}-{punter}".format(team = team, punter=punt_name) in str(play):
                                conduct=conduct+1
                        if "INTERCEPTED" in str(play):
                            interceptions=interceptions+1
                        elif "FUMBLES" in str(play):
                            if "{punter} FUMBLES".format(punter=punt_name) in str(play):
                                fumbles=fumbles+1
                        elif ("pass" in str(play) or "right end ran" in str(play) or "left end ran" in str(play) or "up the middle" in str(play)) and "INTERCEPTED" not in str(play) and "incomplete" not in str(play):
                            if int(yards_gained) >= int(yards_remaining) and yards_gained > 0:
                                first_downs = first_downs + 1
                            if "TOUCHDOWN" in str(play):
                                touchdowns = touchdowns + 1

                        #print conduct
                        #print interceptions
                        #print fumbles
                        #print first_downs
                        #print touchdowns




                    else:
                        continue

                    total_return_yards = sum(return_list)

                csv_data = list()
                #Convert date to string
                csv_data.append(i)
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
                csv_data.append(holds)
                csv_data.append(misses)
                csv_data.append(first_downs)
                csv_data.append(touchdowns)
                csv_data.append(fumbles)
                csv_data.append(interceptions)
                csv_data.append(conduct)


                outputWriter.writerow(csv_data)
    #
    data_csv.close


season = 2018
week_season = range(1,6)

run_stats_import(week_season, season)