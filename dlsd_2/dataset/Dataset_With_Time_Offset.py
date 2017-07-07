from .Dataset import *


class Dataset_With_Time_Offset(Dataset):

	def __init__(self):
		super(Dataset_With_Time_Offset,self).__init__()
		self.source_numpy_array = None
		self.time_offset_numpy_array = None
		self.top_padding = 0
		self.bottom_padding = 0
		self.time_offsets_list = None
		self.max_time_offset = None
	
	def set_source_numpy_array(self, source_numpy_array):
		self.source_numpy_array = source_numpy_array

	def set_top_padding(self, top_padding):
		self.top_padding = top_padding

	def set_bottom_padding(self, bottom_padding):
		self.bottom_padding = bottom_padding

	def set_time_offsets_list(self, time_offsets_list):
		self.time_offsets_list = time_offsets_list
		self.max_time_offset = max(self.time_offsets_list)

	def create_time_offset_data(self):
		self._check_if_source_is_single_column()
		self._create_empty_numpy_array_of_correct_size()
		self._iterate_over_time_offsets_to_fill_created_data()

	def clip_ends_keep_data_between_indices(self,idxs):
		self.df = pd.DataFrame(self.time_offset_numpy_array[idxs[0]:idxs[1],])

	def _check_if_source_is_single_column(self):
		if len(self.source_numpy_array.shape)==1:
		    self.source_numpy_array = self.source_numpy_array.reshape(-1,1)

	def _create_empty_numpy_array_of_correct_size(self):
		row_size = self._num_rows_in_source_data() + self.max_time_offset + self.top_padding + self.bottom_padding
		col_size = len(self.time_offsets_list) * self._num_columns_in_source_data()
		self.time_offset_numpy_array = self.empty_np_array_with_size(row_size,col_size)
	
	def _iterate_over_time_offsets_to_fill_created_data(self):
		for i in range(len(self.time_offsets_list)):
		    a = self._calc_idx_start_row(i)
		    b = self._calc_idx_end_row(i)
		    x = self._calc_idx_start_col(i)
		    y = self._calc_idx_end_col(i)
		    self.time_offset_numpy_array[a:b, x:y] = self.source_numpy_array
	
	def _calc_idx_start_row(self, i):
		current_offset = self.time_offsets_list[i]
		current_offset_rel_to_max_offset = self.max_time_offset - current_offset
		return current_offset_rel_to_max_offset + self.top_padding
	
	def _calc_idx_end_row(self,i):
		current_offset = self.time_offsets_list[i]
		return self.time_offset_numpy_array.shape[0] - current_offset - self.bottom_padding
	
	def _calc_idx_start_col(self,i):
		return i * self._num_columns_in_source_data()
	
	def _calc_idx_end_col(self,i):
		start = self._calc_idx_start_col(i)
		return start + self._num_columns_in_source_data()

	def _num_columns_in_source_data(self):
		return self.source_numpy_array.shape[1]
	
	def _num_rows_in_source_data(self):
		return self.source_numpy_array.shape[0]
	