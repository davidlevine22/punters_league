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

     worksheet_name = 'Weekly Stats'
     worksheet = workbook.add_worksheet(worksheet_name)
     xrow = 0
     result = df
     result = list(map(tuple, result.itertuples(index=True)))
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
     #worksheet.freeze_panes(1, 4)
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
     workbook.close()


documents([1,2,3,4], 2017)