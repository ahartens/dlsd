import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.cm as cm
import numpy as np
from .experiment_output_reader.Experiment_Output_Reader import Experiment_Output_Reader

class Experiment_Grapher:
    '''
        example of usage : (where reader has been created before)
        grapher = Experiment_Grapher_Multiple_IO_Params()
        grapher.set_experiment_reader(single_reader)
        grapher.set_time_window_to_graph(0,int(1440*3))
        grapher.set_target_column_idx(0)
        grapher.plot_predictions_and_target_for_model_with_name('single_hidden_layer_50')
    '''
    def __init__(self):
        self.experiment_output_reader = None
        self.colors = None
        self.model_name = None
        self.io_param_name = None
        self.target_column_idx = None
        self.plot_title = None
        
    def set_experiment_reader(self, reader):
        self.experiment_output_reader = reader
    
    def set_time_window_to_graph(self, s,e):
        self.s = s
        self.e = e
    
    def set_target_column_idx(self,idx):
        self.target_column_idx = idx
    
    def set_model_name(self, name):
        self.model_name = name
    
    def set_io_param_name(self, name):
        self.io_param_name = name
    
    def plot_predictions_and_target_for_model_with_name(self, name):
        self.model_name = name
        dicts = self.experiment_output_reader.get_predictions_and_target_for_model_name(name)
        self.plot_title = self.model_name + " for " + dicts[0]['df'].columns.values[self.target_column_idx]
        self.plot_list_of_dicts_with_name_and_df(dicts)
        self.plot_legend_with_list_of_dicts_with_name_and_df(dicts)

    def plot_list_of_dicts_with_name_and_df(self, dicts):
        self.create_colors_array_of_length(len(dicts))
        plt.figure(num=None, figsize=(20, 6), dpi=80, facecolor='w', edgecolor='k')
        plt.title(self.plot_title)
        for i in range(len(dicts)):
            df = dicts[i]['df']
            plt.plot(df.iloc[self.s:self.e,self.target_column_idx].values,color=self.colors[i])
    
    def plot_legend_with_list_of_dicts_with_name_and_df(self,dicts):
        legend_handles = []
        for i in range(len(dicts)):
            name = dicts[i]['name']
            patch = mpatches.Patch(color=self.colors[i], label=name)
            legend_handles.append(patch)
        plt.legend(handles=legend_handles)

    def create_colors_array_of_length(self, length):
        self.colors = cm.rainbow(np.linspace(0, 1, length))
