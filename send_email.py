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

def right(s, amount):
        return s[-amount:]

#Create Email Connection & Body
SERVER = "smtplib.SMTP('smtp.gmail.com:587')"
#distro = open("exec_distro.txt", "r+")
#mailList = [i.strip() for i in distro.readlines()]


FROM = 'davidlevine22@gmail.com'
TO  = ['davidlevine@iheartmedia.com']
message = 'Why,Oh why!'
username = 'davidlevine22'
password = 'trxcldwjalgbiefc'


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

SUBJECT = "Test"

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
year = 2016
year_string = str(year)+right(str(year+1),2)
data_set = []


read_file = 'data/points/season_{year}.csv'.format(year=year_string)
with open(read_file, "rb") as read_csv:

     reader = csv.reader(read_csv)
     headers = reader.next()
     next(reader)
     #
     for line in reader:
          data_set.append(line)

read_csv.close()

df = pd.DataFrame(data_set).convert_objects(convert_numeric=True)
#print df
result = df.groupby([1]).sum()

print result

#print data_set

workbook_name = 'data/{year}_standings.xlsx'.format(year=year_string)
workbook = xlsxwriter.Workbook(workbook_name)

number = 1

xrow= 0
xcol = 0
#workbook.close()

worksheet_name = 'Season'
worksheet = workbook.add_worksheet(worksheet_name)

weeks = [1,2]

for week in weeks:
     xrow = 0
     worksheet_name = 'Week_{week}'.format(week=str(week))
     worksheet = workbook.add_worksheet(worksheet_name)
     worksheet.write(xrow, xcol, headers[0])
     worksheet.write(xrow, xcol + 1, headers[1])
     worksheet.write(xrow, xcol + 2, headers[2])
     worksheet.write(xrow, xcol + 3, headers[3])
     worksheet.write(xrow, xcol + 4, headers[4])
     worksheet.write(xrow, xcol + 5, headers[5])
     worksheet.write(xrow, xcol + 6, headers[6])
     worksheet.write(xrow, xcol + 7, headers[7])
     worksheet.write(xrow, xcol + 8, headers[8])
     worksheet.write(xrow, xcol + 9, headers[9])
     worksheet.write(xrow, xcol + 10, headers[10])
     worksheet.write(xrow, xcol + 11, headers[11])
     worksheet.write(xrow, xcol + 12, headers[12])
     worksheet.write(xrow, xcol + 13, headers[13])
     worksheet.write(xrow, xcol + 14, headers[14])
     worksheet.write(xrow, xcol + 15, headers[15])
     worksheet.write(xrow, xcol + 16, headers[16])
     worksheet.write(xrow, xcol + 17, headers[17])
     xrow=1
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
               Total_Points = line[17]

               worksheet.write(xrow, xcol, Week)
               worksheet.write(xrow, xcol + 1, Owner)
               worksheet.write(xrow, xcol + 2, Punter)
               worksheet.write(xrow, xcol + 3, Team)
               worksheet.write(xrow, xcol + 4, Blocks)
               worksheet.write(xrow, xcol + 5, Touchbacks)
               worksheet.write(xrow, xcol + 6, Fair_Catches)
               worksheet.write(xrow, xcol + 7, Out_of_Bounds)
               worksheet.write(xrow, xcol + 8, Fifty)
               worksheet.write(xrow, xcol + 9, Sixty)
               worksheet.write(xrow, xcol + 10, Seventy)
               worksheet.write(xrow, xcol + 11, Under_20)
               worksheet.write(xrow, xcol + 12, Under_10)
               worksheet.write(xrow, xcol + 13, Under_5)
               worksheet.write(xrow, xcol + 14, Yd_Line)
               worksheet.write(xrow, xcol + 15, Punt_Avg)
               worksheet.write(xrow, xcol + 16, Return_Avg)
               worksheet.write(xrow, xcol + 17, Total_Points)
               xrow = xrow + 1


workbook.close()

fileToSend = workbook_name
fp = open(fileToSend, "rb")
attachment_file = MIMEBase('application', "octet-stream")
attachment_file.set_payload(fp.read())
encoders.encode_base64(attachment_file)
fp.close()
attachment_file.add_header("Content-Disposition", "attachment", filename=fileToSend)
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
#server.sendmail(FROM, TO, msgRoot.as_string())

server.quit()


print "Email Sent"
