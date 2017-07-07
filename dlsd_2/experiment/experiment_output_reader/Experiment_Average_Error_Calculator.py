import os
import shutil
import pandas as pd    
from dlsd_2.experiment.experiment_output_reader.Many_Sensor_Directory_Helper import Many_Sensor_Directory_Helper

class Experiment_Average_Error_Calculator:
    def __init__(self):
        self.directory_helper = Many_Sensor_Directory_Helper()
        self.current_error_name = None
        self.all_error_types = None
        self.error_function_average_helpers = []
    
    def set_root_experiment_directory(self, path):
        self.directory_helper.set_root_experiment_directory(path)
    
    def calculate_average(self):
        self.directory_helper.prepare_list_of_all_sensors_to_analyze()
        self._init_average_tables_with_first_values()
        self._iterate_over_all_sensors_summing_error()
        self._divide_by_n()
        self._write_averages_to_file()
    
    def _write_averages_to_file(self):
        dir_path = os.path.join(self.directory_helper.root_experiment_directory,"avg_errors")
        self.directory_helper._check_or_make_dir(dir_path)
        for error_directory in self.error_function_average_helpers:
            error_directory.write_averages_to_file(dir_path)

    def _init_average_tables_with_first_values(self):
        first_sensor = self.directory_helper.all_sensor_dirs[0]
        error_dir = self._get_current_error_dir_for_sensor(first_sensor)
        self.all_error_types = next(os.walk(error_dir))[1]
        for error_type in self.all_error_types:
            error = Error_Directory()
            error.setup_structure_to_reflect_directory(os.path.join(error_dir,error_type))
            error.name = error_type
            self.error_function_average_helpers.append(error)

    def _iterate_over_all_sensors_summing_error(self):
        for i in range(1,len(self.directory_helper.all_sensor_dirs)):
            sensor = self.directory_helper.all_sensor_dirs[i]
            error_dir = self._get_current_error_dir_for_sensor(sensor)
            for error_func_type in self.error_function_average_helpers:
                error_func_type.set_current_error_dir_path(error_dir)
                error_func_type.add_current_dir_values_to_sum()
            
    def _get_current_error_dir_for_sensor(self, sensor):
        self.directory_helper.set_current_sensor_directory_with_sensor(sensor)
        return self.directory_helper.get_current_error_directory()
    
    def _divide_by_n(self):
        n = len(self.directory_helper.all_sensor_dirs)
        for error_directory in self.error_function_average_helpers:
            error_directory.divide_by_n(n)
            
class Error_Directory:
    def __init__(self):
        self.name = None
        self.average_error_tables = []
        self.current_path = None
    
    def setup_structure_to_reflect_directory(self, directory):
        files_in_directory = next(os.walk(directory))[2]
        for file_name in files_in_directory:
            error_table = Average_Error_Table()
            error_table.name = file_name
            error_table.df = pd.read_csv(os.path.join(directory,file_name),index_col=0)
            self.average_error_tables.append(error_table)
    
    def set_current_error_dir_path(self, error_dir_path):
        self.current_path = os.path.join(error_dir_path,self.name)
    
    def add_current_dir_values_to_sum(self):
        for average_error_table in self.average_error_tables:
            average_error_table.set_current_error_table_path(self.current_path)
            average_error_table.read_current_table_values_and_add_to_sum()
    
    def divide_by_n(self,n):
        for average_error_table in self.average_error_tables:
            average_error_table.divide_by_n(n)
    
    def write_averages_to_file(self,dir_path):
        error_path = os.path.join(dir_path,self.name)
        if os.path.exists(error_path):
            shutil.rmtree(error_path)
        os.makedirs(error_path)
        for average_error_table in self.average_error_tables:
            average_error_table.write_averages_to_file(error_path)
        

class Average_Error_Table:
    def __init__(self):
        self.name = None
        self.df = None
        self.current_path = None
    
    def set_current_error_table_path(self,error_dir_path):
        self.current_path = os.path.join(error_dir_path,self.name)
    
    def read_current_table_values_and_add_to_sum(self):
        new_values = pd.read_csv(self.current_path,index_col=0)
        self.df.iloc[:] = self.df.values + new_values.values
    
    def divide_by_n(self,n):
        self.df = self.df/n
    
    def write_averages_to_file(self, path):
        self.df.to_csv(os.path.join(path,self.name))