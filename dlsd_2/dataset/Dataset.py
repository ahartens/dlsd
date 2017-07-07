import pandas as pd
import numpy as np
import logging

from .dataset_helpers.Denormalizer import Denormalizer
from .dataset_helpers.Time_Gap_Filler import Time_Gap_Filler
from .dataset_helpers.Inefficient_Sensors_Remover import Inefficient_Sensors_Remover

class Dataset:

	def __init__(self):
		self.df = None
		self.denormalizer = None
		self.path_to_csv = None
		self.time_format = None

	def set_denormalizer(self,denormalizer):
		self.denormalizer = denormalizer

	def set_numpy_array(self,numpy_array):
		self.df = pd.DataFrame(numpy_array)

	def set_pandas_df(self,df):
		self.df = df

	def get_pandas_df(self):
		return self.df

	def get_numpy_array(self):
		return self.df.values

	def get_number_rows(self):
		return self.df.shape[0]

	def get_number_columns(self):
		return self.df.shape[1]

	def get_numpy_rows_at_idxs(self,idxs):
		return self.df.iloc[idxs].values

	def get_numpy_columns_at_idxs(self,idxs):
		return self.df.iloc[:,idxs].values

	def get_column_names(self):
		return self.df.columns.values

	def get_row_names(self):
		return self.df.index.values

	def set_row_names(self,row_names):
		self.df.index = row_names

	def set_column_names(self,col_names):
		self.df.columns = col_names	

	def read_csv(self,path_to_csv,sep=",",index_col = None):
		logging.info("Reading csv : "+path_to_csv)
		self.path_to_csv = path_to_csv
		self.df = pd.read_csv(self.path_to_csv,sep=sep,header=0,index_col=index_col)

	def write_csv(self,path_to_csv):
		self.df.to_csv(path_to_csv)
		
	def normalize(self):
		if self.denormalizer is None:
			max_value = np.nanmax(self.df.values)
			self.df = ((self.df/max_value)*.99999999) + 0.00000001
			self.denormalizer = Denormalizer(max_value)
		else:
		 	self.df = self.denormalizer.normalize(self.df)
	
	def denormalize(self):
		self.df = self.denormalizer(self.df)

	def rolling_average_with_window(self,window):
		logging.info("Performing rolling average with window %d : Final shape is (%d, %d)"%(window,self.df.shape[0],self.df.shape[1]))
		self.df = self.df.rolling(window, min_periods=1).mean()

	def remove_inefficient_sensors(self):
		logging.info("Removing inefficient sensors")
		# TODO finish this
		#self.df = removeInefficientSensors(data_wide_all,sensorEfficiency)
        #specifiedSensors = pd.DataFrame(data_wide.columns.values.reshape((data_wide.columns.values.shape[0],-1)))
		pass

	def summarize_sensor_efficiency(self):
		idxs_where_nan = np.isnan(self.df.values)
		idxs = [len(np.where(idxs_where_nan[:,x] == True)[0]) for x in range(idxs_where_nan.shape[1])]
		max_efficiency = min(idxs)/idxs_where_nan.shape[0]
		min_efficiency = max(idxs)/idxs_where_nan.shape[0]
		logging.info("Summary of sensor efficiency :\tMAX : %f \t MIN : %f"%(max_efficiency,min_efficiency))

	def empty_np_array_with_size(self,rows,columns):
		np_array = np.zeros((rows,columns))
		np_array[:] = np.NAN
		return np_array

	def fill_time_gaps_using_time_format(self, time_format):
		self.time_format = time_format
		time_gap_filler = Time_Gap_Filler()
		time_gap_filler.set_time_format_with_string(self.time_format)
		self.df = time_gap_filler.fill_time_gaps_in_dataframe(self.df)

	def remove_any_rows_with_NaN(self):
		self.df = self.df.iloc[~np.isnan(self.df.values).any(axis=1)]
		logging.info("Removing all rows with NaN, number data points is %d"%self.df.shape[0])

	def remove_inefficient_sensors(self, efficiency_threshold):
		isr = Inefficient_Sensors_Remover()
		self.df = isr.remove_inefficient_sensors(self.df,efficiency_threshold)
		self.efficiency = isr.get_efficiency_df()

	def write_sensor_efficiency_to_file(self,file_path):
		self.efficiency.to_csv(file_path)
