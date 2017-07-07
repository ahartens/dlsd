from dlsd_2.experiment.experiment_output_reader.Many_Sensor_Directory_Helper import Many_Sensor_Directory_Helper
from dlsd_2.experiment.experiment_output_reader.Experiment_Output_Reader import Experiment_Output_Reader
from dlsd_2.experiment.experiment_output_reader.Experiment_Error_Calculator import Experiment_Error_Calculator
import logging

class Experiment_Error_Calculator_For_Iterate_Over_All_Sensors_Using_One_Sensor_As_Output:
    def __init__(self):
        self.directory_helper = Many_Sensor_Directory_Helper()
        self.reader = Experiment_Output_Reader()
        self.list_of_functions = None
    
    def set_root_experiment_directory(self, path):
        self.directory_helper.set_root_experiment_directory(path)
    
    def set_analysis_functions(self, list_of_functions):
        self.analysis_functions = list_of_functions
    
    def analyze_all_sensors(self):
        self.directory_helper.prepare_list_of_all_sensors_to_analyze()
        self._iterate_over_all_sensors_calculating_error()
    
    def _iterate_over_all_sensors_calculating_error(self):
        for sensor in self.directory_helper.all_sensor_dirs:
            self.reader = Experiment_Output_Reader()
            self._extract_data_from_current_sensor(sensor)
            self._iterate_over_error_functions()
    
    def _extract_data_from_current_sensor(self,sensor):
        self.directory_helper.set_current_sensor_directory_with_sensor(sensor)
        self.reader.set_experiment_output_directory(self.directory_helper.current_sensor_dir)
        self.reader.extract_data()

    def _iterate_over_error_functions(self):
        for error_function in self.analysis_functions:
            self._do_analysis_with_error_function(error_function)
            
    def _do_analysis_with_error_function(self, error_function):
        analyzer = Experiment_Error_Calculator()
        analyzer.set_experiment_output_reader(self.reader)
        analyzer.set_output_directory_path(self.directory_helper.make_current_error_directory())
        analyzer.set_analysis_function(error_function)
        analyzer.do_analysis()

