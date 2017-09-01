from nfl_stats import *
from points import *
from send_email import *
import time

start = time.time()

print "It has begun."

season = 2016
week_season = range(1,18)

run_stats_import(week_season, season)
import_done_time = time.time()
print "Import Process Complete in " + str(round(import_done_time - start,2)) + " seconds."

#time.sleep(1)

run_points(season)
process_points_time = time.time()
print "Stats Processing in " + str(round(process_points_time - import_done_time,2)) + " seconds."

#time.sleep(1)

send_email(week_season, season)
send_email_time = time.time()
print "Send Email in " + str(round(send_email_time - process_points_time,2)) + " seconds."
print
print "Script Complete in " + str(round(time.time() - start,2)) + "seconds."