import psycopg2
import datetime
import time
import smtplib
import ConfigParser
import xlsxwriter
import mimetypes
from optparse import OptionParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import Encoders
import pandas
import csv
import pandas as pd
#from html import *

file = "settings/points_system.txt"
    #print file
f = open(file,"r")
point_set = eval(f.read())


def documents(weeks, year):

     def right(s, amount):
             return s[-amount:]

     year_string = str(year)+right(str(year+1),2)
     data_set = []


     read_file = 'data/points/players_{year}.csv'.format(year=year_string)
     with open(read_file, "rb") as read_csv:

          reader = csv.reader(read_csv)
          headers = reader.next()
          #next(reader)
          #
          for line in reader:
               #print line
               data_set.append(line)

     #print headers
     read_csv.close()

     df = pd.DataFrame(data_set).convert_objects(convert_numeric=True)
     df = df[df[0] <= max(weeks)]
     result = df.groupby([1]).sum()
     result = list(map(tuple, result.itertuples(index=True)))

     workbook_name = 'data/standings/{year}_week_{week}_standings.xlsx'.format(year=year, week=max(weeks))
     #frame_writer = pd.ExcelWriter(workbook_name, engine='xlsxwriter')
     workbook = xlsxwriter.Workbook(workbook_name)

     number = 1

     xrow= 0
     xcol = 0

     worksheet_name = 'Standings'
     worksheet = workbook.add_worksheet(worksheet_name)
     integer = workbook.add_format()
     integer.set_num_format('#,##0.00')
     integer.set_align('center')
     integer.set_bold()
     integer_header_format = worksheet.set_column('C:W', 12, integer)
     player = workbook.add_format()
     player.set_align('center')
     player.set_bold()
     player_header_format = worksheet.set_column('B:B', 10, player)
     rank = workbook.add_format()
     rank.set_align('center')
     rank.set_bold()
     rank_header_format = worksheet.set_column('A:A', 5, rank)


     #df.to_excel(frame_writer, sheet_name=worksheet)

     worksheet.write(xrow, xcol, "Rank", rank_header_format)
     worksheet.write(xrow, xcol + 1, "Owner", player_header_format)
     worksheet.write(xrow, xcol + 2, "Blocks", integer_header_format)
     worksheet.write(xrow, xcol + 3, "TB",integer_header_format)
     worksheet.write(xrow, xcol + 4, "FC",integer_header_format)
     worksheet.write(xrow, xcol + 5, "OB",integer_header_format)
     worksheet.write(xrow, xcol + 6, "50+",integer_header_format)
     worksheet.write(xrow, xcol + 7, "60+",integer_header_format)
     worksheet.write(xrow, xcol + 8, "70+",integer_header_format)
     worksheet.write(xrow, xcol + 9, "Under 20",integer_header_format)
     worksheet.write(xrow, xcol + 10, "Under 10",integer_header_format)
     worksheet.write(xrow, xcol + 11, "Under 5",integer_header_format)
     worksheet.write(xrow, xcol + 12, "1 Yd Line",integer_header_format)
     worksheet.write(xrow, xcol + 13, "Punt Avg",integer_header_format)
     worksheet.write(xrow, xcol + 14, "Return Avg",integer_header_format)
     worksheet.write(xrow, xcol + 15, "Holds",integer_header_format)
     worksheet.write(xrow, xcol + 16, "Misses",integer_header_format)
     worksheet.write(xrow, xcol + 17, "First Downs", integer_header_format)
     worksheet.write(xrow, xcol + 18, "Touchdowns", integer_header_format)
     worksheet.write(xrow, xcol + 19, "Fumbles", integer_header_format)
     worksheet.write(xrow, xcol + 20, "Interceptions", integer_header_format)
     worksheet.write(xrow, xcol + 21, "Conduct", integer_header_format)
     worksheet.write(xrow, xcol + 22, "Total Points",integer_header_format)
     worksheet.freeze_panes(1,2)

     xrow = 1
     result = sorted(result, key=lambda x: x[22], reverse=True)
     rank_order = 1
     for i in result:
          if i[0] <> "Free Agent":
               row_integer = workbook.add_format()
               row_integer.set_num_format('#,##0.00')
               row_integer.set_align('center')
               row_player = workbook.add_format()
               row_player.set_align('center')
               row_rank = workbook.add_format()
               row_rank.set_align('center')
               worksheet.write(xrow, xcol, rank_order, row_rank)
               worksheet.write(xrow, xcol + 1, i[0],row_player)
               worksheet.write(xrow, xcol + 2, i[2],row_integer)
               worksheet.write(xrow, xcol + 3, i[3],row_integer)
               worksheet.write(xrow, xcol + 4, i[4],row_integer)
               worksheet.write(xrow, xcol + 5, i[5],row_integer)
               worksheet.write(xrow, xcol + 6, i[6],row_integer)
               worksheet.write(xrow, xcol + 7, i[7],row_integer)
               worksheet.write(xrow, xcol + 8, i[8],row_integer)
               worksheet.write(xrow, xcol + 9, i[9],row_integer)
               worksheet.write(xrow, xcol + 10, i[10],row_integer)
               worksheet.write(xrow, xcol + 11, i[11],row_integer)
               worksheet.write(xrow, xcol + 12, i[12],row_integer)
               worksheet.write(xrow, xcol + 13, i[13],row_integer)
               worksheet.write(xrow, xcol + 14, i[14],row_integer)
               worksheet.write(xrow, xcol + 15, i[15],row_integer)
               worksheet.write(xrow, xcol + 16, i[16],row_integer)
               worksheet.write(xrow, xcol + 17, i[17],row_integer)
               worksheet.write(xrow, xcol + 18, i[18], row_integer)
               worksheet.write(xrow, xcol + 19, i[19], row_integer)
               worksheet.write(xrow, xcol + 20, i[20], row_integer)
               worksheet.write(xrow, xcol + 21, i[21], row_integer)
               worksheet.write(xrow, xcol + 22, i[22], row_integer)


               xrow = xrow + 1
               rank_order = rank_order + 1
          else:
               continue

     worksheet_name = 'Points System'
     xrow = 0
     worksheet = workbook.add_worksheet(worksheet_name)
     points_format = worksheet.set_column('A:B', 13, rank)
     row_rank = workbook.add_format()
     row_rank.set_align('center')
     worksheet.write(xrow, xcol, "Type", points_format)
     worksheet.write(xrow, xcol + 1, "Points", points_format)
     xrow = 1
     for i in sorted(point_set):
          worksheet.write(xrow, xcol, i, row_rank)
          worksheet.write(xrow, xcol + 1, point_set[i], row_rank)
          xrow = 1 + xrow

     worksheet_name = 'Weekly Player Points'
     worksheet = workbook.add_worksheet(worksheet_name)
     xrow = 0
     result = df
     result = list(map(tuple, result.itertuples(index=True)))
     #print result

     result = sorted(result, key=lambda x: (x[25]), reverse=True)
     #print result[0][25]

     stats_integer_header_format = worksheet.set_column('E:Z', 11, integer)
     stats_rank_header_format = worksheet.set_column('A:A', 7, rank)
     stats_owner_header_format = worksheet.set_column('B:C', 11, rank)
     stats_team_header_format = worksheet.set_column('D:D', 7, rank)
     worksheet.write(xrow, xcol, "Week", stats_rank_header_format)
     worksheet.write(xrow, xcol + 1, "Owner", stats_owner_header_format)
     worksheet.write(xrow, xcol + 2, "Punter", stats_owner_header_format)
     worksheet.write(xrow, xcol + 3, "Team", stats_team_header_format)
     worksheet.write(xrow, xcol + 4, "Blocks", stats_integer_header_format)
     worksheet.write(xrow, xcol + 5, "TB", stats_integer_header_format)
     worksheet.write(xrow, xcol + 6, "FC", stats_integer_header_format)
     worksheet.write(xrow, xcol + 7, "OB", stats_integer_header_format)
     worksheet.write(xrow, xcol + 8, "50+", stats_integer_header_format)
     worksheet.write(xrow, xcol + 9, "60+", stats_integer_header_format)
     worksheet.write(xrow, xcol + 10, "70+", stats_integer_header_format)
     worksheet.write(xrow, xcol + 11, "Under 20", stats_integer_header_format)
     worksheet.write(xrow, xcol + 12, "Under 10", stats_integer_header_format)
     worksheet.write(xrow, xcol + 13, "Under 5", stats_integer_header_format)
     worksheet.write(xrow, xcol + 14, "1 Yd Line", stats_integer_header_format)
     worksheet.write(xrow, xcol + 15, "Punt Avg.", stats_integer_header_format)
     worksheet.write(xrow, xcol + 16, "Return Avg.", stats_integer_header_format)
     worksheet.write(xrow, xcol + 17, "Holds", stats_integer_header_format)
     worksheet.write(xrow, xcol + 18, "Misses", stats_integer_header_format)
     worksheet.write(xrow, xcol + 19, "First Downs", stats_integer_header_format)
     worksheet.write(xrow, xcol + 20, "Touchdowns", stats_integer_header_format)
     worksheet.write(xrow, xcol + 21, "Fumbles", stats_integer_header_format)
     worksheet.write(xrow, xcol + 22, "Interceptions", stats_integer_header_format)
     worksheet.write(xrow, xcol + 23, "Conduct", stats_integer_header_format)
     worksheet.write(xrow, xcol + 24, "Total Points", stats_integer_header_format)
     worksheet.freeze_panes(1, 4)
     xrow = 1
     for a in result:

          #print a
          row_float = workbook.add_format()
          row_float.set_num_format('#,##0.00')
          row_float.set_align('center')
          row_integer = workbook.add_format()
          row_integer.set_num_format('#,##0')
          row_integer.set_align('center')
          row_player = workbook.add_format()
          row_player.set_align('center')
          row_rank = workbook.add_format()
          row_rank.set_align('center')
          worksheet.write(xrow, xcol, int(a[1]), row_rank)
          worksheet.write(xrow, xcol + 1, a[2], row_player)
          worksheet.write(xrow, xcol + 2, a[3], row_player)
          worksheet.write(xrow, xcol + 3, a[4], row_player)
          worksheet.write(xrow, xcol + 4, a[5], row_float)
          worksheet.write(xrow, xcol + 5, a[6], row_float)
          worksheet.write(xrow, xcol + 6, a[7], row_float)
          worksheet.write(xrow, xcol + 7, a[8], row_float)
          worksheet.write(xrow, xcol + 8, a[9], row_float)
          worksheet.write(xrow, xcol + 9, a[10], row_float)
          worksheet.write(xrow, xcol + 10, a[11], row_float)
          worksheet.write(xrow, xcol + 11, a[12], row_float)
          worksheet.write(xrow, xcol + 12, a[13], row_float)
          worksheet.write(xrow, xcol + 13, a[14], row_float)
          worksheet.write(xrow, xcol + 14, a[15], row_float)
          worksheet.write(xrow, xcol + 15, a[16], row_float)
          worksheet.write(xrow, xcol + 16, a[17], row_float)
          worksheet.write(xrow, xcol + 17, a[18], row_float)
          worksheet.write(xrow, xcol + 18, a[19], row_float)
          worksheet.write(xrow, xcol + 19, a[20], row_float)
          worksheet.write(xrow, xcol + 20, a[21], row_float)
          worksheet.write(xrow, xcol + 21, a[22], row_float)
          worksheet.write(xrow, xcol + 22, a[23], row_float)
          worksheet.write(xrow, xcol + 23, a[24], row_float)
          worksheet.write(xrow, xcol + 24, a[25], row_float)
          xrow = xrow + 1

     for week in weeks:
          xrow = 0
          worksheet_name = 'Week {week}'.format(week=str(week)) if week < 15 else 'QuarterFinals' if week == 15 else 'SemiFinals' if week == 16 else 'Finals' if week == 17 else 'Broken'
          worksheet = workbook.add_worksheet(worksheet_name)
          week_integer_header_format = worksheet.set_column('E:Z', 10, integer)
          week_rank_header_format = worksheet.set_column('A:A', 5, rank)
          week_owner_header_format = worksheet.set_column('B:C', 11, rank)
          week_team_header_format = worksheet.set_column('D:D', 7, rank)
          worksheet.write(xrow, xcol, "Rank", week_rank_header_format)
          worksheet.write(xrow, xcol + 1, headers[1], week_owner_header_format)
          worksheet.write(xrow, xcol + 2, headers[2], week_owner_header_format)
          worksheet.write(xrow, xcol + 3, headers[3], week_team_header_format)
          worksheet.write(xrow, xcol + 4, headers[4], week_integer_header_format)
          worksheet.write(xrow, xcol + 5, "TB", week_integer_header_format)
          worksheet.write(xrow, xcol + 6, "FC", week_integer_header_format)
          worksheet.write(xrow, xcol + 7, "OB", week_integer_header_format)
          worksheet.write(xrow, xcol + 8, headers[8], week_integer_header_format)
          worksheet.write(xrow, xcol + 9, headers[9], week_integer_header_format)
          worksheet.write(xrow, xcol + 10, headers[10], week_integer_header_format)
          worksheet.write(xrow, xcol + 11, headers[11], week_integer_header_format)
          worksheet.write(xrow, xcol + 12, headers[12], week_integer_header_format)
          worksheet.write(xrow, xcol + 13, headers[13], week_integer_header_format)
          worksheet.write(xrow, xcol + 14, headers[14], week_integer_header_format)
          worksheet.write(xrow, xcol + 15, headers[15], week_integer_header_format)
          worksheet.write(xrow, xcol + 16, headers[16], week_integer_header_format)
          worksheet.write(xrow, xcol + 17, headers[17], week_integer_header_format)
          worksheet.write(xrow, xcol + 18, headers[18], week_integer_header_format)
          worksheet.write(xrow, xcol + 19, headers[19], week_integer_header_format)
          worksheet.write(xrow, xcol + 20, headers[20], week_integer_header_format)
          worksheet.write(xrow, xcol + 21, headers[21], week_integer_header_format)
          worksheet.write(xrow, xcol + 22, headers[22], week_integer_header_format)
          worksheet.write(xrow, xcol + 23, headers[23], week_integer_header_format)
          worksheet.write(xrow, xcol + 24, headers[24], week_integer_header_format)


          worksheet.freeze_panes(1,4)
          xrow=1
          rank_num = 1
          data_set = sorted(data_set, key=lambda x: float(x[24]), reverse=True)
          for line in data_set:

               if int(line[0]) == int(week):
                    #print line
                    Week = line[0]
                    Owner = line[1]
                    Punter = line[2]
                    Team = line[3]
                    Blocks  = line[4]
                    Touchbacks = line[5]
                    Fair_Catches = line[6]
                    Out_of_Bounds = line[7]
                    Fifty = line[8]
                    Sixty = line[9]
                    Seventy = line[10]
                    Under_20 = line[11]
                    Under_10 = line[12]
                    Under_5 = line[13]
                    Yd_Line = line[14]
                    Punt_Avg = line[15]
                    Return_Avg = line[16]
                    Holds = line[17]
                    Misses = line[18]
                    First_Downs = line[19]
                    Touchdowns = line[20]
                    Fumbles = line[21]
                    Interceptions = line[22]
                    Conduct = line[23]
                    Total_Points = line[24]
                    row_integer = workbook.add_format()
                    row_integer.set_num_format('#,##0.00')
                    row_integer.set_align('center')
                    row_player = workbook.add_format()
                    row_player.set_align('center')
                    row_rank = workbook.add_format()
                    row_rank.set_align('center')

                    worksheet.write(xrow, xcol, rank_num, row_rank)
                    worksheet.write(xrow, xcol + 1, Owner, row_player)
                    worksheet.write(xrow, xcol + 2, Punter, row_player)
                    worksheet.write(xrow, xcol + 3, Team, row_player)
                    worksheet.write(xrow, xcol + 4, float(Blocks), row_integer)
                    worksheet.write(xrow, xcol + 5, float(Touchbacks), row_integer)
                    worksheet.write(xrow, xcol + 6, float(Fair_Catches), row_integer)
                    worksheet.write(xrow, xcol + 7, float(Out_of_Bounds), row_integer)
                    worksheet.write(xrow, xcol + 8, float(Fifty), row_integer)
                    worksheet.write(xrow, xcol + 9, float(Sixty), row_integer)
                    worksheet.write(xrow, xcol + 10, float(Seventy), row_integer)
                    worksheet.write(xrow, xcol + 11, float(Under_20), row_integer)
                    worksheet.write(xrow, xcol + 12, float(Under_10), row_integer)
                    worksheet.write(xrow, xcol + 13, float(Under_5), row_integer)
                    worksheet.write(xrow, xcol + 14, float(Yd_Line), row_integer)
                    worksheet.write(xrow, xcol + 15, float(Punt_Avg), row_integer)
                    worksheet.write(xrow, xcol + 16, float(Return_Avg), row_integer)
                    worksheet.write(xrow, xcol + 17, float(Holds), row_integer)
                    worksheet.write(xrow, xcol + 18, float(Misses), row_integer)
                    worksheet.write(xrow, xcol + 19, float(First_Downs), row_integer)
                    worksheet.write(xrow, xcol + 20, float(Touchdowns), row_integer)
                    worksheet.write(xrow, xcol + 21, float(Fumbles), row_integer)
                    worksheet.write(xrow, xcol + 22, float(Interceptions), row_integer)
                    worksheet.write(xrow, xcol + 23, float(Conduct), row_integer)
                    worksheet.write(xrow, xcol + 24, float(Total_Points), row_integer)
                    xrow = xrow + 1
                    rank_num = rank_num + 1
     workbook.close()


documents(range(1, 18), 2017)