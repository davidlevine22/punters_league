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
from email import encoders
import pandas
import csv
import pandas as pd
from html import *


def send_email(weeks, year, message):

     def right(s, amount):
             return s[-amount:]

     #Create Email Connection & Body
     SERVER = "smtplib.SMTP('smtp.gmail.com:587')"
     distro_list = "distro/{year}/league_distro.txt".format(year=year)
     distro = open(distro_list, "r+")
     mailList = [i.strip() for i in distro.readlines()]


     FROM = 'davidlevine22@gmail.com'
     #TO = mailList
     TO = ['davidlevine@iheartmedia.com']
     username = 'davidlevine22'
     password = open("password.txt", "r+")
     password = [i.strip() for i in password.readlines()]
     password = ''.join(password)

     # Create message container.
     msgRoot = MIMEMultipart('related')
     html = message

     parser = OptionParser()
     #parser.add_option("-f", "--from", dest="sender", help="sender email address", default="iHR BI")
     parser.add_option("-t", "--to", dest="recipient", help="recipient email address")
     parser.add_option("-s", "--subject", dest="subject", help="email subject", default="Data Metrics Report Preview")
     parser.add_option("-i", "--image", dest="image", help="image attachment", default=False)
     parser.add_option("-p", "--pdf", dest="pdf", help="pdf attachment", default=False)
     (options, args) = parser.parse_args()

     SUBJECT = "Punters League {year_number} - Week {week_number} Update".format(year_number = year, week_number = max(weeks))

     text_body = ''

     TEXT = text_body
     #print text_body

     # Prepare actual message
     message = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\

     %s
     """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

     message_b = """%s""" % (TEXT)
     msgHtml = MIMEText(html, 'html')
     msgHtml.add_header('Content-Disposition', 'inline')
     msgRoot.attach(msgHtml)

     #Excel
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
               #print line
               data_set.append(line)

     read_csv.close()

     df = pd.DataFrame(data_set).convert_objects(convert_numeric=True)
     df = df[df[0] <= max(weeks)]
     result = df.groupby([1]).sum()
     result = list(map(tuple, result.itertuples(index=True)))

     workbook_name = 'data/weekly_update/{year}/{year}_week_{week}_standings.xlsx'.format(year=year, week=max(weeks))
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
     integer_header_format = worksheet.set_column('C:R', 10, integer)
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
     worksheet.write(xrow, xcol + 17, "Total Points",integer_header_format)
     worksheet.freeze_panes(1,2)

     xrow = 1
     result = sorted(result, key=lambda x: x[17], reverse=True)
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
               xrow = xrow + 1
               rank_order = rank_order + 1
          else:
               continue

     open_file = 'data/season/season_{year}.csv'.format(year=year_string)
     with open(open_file, "rb") as data_csv:
          writer = csv.reader(data_csv)
          #headers = reader.next()
          next(writer)

     #open_csv.close()
          worksheet_name = 'Weekly Stats'
          worksheet = workbook.add_worksheet(worksheet_name)
          xrow = 0
          xrow = 0
          #
          stats_integer_header_format = worksheet.set_column('E:U', 10, integer)
          stats_rank_header_format = worksheet.set_column('A:A', 7, rank)
          stats_owner_header_format = worksheet.set_column('B:C', 11, rank)
          stats_team_header_format = worksheet.set_column('D:D', 7, rank)
          worksheet.write(xrow, xcol, "Week", stats_rank_header_format)
          worksheet.write(xrow, xcol + 1, "Owner", stats_owner_header_format)
          worksheet.write(xrow, xcol+2, "Punter", stats_owner_header_format)
          worksheet.write(xrow, xcol+3, "Team", stats_team_header_format)
          worksheet.write(xrow, xcol+4, "Punts", stats_team_header_format)
          worksheet.write(xrow, xcol+5, "Yards", stats_team_header_format)
          worksheet.write(xrow, xcol+6, "Blocks", stats_integer_header_format)
          worksheet.write(xrow, xcol+7, "TB", stats_integer_header_format)
          worksheet.write(xrow, xcol+8, "FC", stats_integer_header_format)
          worksheet.write(xrow, xcol+9, "OB", stats_integer_header_format)
          worksheet.write(xrow, xcol+10, "50+", stats_integer_header_format)
          worksheet.write(xrow, xcol+11, "60+", stats_integer_header_format)
          worksheet.write(xrow, xcol+12, "70+", stats_integer_header_format)
          worksheet.write(xrow, xcol+13, "Under 20", stats_integer_header_format)
          worksheet.write(xrow, xcol+14, "Under 10", stats_integer_header_format)
          worksheet.write(xrow, xcol+15, "Under 5", stats_integer_header_format)
          worksheet.write(xrow, xcol+16, "1 Yd Line", stats_integer_header_format)
          worksheet.write(xrow, xcol+17, "Returns", stats_integer_header_format)
          worksheet.write(xrow, xcol+18, "RY", stats_integer_header_format)
          worksheet.write(xrow, xcol+19, "Holds", stats_integer_header_format)
          worksheet.write(xrow, xcol+20, "Misses", stats_integer_header_format)
          worksheet.freeze_panes(1,3)
          xrow = 1
          new_data_set = []
          for a in writer:
               #print a
               row_integer = workbook.add_format()
               row_integer.set_num_format('#,##0')
               row_integer.set_align('center')
               row_player = workbook.add_format()
               row_player.set_align('center')
               row_rank = workbook.add_format()
               row_rank.set_align('center')
               worksheet.write(xrow, xcol, int(a[0]), row_rank)
               worksheet.write(xrow, xcol + 1, a[1], row_player)
               worksheet.write(xrow, xcol+2, a[2], row_player)
               worksheet.write(xrow, xcol+3, a[3], row_player)
               worksheet.write(xrow, xcol+4, int(a[4]), row_integer)
               worksheet.write(xrow, xcol+5, int(a[5]), row_integer)
               worksheet.write(xrow, xcol+6, int(a[6]), row_integer)
               worksheet.write(xrow, xcol+7, int(a[7]), row_integer)
               worksheet.write(xrow, xcol+8, int(a[8]), row_integer)
               worksheet.write(xrow, xcol+9, int(a[9]), row_integer)
               worksheet.write(xrow, xcol+10, int(a[10]), row_integer)
               worksheet.write(xrow, xcol+11, int(a[11]), row_integer)
               worksheet.write(xrow, xcol+12, int(a[12]), row_integer)
               worksheet.write(xrow, xcol+13, int(a[13]), row_integer)
               worksheet.write(xrow, xcol+14, int(a[14]), row_integer)
               worksheet.write(xrow, xcol+15, int(a[15]), row_integer)
               worksheet.write(xrow, xcol+16, int(a[16]), row_integer)
               worksheet.write(xrow, xcol+17, int(a[17]), row_integer)
               worksheet.write(xrow, xcol+18, int(a[18]), row_integer)
               worksheet.write(xrow, xcol+19, int(a[19]), row_integer)
               worksheet.write(xrow, xcol+20, int(a[20]), row_integer)
               xrow = xrow + 1
               #print a
               new_data_set.append(a)

    #read_csv.close()
          #print data_set

          data_frame = pd.DataFrame(new_data_set).convert_objects(convert_numeric=True)
          data_frame = data_frame[data_frame[0] <= max(weeks)]
          data_frame[3].replace(["JAC"],["JAX"],inplace=True)
          #result_base = list(map(tuple, df.itertuples(index=True)))
          #print data_frame[data_frame[3] == "B.Nortman",]
          data_result = data_frame.groupby([2,3], as_index=False).sum()
          data_result = list(map(tuple, data_result.itertuples(index=True)))
          #print data_result

          worksheet_name = 'Punter Stats'
          worksheet = workbook.add_worksheet(worksheet_name)
          xrow = 0
          xrow = 0
          punter_integer_header_format = worksheet.set_column('C:S', 10, integer)
          punter_owner_header_format = worksheet.set_column('A:A', 11, rank)
          punter_team_header_format = worksheet.set_column('B:B', 7, rank)
          worksheet.write(xrow, xcol, "Punter", punter_owner_header_format)
          worksheet.write(xrow, xcol+1, "Team", punter_team_header_format)
          worksheet.write(xrow, xcol+2, "Punts", punter_integer_header_format)
          worksheet.write(xrow, xcol+3, "Yards", punter_integer_header_format)
          worksheet.write(xrow, xcol+4, "Blocks", punter_integer_header_format)
          worksheet.write(xrow, xcol+5, "TB", punter_integer_header_format)
          worksheet.write(xrow, xcol+6, "FC", punter_integer_header_format)
          worksheet.write(xrow, xcol+7, "OB", punter_integer_header_format)
          worksheet.write(xrow, xcol+8, "50+", punter_integer_header_format)
          worksheet.write(xrow, xcol+9, "60+", punter_integer_header_format)
          worksheet.write(xrow, xcol+10, "70+", punter_integer_header_format)
          worksheet.write(xrow, xcol+11, "Under 20", punter_integer_header_format)
          worksheet.write(xrow, xcol+12, "Under 10", punter_integer_header_format)
          worksheet.write(xrow, xcol+13, "Under 5", punter_integer_header_format)
          worksheet.write(xrow, xcol+14, "1 Yd Line", punter_integer_header_format)
          worksheet.write(xrow, xcol+15, "Returns", punter_integer_header_format)
          worksheet.write(xrow, xcol+16, "RY", punter_integer_header_format)
          worksheet.write(xrow, xcol+17, "Holds", punter_integer_header_format)
          worksheet.write(xrow, xcol+18, "Misses", punter_integer_header_format)

          worksheet.freeze_panes(1,2)

          xrow = 1
          data_result = sorted(data_result, key=lambda x: x[1])
          for a in data_result:
               #print a
               punter_row_integer = workbook.add_format()
               punter_row_integer.set_num_format('#,##0')
               punter_row_integer.set_align('center')
               punter_row_player = workbook.add_format()
               punter_row_player.set_align('center')
               punter_row_rank = workbook.add_format()
               punter_row_rank.set_align('center')
               worksheet.write(xrow, xcol, a[1], punter_row_rank)
               worksheet.write(xrow, xcol + 1, a[2], punter_row_player)
               worksheet.write(xrow, xcol+2, int(a[4]), punter_row_player)
               worksheet.write(xrow, xcol+3, int(a[5]), punter_row_player)
               worksheet.write(xrow, xcol+4, int(a[6]), punter_row_integer)
               worksheet.write(xrow, xcol+5, int(a[7]), punter_row_integer)
               worksheet.write(xrow, xcol+6, int(a[8]), punter_row_integer)
               worksheet.write(xrow, xcol+7, int(a[9]), punter_row_integer)
               worksheet.write(xrow, xcol+8, int(a[10]), punter_row_integer)
               worksheet.write(xrow, xcol+9, int(a[11]), punter_row_integer)
               worksheet.write(xrow, xcol+10, int(a[12]), punter_row_integer)
               worksheet.write(xrow, xcol+11, int(a[13]), punter_row_integer)
               worksheet.write(xrow, xcol+12, int(a[14]), punter_row_integer)
               worksheet.write(xrow, xcol+13, int(a[15]), punter_row_integer)
               worksheet.write(xrow, xcol+14, int(a[16]), punter_row_integer)
               worksheet.write(xrow, xcol+15, int(a[17]), punter_row_integer)
               worksheet.write(xrow, xcol+16, int(a[18]), punter_row_integer)
               worksheet.write(xrow, xcol+17, int(a[19]), punter_row_integer)
               worksheet.write(xrow, xcol+18, int(a[20]), punter_row_integer)
               xrow = xrow + 1

     #weeks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
     #print weeks
     #print range(1,17)

     for week in weeks:
          xrow = 0
          worksheet_name = 'Week {week}'.format(week=str(week))
          worksheet = workbook.add_worksheet(worksheet_name)
          week_integer_header_format = worksheet.set_column('E:T', 10, integer)
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
          worksheet.freeze_panes(1,3)
          xrow=1
          rank_num = 1
          data_set = sorted(data_set, key=lambda x: float(x[19]), reverse=True)
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
                    Total_Points = line[19]
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
                    worksheet.write(xrow, xcol + 19, float(Total_Points), row_integer)
                    xrow = xrow + 1
                    rank_num = rank_num + 1


     workbook.close()

     fileToSend = workbook_name
     fp = open(fileToSend, "rb")
     attachment_file = MIMEBase('application', "octet-stream")
     attachment_file.set_payload(fp.read())
     encoders.encode_base64(attachment_file)
     fp.close()
     attachment_file.add_header("Content-Disposition", "attachment", filename="this_week_in_punting.xlsx")
     msgRoot.attach(attachment_file)

     # make up message
     msgRoot['Subject'] = SUBJECT
     msgRoot['From'] = FROM
     #msgRoot['To'] = "ihr-analytics@iheartmedia.com"

     # sending

     server = smtplib.SMTP('smtp.gmail.com:587')
     server.ehlo()
     server.starttls()
     server.login(username,password)
     server.sendmail(FROM, TO, msgRoot.as_string())

     server.quit()

