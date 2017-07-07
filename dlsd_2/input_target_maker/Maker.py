from dlsd_2.dataset.Dataset import Dataset
from dlsd_2.dataset.Dataset_With_Time_Offset import Dataset_With_Time_Offset
import logging

class Maker:
	def __init__(self):
		self.selected_source_object = None # the subset of source data (ex a single sensor) in input/target
		self.selected_source_numpy_data = None
		self.dataset_object = None
		self.sensor_idxs_list = None
		self.time_offsets_list = None
		self.top_padding = 0
		self.bottom_padding = 0

	def extract_desired_sensors_and_row_names_from_source_dataset_object(self,source_dataset_object):
		if self.sensor_idxs_list is None:
			self._set_sensor_idxs_to_use_all_sensors_from_source(source_dataset_object)
		self.selected_source_numpy_data = source_dataset_object.df[self.sensor_idxs_list]
		self.selected_source_sensor_rows_names = source_dataset_object.df.index.values

	def _set_sensor_idxs_to_use_all_sensors_from_source(self, source_dataset_object):
		self.sensor_idxs_list = list(source_dataset_object.df.columns.values)

	def make_dataset_object_with_clip_range(self, clip_range):
		if self.time_offsets_list is None:
			raise Exception('no time offsets are set')
		self.dataset_object = Dataset_With_Time_Offset()
		self.dataset_object.set_source_numpy_array(self.selected_source_numpy_data)
		self.dataset_object.set_top_padding(self.top_padding)
		self.dataset_object.set_bottom_padding(self.bottom_padding)
		self.dataset_object.set_time_offsets_list(self.time_offsets_list)
		self.dataset_object.create_time_offset_data()
		self.dataset_object.clip_ends_keep_data_between_indices(clip_range)
		self._create_and_set_column_headers()

	def _create_and_set_column_headers(self):
		headers = []
		for time_offset in self.time_offsets_list:
			for sensor in self.sensor_idxs_list:
				headers.append(str(sensor)+"__t"+str(time_offset))
		self.dataset_object.df.columns = headers

	def max_time_offset(self):
		return max(self.time_offsets_list)

	def multiply_by_adjacency_of_target_sensor_including_target_sensor(self, adjacency_matrix, target_sensor_idxs_list, include_target_sensor = True):
		target_sensor = target_sensor_idxs_list[0]
		target_adjacency = self._get_adjacency_for_target_sensor(adjacency_matrix, target_sensor, self.sensor_idxs_list)
		if not include_target_sensor:
			target_sensor_idx_in_input = self.sensor_idxs_list.index(target_sensor)
			target_adjacency[target_sensor_idx_in_input] = 0
		self.selected_source_numpy_data = self.selected_source_numpy_data * target_adjacency

	def _get_adjacency_for_target_sensor(self,adjacency_matrix, target_sensor, input_sensor_idxs_list):
		adjacency_matrix.subset_sensors(input_sensor_idxs_list)
		adjacency = adjacency_matrix.get_adjacency_for_sensor(target_sensor)[0]
		return adjacency
