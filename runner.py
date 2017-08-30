from nfl_stats import *
from points import *
from send_email import *
import time

season = 2016
week_season = range(1,17)

#run_stats_import(week_season, season)

#time.sleep(3)

run_points(season)

time.sleep(3)

send_email(week_season, season)