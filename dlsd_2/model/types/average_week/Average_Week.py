from dlsd_2.model.Model import *
from dlsd_2.model.types.average_week.Average_Week_Content import *
from dlsd_2.input_target_maker.Maker import *

class Average_Week(Model):

	def __init__(self):
		super(Average_Week,self).__init__()
		logging.info("Creating Average Week model")
		self.average_week_externally_set = False
		self.model_content = Average_Week_Content()
		self.name = "Average_Week"

	def train_with_prepared_input_target_maker(self,itm):
		if self.average_week_externally_set is False:
			super(Average_Week,self).train_with_prepared_input_target_maker(itm)
		else:
			self._set_global_itms_for_training(itm)
			self.model_input.set_input_and_target_from_input_target_maker(itm)

	def _train(self):
		self.model_content.create_source_average_data_with_input_target_maker(self.current_input_target_maker)

	def _test(self):
		self.model_content.set_input_target_maker(self.current_input_target_maker)
		predictions = self.model_content.make_prediction_dataset_object()
		super(Average_Week,self).set_model_output_with_predictions_numpy_array(predictions.df.values) # TODO check works

	def _get_day_begin_integer_from_target_dataset(self):
		first_time_stamp_string = self.current_input_target_maker.target_dataset_object.df.index.values[0,0]
		first_timestampe_datetime = datetime.datetime.strptime(first_time_stamp_string,self.current_input_target_maker.time_format)

	def set_average_data_from_csv_file_path(self,file_path):
		''' Single average week is provided : training doesn't have to occur '''
		self.average_week_externally_set = True
		self.model_content.set_average_data_from_csv_file_path(file_path)

	def write_average_week_to_filepath(self, file_path):
		''' After training a single average week is created. Print this out here '''
		self.model_content.source_average_dataset_object.write_csv(file_path)

