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
#from html import *


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
     workbook_name = 'data/standings/{year}_week_{week}_standings.xlsx'.format(year=year, week=max(weeks))
     #frame_writer = pd.ExcelWriter(workbook_name, engine='xlsxwriter')

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

send_email([1], 2018, "Hey")