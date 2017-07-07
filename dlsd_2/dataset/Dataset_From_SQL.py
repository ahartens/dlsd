from .Dataset import Dataset
import logging

class Dataset_From_SQL(Dataset):

	def pivot(self):
		logging.info("Pivoting SQL dataset")
		sql_headers = self.df.columns.values
		self.df = self.df.pivot(index = sql_headers[1],
									columns = sql_headers[0],
									values = sql_headers[2])
		self._check_column_headers_are_strings()

	def pivot_using_specified_sensors(self, specified_sensors):
		# TODO create separate class for specified sensors?
		logging.info("Pivoting SQL dataset using %d specified sensors")
		sensor_idxs = np.where(self.df.iloc[:,0].values==specified_sensors.values)[1]
		self.df = self.df.iloc[sensor_idxs,:]
		self._check_column_headers_are_strings()


	def _check_column_headers_are_strings(self):
		if(type(self.df.columns.values) is not 'str' ):
			self.df.columns = [str(x) for x in self.df.columns.values]
