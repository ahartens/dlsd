class Model_Input_Output_Parameters:
	def __init__(self):
		self.input_time_offsets_list = [0]
		self.input_sensor_idxs_list = None
		self.target_time_offsets_list = None
		self.target_sensor_idxs_list = None
		self.name = None
		self.use_adjacency_matrix = False
		self.use_single_sensor_as_input = False
		self.adjacency_matrix = None
		self.include_output_sensor_in_adjacency = True

	def set_input_time_offsets_list(self, the_list):
		self.input_time_offsets_list = the_list
	
	def set_input_sensor_idxs_list(self, the_list):
		self.input_sensor_idxs_list = the_list
	
	def set_target_time_offsets_list(self, the_list):
		self.target_time_offsets_list = the_list
	
	def set_target_sensor_idxs_list(self, the_list):
		self.target_sensor_idxs_list = the_list
	
	def set_use_adjacency_matrix(self, the_boolean):
		self.use_adjacency_matrix = the_boolean