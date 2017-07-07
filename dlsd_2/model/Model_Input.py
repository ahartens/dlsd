import logging

class Model_Input:

	def __init__(self):
		self.input_dataset_object = None
		self.target_dataset_object = None

	def set_input_and_target_from_input_target_maker(self, input_target_maker):
		self.set_input_dataset_object(input_target_maker.get_input_dataset_object())
		self.set_target_dataset_object(input_target_maker.get_target_dataset_object())

	def set_input_dataset_object(self,dataset_object):
		self.input_dataset_object = dataset_object

	def set_target_dataset_object(self,dataset_object):
		self.target_dataset_object = dataset_object

	def get_number_inputs(self):
		return self.input_dataset_object.df.shape[1]

	def get_number_datapoints(self):
		return self.input_dataset_object.df.shape[0]

	def get_number_targets(self):
		return self.target_dataset_object.df.shape[1]

	def get_all_input_as_numpy_array(self):
		return self.input_dataset_object.df.values

	def get_all_target_as_numpy_array(self):
		return self.target_dataset_object.df.values

	def get_target_dataset_object(self):
		return self.target_dataset_object