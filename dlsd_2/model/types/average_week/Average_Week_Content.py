from dlsd_2.model.Model_Content import Model_Content
from dlsd_2.dataset.Dataset import Dataset
from dlsd_2.dataset.dataset_helpers.Time_Gap_Filler import Numpy_Datetime_Helper
from dlsd_2.calc.calculate_average_week import *
import logging
import numpy as np
import pandas as pd
import datetime

LEN_WEEK = 7*1440


class Average_Week_Content(Model_Content):
	
	def __init__(self):
		super(Average_Week_Content,self).__init__()
		self.source_average_dataset_object = Dataset() # contains all sensors
		self.prediction_dataset_object = Dataset()
		self.subset_avg_week_array = None # subset of sensors specified by target_sensor_idxs_list
		self.target_begin_weekday_int = None
		self.num_target_rows = None
		self.num_target_sensors = None
		self.num_target_offsets = None
		self.input_target_maker = None
		self.weekday_int_source = None

	def set_input_target_maker(self, input_target_maker, test = False):
		self.input_target_maker = input_target_maker
		self.num_target_sensors = len(input_target_maker.get_target_sensor_idxs_list())
		self.num_target_offsets = len(input_target_maker.get_target_time_offsets_list())
		self._set_parameters_from_input_target_maker() if test is False else logging.debug("Testing")

	def _set_parameters_from_input_target_maker(self):
		self.set_source_weekday_begin_int()
		self.num_target_rows = self.input_target_maker.get_target_dataset_object().get_number_rows()

	def set_source_weekday_begin_int(self):
		first_day_timestamp_string = self.input_target_maker.source_dataset_object.df.index.values[0]
		self.target_begin_weekday_int = get_weekday_int_from_timestamp_string_with_format(first_day_timestamp_string,self.input_target_maker.time_format) if self.target_begin_weekday_int is None else self.target_begin_weekday_int

	def set_average_data_from_csv_file_path(self,file_path):
		self.source_average_dataset_object = Dataset()
		self.source_average_dataset_object.read_csv(file_path,index_col=0)

	def create_source_average_data_with_input_target_maker(self, input_target_maker):
		source = input_target_maker.source_dataset_object
		idx = self._get_idx_first_midnight(input_target_maker)
		average_data = calculate_average_week_from_numpy_array(source.df.iloc[idx:source.df.shape[0],:].values)
		current_weekday_start_int = get_weekday_int_from_timestamp_string_with_format(source.df.index.values[0], input_target_maker.time_format) if self.weekday_int_source is None else self.weekday_int_source
		average_data = rearrange_week_starting_to_start_on_monday_with_current_day_start_int(average_data, current_weekday_start_int)
		self.source_average_dataset_object.set_numpy_array(average_data)
		self.source_average_dataset_object.set_row_names(make_week_starting_on_monday_timestamps(weekday_begin_int = 0))
		self.source_average_dataset_object.set_column_names(source.get_column_names())

	def _get_idx_first_midnight(self,itm):
		idx = 0
		the_datetime = convert_string_to_datetime(itm.source_dataset_object.df.index.values[idx],itm.time_format)
		while(the_datetime.hour!=0):
			idx = idx + 1
			the_datetime = convert_string_to_datetime(itm.source_dataset_object.df.index.values[idx],itm.time_format)
		return 0

	def make_prediction_dataset_object(self):
		size = [self.num_target_rows , self.num_target_offsets*self.num_target_sensors]
		array = np.zeros(size)
		self._extract_sensors_currently_being_used_as_output_from_source_data()
		self._iterate_over_target_time_offsets_replicating_average_week(array)
		self.prediction_dataset_object.set_numpy_array(array)
		return self.prediction_dataset_object

	def _extract_sensors_currently_being_used_as_output_from_source_data(self):
		self.subset_avg_week_array = self.source_average_dataset_object.df[self.input_target_maker.get_target_sensor_idxs_list()].values


	def _iterate_over_target_time_offsets_replicating_average_week(self,array):
		'''
			For each time offset:
				rearrange avg week to start at desired time offset
				copy the average week x number of times (until target # rows filled) 
		'''
		for i in range(self.num_target_offsets):
			cur_time_offset = self._calculate_time_offset_in_min_relative_to_input_time_offsets(i)
			avg_week_starting_at_time = rearrange_week_to_start_at_time(self.subset_avg_week_array, cur_time_offset)
			self._fill_prediction_with_copies_of_avg_week_at_timeoffset_index(avg_week_starting_at_time, i, array)
				
	def _calculate_time_offset_in_min_relative_to_input_time_offsets(self,idx_current_time_offset):
		'''
			All time offsets are all relative to time 0 of the input time offset. 
			So if input time offset is [0,5,10] and target time offset is [5,10,20] the target time offsets are actually [15,20,30]
			Average Weeks are standardized to start on mondays, and then rearranged to fit the target beginning day
		'''
		current_time_offset = self._target_time_offset_at_index(idx_current_time_offset)
		weekday_begin_in_minutes = self.target_begin_weekday_int * 1440
		return current_time_offset + weekday_begin_in_minutes + self._max_input_time_offset()

	def _fill_prediction_with_copies_of_avg_week_at_timeoffset_index(self, avg_week_starting_at_time, idx_current_time_offset,array):
		'''
			Iterate down the rows of the prediction array, filling in the current time_offset columns
			with copies of the avg week (adjusted to start at the time offset)
		'''
		s_y = self.num_target_sensors*idx_current_time_offset # fill only columns associated with current time offset
		e_y = s_y + self.num_target_sensors
		n_copies_avg_week_to_make = int(self.num_target_rows/LEN_WEEK)
		for i in range(0,n_copies_avg_week_to_make):
			array[i*LEN_WEEK:(i+1)*LEN_WEEK,s_y:e_y] = avg_week_starting_at_time
		# fill last, not full week row by row :
		i = 0
		ind = n_copies_avg_week_to_make*LEN_WEEK
		while(ind<self.num_target_rows):
			array[ind,s_y:e_y] = avg_week_starting_at_time[i,:]
			ind = ind + 1
			i = i + 1

	def _target_time_offset_at_index(self, index):
		return self.input_target_maker.get_target_time_offsets_list()[index]
	
	def _max_input_time_offset(self):
		return max(self.input_target_maker.get_input_time_offsets_list())