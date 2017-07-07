import datetime
import numpy as np
import pandas as pd
import logging
import copy

class Numpy_Datetime_Helper:
	def set_time_format(self,time_format):
		self.time_format = time_format

	def _convert_np_array_of_datetimes_to_string(self,np_array):
		for i in range(np_array.shape[0]):
		    np_array[i] = datetime.datetime.strptime(np_array[i],self.time_format)
		return np_array

	def convert_np_array_of_strings_to_datetime(self,np_array):
		for i in range(np_array.shape[0]):
		    np_array[i] = datetime.datetime.strptime(np_array[i],self.time_format)
		return np_array

	def _convert_list_of_datetime_objs_to_strings(self,the_list):
		strings = []
		for i in range(len(the_list)):
		    strings.append(datetime.datetime.strftime(the_list[i],self.time_format))
		return strings

class Time_Gap_Filler:
	def __init__(self):
		self.orig_df = None
		self.new_df = None
		self.orig_time_stamps = None
		self.new_time_stamps = None

	def set_time_format_with_string(self, time_format):
		self.time_format = time_format

	def fill_time_gaps_in_dataframe(self, orig_df):
		'''
			Public method for filling time gaps
			Params
				self.orig_df : panda data frame containing wide data (one row per time stamp, one column per sensor)
				self.time_format : format that time stamp is to be parsed with. some differences exist (no millisecond etc)
			Returns
				[self.new_df, self.new_time_stamps]
		'''
		self.orig_df = orig_df
		self._convert_original_timestamp_string_to_datetime()
		if self._count_gaps(self.orig_time_stamps) is 0:
			logging.info("No time gaps found")
			self._convert_original_timestamp_datetime_to_string()
			return self.orig_df
		logging.info("Time gaps found, beginning to fill")
		self._fill_gaps()
		return self.new_df


	#	------------------------------------------------------------


	def _convert_original_timestamp_string_to_datetime(self):
		self.orig_time_stamps = (self._convert_np_array_of_datetimes_to_string(copy.copy(self.orig_df.index.values)))
		#self.orig_df.index = self.orig_time_stamps

	def _convert_original_timestamp_datetime_to_string(self):
		pass#self.orig_df.index = self._convert_list_of_datetime_objs_to_strings(self.orig_df.index)

	def _convert_np_array_of_datetimes_to_string(self,np_array):
		for i in range(np_array.shape[0]):
		    np_array[i] = datetime.datetime.strptime(np_array[i],self.time_format)
		return np_array

	def _convert_list_of_datetime_objs_to_strings(self,the_list):
		strings = []
		for i in range(len(the_list)):
		    strings.append(datetime.datetime.strftime(the_list[i],self.time_format))
		return strings

	def _add_timestamp_string_to_new_time_stamps_from_datetime_obj(self,datetime_obj):
		#self.new_time_stamps.append(datetime.datetime.strftime(datetime_obj,self.time_format))
		self.new_time_stamps.append(datetime_obj)

	def _fill_gaps(self):
		self._create_empty_variables()
		self._fill_first_row()
		self._fill_table()
		self._label_table()
		self._check_if_has_gaps()


	#	------------------------------------------------------------	

	def _create_empty_variables(self):
		
		total_gap_size = self._get_total_length_of_all_gaps()
		self.new_df = pd.DataFrame(np.empty([self.orig_df.shape[0]+total_gap_size,self.orig_df.shape[1]]))
		self.new_df.iloc[:]=np.NAN
		self.new_time_stamps = []
		self.new_i = 0


	def _fill_first_row(self):
		
		self._add_timestamp_string_to_new_time_stamps_from_datetime_obj(self.orig_time_stamps[0])
		self.new_df.iloc[0] = self.orig_df.iloc[0].values
		self.new_i = 1


	def _fill_table(self):
		
		for i in range(1,self.orig_time_stamps.shape[0]):
			delta = self.orig_time_stamps[i] - self.orig_time_stamps[i-1]
			if(delta.seconds != 60 or delta.days != 0):
				self._gap_found(i)
			else:
				self._no_gap_found(i)


	def _label_table(self):

		self.new_df.index = self._convert_list_of_datetime_objs_to_strings(self.new_time_stamps)
		self.new_df.columns = self.orig_df.columns.values
		

	def _check_if_has_gaps(self):

		if self._count_gaps(self.new_time_stamps) is 0:
			logging.debug("Time gaps successfully filled")  
		else:
			raise Exception("%d Gaps found!!!"%count)

	#	------------------------------------------------------------	


	def _no_gap_found(self, i):

		self._add_timestamp_string_to_new_time_stamps_from_datetime_obj(self.orig_time_stamps[i])
		self.new_df.iloc[self.new_i,:] = self.orig_df.iloc[i,:].values
		self.new_i = self.new_i + 1
	
	def convert(self, date, time_format = '%Y-%m-%d %H:%M:%S'):
	    return datetime.datetime.strftime(date,self.time_format)


	def _gap_found(self, i):

		date_start = self.orig_time_stamps[i-1]
		date_end = self.orig_time_stamps[i]
		date_next, delta = self._increment_time_get_delta(date_start,date_end)
		while(delta.seconds > 0 or delta.days != 0):
			self._add_timestamp_string_to_new_time_stamps_from_datetime_obj(date_next)
			date_next, delta = self._increment_time_get_delta(date_next,date_end)
			self.new_i = self.new_i + 1
		self._add_timestamp_string_to_new_time_stamps_from_datetime_obj(date_next)
		self.new_df.iloc[self.new_i,] = self.orig_df.iloc[i,].values
		self.new_i = self.new_i + 1


	#	------------------------------------------------------------	


	def _increment_time_get_delta(self, _current_date_next, _date_end):
		_date_next = _current_date_next + datetime.timedelta(0,60)
		return _date_next, _date_end - _date_next


	def _count_gaps(self, np_array):
		_count = 0
		for i in range(1,len(np_array)):
			delta = np_array[i] - np_array[i-1]
			if(delta.seconds !=60 or delta.days != 0):
				_count = _count+1
		return _count


	#	------------------------------------------------------------	


	def _get_total_length_of_all_gaps(self):

		idxs_gaps = self._get_indices_where_gaps_begin(self.orig_time_stamps)

		# Need to know how large new matrix is : count size of all gaps
		total_gap_size = 0
		for i in range(len(idxs_gaps)):
		    #for gap_start in idxs_gaps:
		    date_start = self.orig_time_stamps[idxs_gaps[i]]
		    date_end = self.orig_time_stamps[idxs_gaps[i]+1]

		    # add a single next minute
		    date_next = date_start
		    date_next = date_start + datetime.timedelta(0,60)
		    delta = date_end - date_next

		    while(delta.seconds != 60 or delta.days != 0): 
		        total_gap_size = total_gap_size + 1
		        date_next = date_next + datetime.timedelta(0,60)
		        delta = date_end - date_next
		    total_gap_size = total_gap_size + 1

		return total_gap_size

	def _get_indices_where_gaps_begin(self, vector_of_time_stamps):

		idxs_gaps = []
		for i in range(1,vector_of_time_stamps.shape[0]):
			delta = vector_of_time_stamps[i] - vector_of_time_stamps[i-1]
			if(delta.seconds != 60 or delta.days != 0):
				idxs_gaps.append(i-1)
		return idxs_gaps




