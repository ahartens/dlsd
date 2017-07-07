from .Model_Input import Model_Input
from .Model_Output import Model_Output
from .Model_Content import Model_Content

import logging

class Model:
	'''
		Two phases of model usage. Both methods require an input_target maker
			1. During train, the model_content receives the training data and builds an internal representation of the model
			2. During test, the model_content is responsible for creating a target_dataset_object
		The model_input is a wrapper for the input_dataset_object and target_dataset_object, responsible for handling input to model
		The model_output is a wrapper for a prediction_dataset_object and target_dataset_object, responsible for calculating prediction error
	'''
	def __init__(self):
		self.model_input = Model_Input()
		self.model_output = Model_Output()
		self.model_content = Model_Content()
		self.train_input_target_maker = None
		self.current_input_target_maker = None
		self.experiment_helper = None
		self.name = "Abstract Class"

	def train_with_prepared_input_target_maker(self,itm):
		self._set_global_itms_for_training(itm)
		self.model_input.set_input_and_target_from_input_target_maker(itm)
		self._train()

	def test_with_prepared_input_target_maker(self,itm):
		self.current_input_target_maker = itm
		self.model_input.set_input_and_target_from_input_target_maker(itm)
		self._test()

	def prepare_data_and_train_with_input_target_maker(self,itm):
		self._set_global_itms_for_training(itm)
		self.current_input_target_maker.prepare_source_data_and_make_input_and_target()
		self.model_input.set_input_and_target_from_input_target_maker(itm)
		self._train()

	def prepare_data_and_test_with_input_target_maker(self,itm):
		self.current_input_target_maker = itm
		self.current_input_target_maker.copy_parameters_from_maker(self.train_input_target_maker)
		self.current_input_target_maker.prepare_source_data_and_make_input_and_target()
		self.model_input.set_input_and_target_from_input_target_maker(itm)
		self._test()

	def _set_global_itms_for_training(self,itm):
		self.current_input_target_maker = itm
		self.train_input_target_maker = itm

	def _train(self):
		raise NotImplementedError
	
	def _test(self):
		raise NotImplementedError

	def calc_prediction_accuracy(self):
		mape = self.model_output.calc_mape()
		mae = self.model_output.calc_mae()
		return {'mape':mape,'mae':mae}
		
	def get_target_and_predictions_df(self):
		return self.model_output.make_target_and_predictions_df()

	def get_target_df(self):
		return self.model_output.get_target_df

	def get_prediction_df(self):
		return self.model_output.get_prediction_df()

	def write_target_and_predictions_to_file(self, file_path):
		logging.info("Writing target and predictions to %s"%file_path)
		new_df = self.get_target_and_predictions_df()
		new_df.to_csv(file_path)

	def write_predictions_using_experiment_helper(self):
		path = self.experiment_helper.make_new_model_prediction_file_path_with_model_name(self.name)
		logging.info("Writing Predictions to %s"%path)
		predictions = self.get_prediction_df()
		predictions.to_csv(path)

	def set_model_output_with_predictions_numpy_array(self, predictions_numpy_array):
		''' Called after testing by subclasses of Model '''
		self.model_output.set_target_dataset_object(self.model_input.get_target_dataset_object())
		self.model_output.set_prediction_dataset_object_with_numpy_array(predictions_numpy_array)

	def set_experiment_helper(self, experiment_helper):
		''' Experiment_helpers provide directory file paths to save information to '''
		self.experiment_helper = experiment_helper
