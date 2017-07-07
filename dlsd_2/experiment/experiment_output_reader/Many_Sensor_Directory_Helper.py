import os

class Many_Sensor_Directory_Helper:
    def __init__(self):
        self.root_experiment_directory = None
        self.all_sensor_dirs = None
        self.current_sensor_dir = None
        
    def set_root_experiment_directory(self, path):
        self.root_experiment_directory = path

    def prepare_list_of_all_sensors_to_analyze(self):
        self.all_sensor_dirs = next(os.walk(self.root_experiment_directory))[1]
        if ("avg_errors" in self.all_sensor_dirs):
            self.all_sensor_dirs.remove("avg_errors")

    def set_current_sensor_directory_with_sensor(self, sensor):
        self.current_sensor_dir = os.path.join(self.root_experiment_directory,str(sensor))

    def make_current_error_directory(self):
        path = self.get_current_error_directory()
        if not os.path.exists(path):
            os.makedirs(path)
        return path
    
    def get_current_error_directory(self):
        return os.path.join(self.current_sensor_dir,"error")
    
    def _check_or_make_dir(self, dir_name):
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        return dir_name