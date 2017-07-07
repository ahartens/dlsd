import os
import pandas as pd

class Experiment_Output_Reader:
    def __init__(self):
        self.experiment_directory = None
        self.io_params = []        

    def set_experiment_output_directory(self, path):
        self.experiment_directory = path
   
    def extract_data(self):
        self._extract_necessary_file_paths_output_directory()
        self._read_target_data()
        self._read_predictions_data()
    
    def _extract_necessary_file_paths_output_directory(self):
        self._read_directory_and_find_io_param_paths()
        
    def _read_directory_and_find_io_param_paths(self):
        for root, dirs, files in os.walk(self.experiment_directory, topdown=True):
            for name in files:
                if name == "target.csv":
                    self._make_new_io_param_object(root)
    
    def _make_new_io_param_object(self,root_path):
        io_param = IO_Param_Output()
        io_param.set_path(root_path)
        self.io_params.append(io_param)
    
    def _read_target_data(self):
        for io_param in self.io_params:
            io_param.read_target_file()
        
    def _read_predictions_data(self):
        for io_param in self.io_params:
            io_param.read_prediction_files()

    def _read_prediction_file(self, root, name):
        path = os.path.join(root,name)
        df = pd.read_csv(path,index_col=0)
        return {'df':df, 'name':name.replace('.csv','')}
    
    def get_model_names(self):
        model_names = []
        io_param = self.io_params[0]
        for model_predictions in io_param.model_predictions:
            model_names.append(model_predictions.name)
        return model_names
    
    def get_io_param_names(self):
        names = []
        for io_param in self.io_params:
            names.append(io_param.name)
        return names
    
    def get_predictions_and_target_for_model_name(self, model_name):
        data = [{'df':self.io_params[0].target.df,'name':'Target'}]
        for io_param in self.io_params:
            for model_predictions in io_param.model_predictions:
                 if model_predictions.name == model_name:
                    data.append({'df':model_predictions.df,'name':io_param.name,'target':io_param.target.df})
        return data 

class Table:
    def __init__(self):
        self.root = None
        self.name = None
        self.path = None
        self.df = None
        
    def read_data(self):
        self.df = pd.read_csv(self.path,index_col=0)

class IO_Param_Output:
    def __init__(self):
        self.path = None
        self.name = None
        self.target = Table()
        self.model_predictions = []
    
    def set_path(self,path):
        self.path = path
        self.name = os.path.basename(os.path.normpath(path))
    
    def read_target_file(self):
        self.target.root = self.path
        self.target.name = "Target"
        self.target.path = os.path.join(self.path,"target.csv")
        self.target.read_data()
    
    def read_prediction_files(self):
        for root, dirs, files in os.walk(os.path.join(self.path,"predictions"), topdown=True):
            for name in files:
                self.make_new_prediction_table(root,name)

    def make_new_prediction_table(self, root, name):
        table = Table()
        table.name = name.replace(".csv","")
        table.path = os.path.join(root,name)
        table.root = root
        table.read_data()
        self.model_predictions.append(table)