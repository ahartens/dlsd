import pandas as pd
import numpy as np
class Adjacency_Matrix:
    def __init__(self):
        self.df = None
        self.subset_df = None
        
    def set_matrix_from_file_path(self, path):
        self.df = pd.read_csv(path,index_col = 0)
        self.convert_idx_and_cols_of_df_to_string(self.df)

    def subset_sensors(self, list_of_strs):
        self.check_sensors_in_adjacency(list_of_strs)
        self.subset_df = self.df[list_of_strs]
    
    def get_adjacency_for_sensor(self, sensor):
        row = self.subset_df.loc[sensor]
        row = row.reshape([1,-1])
        return row

    def convert_idx_and_cols_of_df_to_string(self, the_df):
        the_df.columns = [str(x) for x in the_df.columns.values]
        the_df.index = [str(x) for x in the_df.index.values]

    def check_sensors_in_adjacency(self, sensors):
        not_in_adj = []
        for sensor in sensors:
            if sensor not in self.df.columns.values:
                not_in_adj.append(sensor)
        if len(not_in_adj) != 0:
            self.add_zeros_for_sensors_not_in_adjacency(not_in_adj)
            
    def add_zeros_for_sensors_not_in_adjacency(self,not_in_adj):
        new_size = self.df.shape[1] + len(not_in_adj)
        new_names =  np.concatenate((self.df.columns.values,np.array(not_in_adj)),axis=0)
        new_df = pd.DataFrame(np.zeros([new_size, new_size],dtype=np.int64))
        new_df.columns = new_names
        new_df.index = new_names
        new_df.iloc[0:self.df.shape[0], 0:self.df.shape[1]] = self.df.values
        self.df = new_df