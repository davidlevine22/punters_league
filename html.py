import webbrowser
import datetime
import csv
import pandas as pd


def html_body(week, year):

    f = open('table.html','w')
    def right(s, amount):
             return s[-amount:]
    year_string = str(year)+right(str(year+1),2)

    today = (datetime.datetime.now()).strftime('%Y-%m-%d')
    yesterday = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime('%A - %B %d, %Y')
    yesterday_month_value = (datetime.datetime.now() - datetime.timedelta(days = 1)).month
    yesterday_day_value = (datetime.datetime.now() - datetime.timedelta(days = 1)).day
    yesterday_year_value = (datetime.datetime.now() - datetime.timedelta(days = 1)).year
    yesterday_month= datetime.date(yesterday_year_value, yesterday_month_value, 1).strftime('%Y-%m-%d')

    read_file = 'data/points/season_{year}.csv'.format(year=year_string)
    data_set = []
    season_data_set = []
    with open(read_file, "rb") as read_csv:

        reader = csv.reader(read_csv)
        headers = reader.next()
        #next(reader)
              #
        for line in reader:
            #print line
            data_set.append(line)
            season_data_set.append(line)

    read_csv.close()

    #print data_set

    cid = 'punters_league_'+today
    df = pd.DataFrame(data_set).convert_objects(convert_numeric=True)
    season_df = pd.DataFrame(season_data_set).convert_objects(convert_numeric=True)
    df = df[df[0] == max(week)]
    season_df = season_df[season_df[0] <= max(week)]

    result = df.groupby([1,2], as_index=False).sum()
    result = list(map(tuple, result.itertuples(index=True)))
    result = sorted(result, key=lambda x: x[17], reverse=True)
    season_result = season_df.groupby([1], as_index=False).sum()
    season_result = list(map(tuple, season_result.itertuples(index=True)))
    season_result = sorted(season_result, key=lambda x: x[16], reverse=True)
    #print season_result
    #img = open("output\image.png", 'rb').read()
    weekly_standings = []
    weekly_rank = 1
    weekly_player_punt = []
    for a in result:
        player_punt = []
        player_list = []
        if a[1] <> "Free Agent":
            #a[]
            owner = a[1]
            punter = a[2]
            points = a[17]
            player_list.append(weekly_rank)
            player_list.append(owner)
            player_list.append(punter)
            player_list.append(points)
            weekly_standings.append(player_list)
            weekly_rank = weekly_rank + 1
            player_punt.append(owner)
            player_punt.append(punter)
            weekly_player_punt.append(player_punt)

    owner_player_dictionary = {key: value for (key, value) in weekly_player_punt}
    #print owner_player_dictionary
    season_standings = []
    season_rank = 1

    for b in season_result:
        season_player_list = []
        if b[1] <> "Free Agent":
            #a[]
            owner = b[1]
            #punter = b[2]
            points = b[16]
            season_player_list.append(season_rank)
            season_player_list.append(owner)
            season_player_list.append(owner_player_dictionary.get(owner, "Missing Label"))
            season_player_list.append(points)

            season_standings.append(season_player_list)
            season_rank = season_rank + 1



    def this_week(rank, variable):
        x = 0 if variable == "Rank" else 1 if variable == "Owner" else 2 if variable == "Punter" else 3 if variable == "Points" else 1
        for i in weekly_standings:
            if rank == i[0]:
                #print i
                if x == 3:
                    return round(i[x],1)
                else:
                    return i[x]

    def this_season(rank, variable):
        x = 0 if variable == "Rank" else 1 if variable == "Owner" else 2 if variable == "Punter" else 3 if variable == "Points" else 1
        for j in season_standings:
            if rank == j[0]:
                #print i
                if x == 3:
                    return round(j[x],1)
                else:
                    return j[x]

    message = """<html><head><style>
                    table {{
                            border-collapse: collapse;
                        }}
                    table, th, td {{
                        border: 2px solid black;
                    }}

                    If you are recieving this email, it's likely that other people question your life choices.

                    </style></head>
                    <body>
                        <table width="510" style="width=500px;">
                        <col width="510" style="width=500px;">
                        <tr><th bgcolor="#228B22" height = "50"><center><font color="white">Punters League {year_number} <br> Week {week_number} Update</font></center></th></tr>
                        </table>
                        <br>

                    <table width="510" style="width=510px;">
                        <tr><th bgcolor="black", colspan=4><center><font color="white">Week {week_number} Standings</font></center></th>
                        </tr>

                        <tr><td bgcolor="#191970" width="120" style="width=90px"><center><font color="white">Rank</font></center></td>
                            <td bgcolor="#191970" width="120" style="width=90px"><center><font color="white">Owner</font></center></td>
                            <td bgcolor="#191970" width="155" style="width=90px"><center><font color="white">Punter</font></center></td>
                            <td bgcolor="#191970" width="115" style="width=90px"><center><font color="white">Points</font></center></td>
                        </tr>

                        <tr>
                            <td><center>1</center></td>
                            <td><center>{owner_1}</center></td>
                            <td><center>{punter_1}</center></td>
                            <td><center>{points_1}</center></td>
                        </tr>
                        <tr bgcolor="#F0F0F0">
                            <td><center>2</center></td>
                            <td><center>{owner_2}</center></td>
                            <td><center>{punter_2}</center></td>
                            <td><center>{points_2}</center></td>
                        </tr>
                        <tr>
                            <td><center>3</center></td>
                            <td><center>{owner_3}</center></td>
                            <td><center>{punter_3}</center></td>
                            <td><center>{points_3}</center></td>
                        </tr>
                        <tr bgcolor="#F0F0F0">
                            <td><center>4</center></td>
                            <td><center>{owner_4}</center></td>
                            <td><center>{punter_4}</center></td>
                            <td><center>{points_4}</center></td>
                        </tr>
                        <tr>
                            <td><center>5</center></td>
                            <td><center>{owner_5}</center></td>
                            <td><center>{punter_5}</center></td>
                            <td><center>{points_5}</center></td>
                        </tr>
                        <tr bgcolor="#F0F0F0">
                            <td><center>6</center></td>
                            <td><center>{owner_6}</center></td>
                            <td><center>{punter_6}</center></td>
                            <td><center>{points_6}</center></td>
                        </tr>
                        <tr>
                            <td><center>7</center></td>
                            <td><center>{owner_7}</center></td>
                            <td><center>{punter_7}</center></td>
                            <td><center>{points_7}</center></td>
                        </tr>
                        <tr bgcolor="#F0F0F0">
                            <td><center>8</center></td>
                            <td><center>{owner_8}</center></td>
                            <td><center>{punter_8}</center></td>
                            <td><center>{points_8}</center></td>
                        </tr>
                        <tr>
                            <td><center>9</center></td>
                            <td><center>{owner_9}</center></td>
                            <td><center>{punter_9}</center></td>
                            <td><center>{points_9}</center></td>
                        </tr>
                        <tr bgcolor="#F0F0F0">
                            <td><center>10</center></td>
                            <td><center>{owner_10}</center></td>
                            <td><center>{punter_10}</center></td>
                            <td><center>{points_10}</center></td>
                        </tr>
                      </table>

                      <br>

                      <table width="510" style="width=510px;">
                        <tr><th bgcolor="black", colspan=4><center><font color="white">Season Standings</font></center></th>
                        </tr>

                        <tr><td bgcolor="#FF4500" width="120" style="width=90px"><center><font color="white">Rank</font></center></td>
                            <td bgcolor="#FF4500" width="120" style="width=90px"><center><font color="white">Owner</font></center></td>
                            <td bgcolor="#FF4500" width="155" style="width=90px"><center><font color="white">Current Punter</font></center></td>
                            <td bgcolor="#FF4500" width="115" style="width=90px"><center><font color="white">Points</font></center></td>
                        </tr>

                        <tr>
                            <td><center>1</center></td>
                            <td><center>{season_owner_1}</center></td>
                            <td><center>{season_punter_1}</center></td>
                            <td><center>{season_points_1}</center></td>
                        </tr>
                        <tr bgcolor="#F0F0F0">
                            <td><center>2</center></td>
                            <td><center>{season_owner_2}</center></td>
                            <td><center>{season_punter_2}</center></td>
                            <td><center>{season_points_2}</center></td>
                        </tr>
                        <tr>
                            <td><center>3</center></td>
                            <td><center>{season_owner_3}</center></td>
                            <td><center>{season_punter_3}</center></td>
                            <td><center>{season_points_3}</center></td>
                        </tr>
                        <tr bgcolor="#F0F0F0">
                            <td><center>4</center></td>
                            <td><center>{season_owner_4}</center></td>
                            <td><center>{season_punter_4}</center></td>
                            <td><center>{season_points_4}</center></td>
                        </tr>
                        <tr>
                            <td><center>5</center></td>
                            <td><center>{season_owner_5}</center></td>
                            <td><center>{season_punter_5}</center></td>
                            <td><center>{season_points_5}</center></td>
                        </tr>
                        <tr bgcolor="#F0F0F0">
                            <td><center>6</center></td>
                            <td><center>{season_owner_6}</center></td>
                            <td><center>{season_punter_6}</center></td>
                            <td><center>{season_points_6}</center></td>
                        </tr>
                        <tr>
                            <td><center>7</center></td>
                            <td><center>{season_owner_7}</center></td>
                            <td><center>{season_punter_7}</center></td>
                            <td><center>{season_points_7}</center></td>
                        </tr>
                        <tr bgcolor="#F0F0F0">
                            <td><center>8</center></td>
                            <td><center>{season_owner_8}</center></td>
                            <td><center>{season_punter_8}</center></td>
                            <td><center>{season_points_8}</center></td>
                        </tr>
                        <tr>
                            <td><center>9</center></td>
                            <td><center>{season_owner_9}</center></td>
                            <td><center>{season_punter_9}</center></td>
                            <td><center>{season_points_9}</center></td>
                        </tr>
                        <tr bgcolor="#F0F0F0">
                            <td><center>10</center></td>
                            <td><center>{season_owner_10}</center></td>
                            <td><center>{season_punter_10}</center></td>
                            <td><center>{season_points_10}</center></td>
                        </tr>
                      </table>

                    </body>
                    </html>
                    """.format(year_number=year,
                               week_number=max(week),
                               owner_1=this_week(1, "Owner"),
                               owner_2=this_week(2, "Owner"),
                               owner_3=this_week(3, "Owner"),
                               owner_4=this_week(4, "Owner"),
                               owner_5=this_week(5, "Owner"),
                               owner_6=this_week(6, "Owner"),
                               owner_7=this_week(7, "Owner"),
                               owner_8=this_week(8, "Owner"),
                               owner_9=this_week(9, "Owner"),
                               owner_10=this_week(10, "Owner"),
                               owner_11=this_week(11, "Owner"),
                               owner_12=this_week(12, "Owner"),
                               owner_13=this_week(13, "Owner"),
                               owner_14=this_week(14, "Owner"),
                               owner_15=this_week(15, "Owner"),
                               
                               punter_1=this_week(1, "Punter"),
                               punter_2=this_week(2, "Punter"),
                               punter_3=this_week(3, "Punter"),
                               punter_4=this_week(4, "Punter"),
                               punter_5=this_week(5, "Punter"),
                               punter_6=this_week(6, "Punter"),
                               punter_7=this_week(7, "Punter"),
                               punter_8=this_week(8, "Punter"),
                               punter_9=this_week(9, "Punter"),
                               punter_10=this_week(10, "Punter"),
                               punter_11=this_week(11, "Punter"),
                               punter_12=this_week(12, "Punter"),
                               punter_13=this_week(13, "Punter"),
                               punter_14=this_week(14, "Punter"),
                               punter_15=this_week(15, "Punter"),

                               points_1=this_week(1, "Points"),
                               points_2=this_week(2, "Points"),
                               points_3=this_week(3, "Points"),
                               points_4=this_week(4, "Points"),
                               points_5=this_week(5, "Points"),
                               points_6=this_week(6, "Points"),
                               points_7=this_week(7, "Points"),
                               points_8=this_week(8, "Points"),
                               points_9=this_week(9, "Points"),
                               points_10=this_week(10, "Points"),
                               points_11=this_week(11, "Points"),
                               points_12=this_week(12, "Points"),
                               points_13=this_week(13, "Points"),
                               points_14=this_week(14, "Points"),
                               points_15=this_week(15, "Points"),
                               
                               season_owner_1=this_season(1, "Owner"),
                               season_owner_2=this_season(2, "Owner"),
                               season_owner_3=this_season(3, "Owner"),
                               season_owner_4=this_season(4, "Owner"),
                               season_owner_5=this_season(5, "Owner"),
                               season_owner_6=this_season(6, "Owner"),
                               season_owner_7=this_season(7, "Owner"),
                               season_owner_8=this_season(8, "Owner"),
                               season_owner_9=this_season(9, "Owner"),
                               season_owner_10=this_season(10, "Owner"),
                               season_owner_11=this_season(11, "Owner"),
                               season_owner_12=this_season(12, "Owner"),
                               season_owner_13=this_season(13, "Owner"),
                               season_owner_14=this_season(14, "Owner"),
                               season_owner_15=this_season(15, "Owner"),
                               
                               season_punter_1=this_season(1, "Punter"),
                               season_punter_2=this_season(2, "Punter"),
                               season_punter_3=this_season(3, "Punter"),
                               season_punter_4=this_season(4, "Punter"),
                               season_punter_5=this_season(5, "Punter"),
                               season_punter_6=this_season(6, "Punter"),
                               season_punter_7=this_season(7, "Punter"),
                               season_punter_8=this_season(8, "Punter"),
                               season_punter_9=this_season(9, "Punter"),
                               season_punter_10=this_season(10, "Punter"),
                               season_punter_11=this_season(11, "Punter"),
                               season_punter_12=this_season(12, "Punter"),
                               season_punter_13=this_season(13, "Punter"),
                               season_punter_14=this_season(14, "Punter"),
                               season_punter_15=this_season(15, "Punter"),

                               season_points_1=this_season(1, "Points"),
                               season_points_2=this_season(2, "Points"),
                               season_points_3=this_season(3, "Points"),
                               season_points_4=this_season(4, "Points"),
                               season_points_5=this_season(5, "Points"),
                               season_points_6=this_season(6, "Points"),
                               season_points_7=this_season(7, "Points"),
                               season_points_8=this_season(8, "Points"),
                               season_points_9=this_season(9, "Points"),
                               season_points_10=this_season(10, "Points"),
                               season_points_11=this_season(11, "Points"),
                               season_points_12=this_season(12, "Points"),
                               season_points_13=this_season(13, "Points"),
                               season_points_14=this_season(14, "Points"),
                               season_points_15=this_season(15, "Points"),
                               )

    #print message

    f.write(message)
    f.close()
    return message
    #webbrowser.open_new_tab('table.html')

#
#html_body(range(1,5), 2016)