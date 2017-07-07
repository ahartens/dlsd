from .experiment_helper.Experiment_Helper import Experiment_Helper
from dlsd_2.input_target_maker.Input_Target_Maker import Input_And_Target_Maker_2
from dlsd_2.input_target_maker.Source_Maker import Source_Maker
from dlsd_2.input_target_maker.Model_Input_Output_Parameters import Model_Input_Output_Parameters
from dlsd_2.input_target_maker.Adjacency_Matrix import Adjacency_Matrix
from dlsd_2.experiment.experiment_output_reader.Experiment_Error_Calculator_For_Iterate_Over_All_Sensors_Using_One_Sensor_As_Output import *
from dlsd_2.experiment.experiment_output_reader.Experiment_Average_Error_Calculator import Experiment_Average_Error_Calculator
from dlsd_2.calc.error import MAE
from dlsd_2.calc.error import MAPE

import pandas as pd
import logging

logging.basicConfig(level=logging.DEBUG)#filename='17_05_04_dlsd_2_trials.log',)

class Experiment:
	def __init__(self):
		self.root_path = None
		self.source_maker = None
		self.models = []
		self.model_input_output_parameters = []
		self.train_input_and_target_maker = None
		self.test_input_and_target_maker = None
		self.current_io_paramter = None
	
	def set_experiment_root_path(self, path):
		self.root_path = path # path where all output should be stored

	def run_experiment(self):
		self._gather_experiment()
		self._iterate_over_io_params()
		self._calculate_accuracy_of_models()

	def _gather_experiment(self):
		self._define_source_maker()
		self._define_model_input_output_parameters()
		self._define_models() 
		self._prepare_source_data_and_input_target_makers()

	def _define_source_maker(self):
		raise NotImplementedError

	def _define_models(self):
		raise NotImplementedError

	def _define_model_input_output_parameters(self):
		raise NotImplementedError

	def _define_input_and_target_makers(self):
		raise NotImplementedError

	def _prepare_source_data_and_input_target_makers(self):
		self.source_maker.create_train_and_test_data()
		self._create_input_and_target_makers()

	def _create_input_and_target_makers(self):
		self.train_input_and_target_maker = Input_And_Target_Maker_2()
		self.test_input_and_target_maker = Input_And_Target_Maker_2()
		self.train_input_and_target_maker.set_source_dataset_object(self.source_maker.train)
		self.test_input_and_target_maker.set_source_dataset_object(self.source_maker.test)
		self.train_input_and_target_maker.time_format = self.source_maker.time_format_train
		self.test_input_and_target_maker.time_format = self.source_maker.time_format_test

	def _iterate_over_io_params(self):
		for input_output_parameter in self.model_input_output_parameters:
			self.current_io_param = input_output_parameter			
			self._create_current_experiment_helper()
			self._create_input_and_target_to_current_io_params()
			self._train_and_test_all_models_and_write_predictions_to_file()

	def _create_current_experiment_helper(self):
		self.current_experiment_helper = Experiment_Helper()
		self.current_experiment_helper.set_experiment_output_path(self.root_path)
		self.current_experiment_helper.set_io_parameters_name(self.current_io_param.name)
		self.current_experiment_helper.setup_directory()

	def _create_input_and_target_to_current_io_params(self):
		self._set_input_target_makers_to_current_model_input_output_parameters()
		self._make_input_and_target()
		self._write_target_data_to_file()

	def _train_and_test_all_models_and_write_predictions_to_file(self):
		for model in self.models:
			model.set_experiment_helper(self.current_experiment_helper)
			model.train_with_prepared_input_target_maker(self.train_input_and_target_maker)
			model.test_with_prepared_input_target_maker(self.test_input_and_target_maker)
			model.write_predictions_using_experiment_helper()

	def _set_input_target_makers_to_current_model_input_output_parameters(self):
		self.train_input_and_target_maker.set_all_sensor_idxs_and_time_offsets_using_parameters_object(self.current_io_param)
		self.test_input_and_target_maker.set_all_sensor_idxs_and_time_offsets_using_parameters_object(self.current_io_param)

	def _make_input_and_target(self):
		self.train_input_and_target_maker.make_input_and_target()
		self.test_input_and_target_maker.make_input_and_target()

	def _write_target_data_to_file(self):
		test_df = self.test_input_and_target_maker.get_target_df()
		test_df.to_csv(self.current_experiment_helper.get_target_file_path())

	def _collect_all_model_accuracies(self):
		model_prediction_accuracies = []
		for model in self.models:
			model_prediction_accuracies.append(model.calc_prediction_accuracy())
		return model_prediction_accuracies

	def _calculate_accuracy_of_models(self):
		logging.debug("calculating average error")
		analyzer = Experiment_Error_Calculator_For_Iterate_Over_All_Sensors_Using_One_Sensor_As_Output()
		analyzer.set_root_experiment_directory(self.root_path)
		analyzer.set_analysis_functions([MAE()])
		analyzer.analyze_all_sensors()
		logging.debug("calculating average error")
		avg = Experiment_Average_Error_Calculator()
		avg.set_root_experiment_directory(self.root_path)
		avg.calculate_average()


	def add_model(self, model):
		self.models.append(model)

	def add_input_output_parameter(self, io_param):
		self.model_input_output_parameters.append(io_param)

	def set_input_output_parameters_list(self, the_list):
		self.model_input_output_parameters = the_list

	def set_source_maker(self, source_maker):
		self.source_maker = source_maker