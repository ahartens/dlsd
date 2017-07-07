import os
import pandas as pd
import numpy as np
class Experiment_Error_Calculator:
    def __init__(self):
        self.reader = None
        self.mae_tables = []
        self.col_num = None
        self.path_output = None
        self.current_table = None
        self.analysis_function = None

    def set_experiment_output_reader(self, reader):
        self.reader = reader
       
    def set_output_directory_path(self,path):
        self.output_directory_path = path
    
    def set_analysis_function(self, function):
        self.analysis_function = function
        
    def do_analysis(self):
        self._make_analysis_output_directory()
        self._iterate_over_all_models_and_write_analysis_files()

    def _make_analysis_output_directory(self):
        self.path_output = self._check_or_make_dir(os.path.join(self.output_directory_path,self.analysis_function.name))

    def _iterate_over_all_models_and_write_analysis_files(self):
        model_names = self.reader.get_model_names()
        for model_name in model_names:
            dicts_for_model = self.reader.get_predictions_and_target_for_model_name(model_name)
            self._make_empty_tables_for_current_model(dicts_for_model)
            self._iterate_over_all_io_params_for_single_model_doing_analysis(dicts_for_model)
            self.current_table.to_csv(os.path.join(self.path_output,model_name+".csv"))

    def _make_empty_tables_for_current_model(self,dicts_for_model):
        self.col_num = dicts_for_model[0]['df'].shape[1]
        columns = dicts_for_model[0]['df'].columns.values
        index = self.reader.get_io_param_names()
        self.current_table = pd.DataFrame(np.zeros((len(dicts_for_model)-1,self.col_num)))
        self.current_table.columns = columns
        self.current_table.index = index
    
    def _iterate_over_all_io_params_for_single_model_doing_analysis(self,dicts_for_model):
        target = dicts_for_model[0]['df'].values
        for i in range(1,len(dicts_for_model)):
            preds = dicts_for_model[i]['df']
            targ = dicts_for_model[i]['target']
            mae = self.analysis_function.calc_error_with_prediction_and_target(preds,targ.values) # sometimes problems here
            self.current_table.iloc[i-1,:] = mae.values # i-1 because first in list is the target(made by reader)
    
    def _check_or_make_dir(self, dir_name):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        return dir_name