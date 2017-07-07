from .Experiment import *
from .experiment_helper.Experiment_Helper_Iterate_Over_All_Sensors_Using_One_Sensor_As_Output import Experiment_Helper_Iterate_Over_All_Sensors_Using_One_Sensor_As_Output

import os
class Experiment_Iterate_Over_All_Sensors_Using_One_Sensor_As_Output(Experiment):
	def __init__(self):
		super(Experiment_Iterate_Over_All_Sensors_Using_One_Sensor_As_Output,self).__init__()

	def run_experiment(self):
		self._gather_experiment()
		self._iterate_over_all_sensors_test_and_train_using_one_sensor_as_target()
		self._calculate_accuracy_of_models()

	def _iterate_over_all_sensors_test_and_train_using_one_sensor_as_target(self):
		available_sensors = self.train_input_and_target_maker.get_source_idxs_list() # bc of type remove inefficient sensors, get available sensors
		for i in range(1,3):#for self.current_sensor_used_as_model_output in available_sensors:
			self.target_for_current_sensor_written_to_file = False
			self.current_sensor_used_as_model_output = available_sensors[i]
			logging.info("Starting experiment with sensor "+self.current_sensor_used_as_model_output)
			self._iterate_over_io_params()

	def _create_current_experiment_helper(self):
		self.current_experiment_helper = Experiment_Helper_Iterate_Over_All_Sensors_Using_One_Sensor_As_Output()
		self.current_experiment_helper.set_experiment_output_path(self.root_path)
		self.current_experiment_helper.set_sensor_name(self.current_sensor_used_as_model_output)
		self.current_experiment_helper.set_io_parameters_name(self.current_io_param.name)
		self.current_experiment_helper.setup_directory()
	
	def _set_input_target_makers_to_current_model_input_output_parameters(self):
		self._modify_current_input_output_parameters_to_reflect_current_sensor()
		super(Experiment_Iterate_Over_All_Sensors_Using_One_Sensor_As_Output,self)._set_input_target_makers_to_current_model_input_output_parameters()

	def _modify_current_input_output_parameters_to_reflect_current_sensor(self):
		self.current_io_param.set_target_sensor_idxs_list([self.current_sensor_used_as_model_output])
		if self.current_io_param.use_single_sensor_as_input: # if single input/single output
			self.current_io_param.set_input_sensor_idxs_list([self.current_sensor_used_as_model_output])