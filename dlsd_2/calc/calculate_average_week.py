import logging
import numpy as np
import pandas as pd
import datetime

LEN_DAY = 1440
LEN_WEEK = 7*LEN_DAY

def calculate_average_week_from_numpy_array(data):
	num_sensors = data.shape[1]
	num_weeks = data.shape[0]/LEN_WEEK
	data_avg = np.zeros([LEN_WEEK,num_sensors])
	logging.info("Data successfully prepared, finding average of %d weeks"%num_weeks)
	for time_in_week in range(0,LEN_WEEK):
	    # get indices of all rows corresponding to a certain time of the day/week 
	    idxs_for_time_n = [(LEN_WEEK*week_idx)+time_in_week for week_idx in range(0,int(num_weeks))]
	    # (eg monday 00:02) is equal to the average of every monday at 00:02
	    data_avg[time_in_week] = np.nanmean(data[idxs_for_time_n],0)
	return data_avg

def rearrange_week_to_start_at_time(week, time):
	week_starting_on_n = np.zeros([LEN_WEEK,week.shape[1]])
	week_starting_on_n[ 0 : (LEN_WEEK-time) , : ] = week[ time:LEN_WEEK , : ]
	week_starting_on_n[ (LEN_WEEK-time) : LEN_WEEK , : ] = week[0:time , : ]
	return week_starting_on_n

def rearrange_week_to_start_on_day_int(week, day_int):
	time = day_int * LEN_DAY
	return rearrange_week_to_start_at_time(week, time)

def rearrange_week_starting_to_start_on_monday_with_current_day_start_int(week, current_day_int):
	return rearrange_week_to_start_on_day_int(week,7-current_day_int)

def get_weekday_int_from_timestamp_string_with_format(time_stamp, time_format):
	first_datetime = datetime.datetime.strptime(time_stamp,time_format)
	return first_datetime.weekday()

def make_week_starting_on_monday_timestamps(weekday_begin_int=0, time_format='%Y-%m-%d %H:%M:%S'):
	the_datetime = get_real_datetime_starting_on_given_weekday_int(weekday_begin_int,time_format)
	datetimes = [the_datetime]
	while len(datetimes) < LEN_WEEK :
		the_datetime = the_datetime + datetime.timedelta(0,60)
		datetimes.append(datetime.datetime.strftime(the_datetime,time_format))
	return datetimes

def get_real_datetime_starting_on_given_weekday_int(weekday_begin_int,time_format):
	the_datetime = datetime.datetime.strptime('2017-01-01 00:00:00',time_format)
	while the_datetime.weekday() is not weekday_begin_int:
		the_datetime = the_datetime + datetime.timedelta(1)
	return the_datetime

def convert_string_to_datetime(string, time_format):
	return datetime.datetime.strptime(string,time_format)

def convert_datetime_to_string(datetime,time_format):
	return datetime.datetime.strttime(datetime,time_format)