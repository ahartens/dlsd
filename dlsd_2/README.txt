# Alex Hartenstein

## How to run an experiment

1. create a subclass of 'Experiment'
2. override _define_source_maker and create a Source_Maker object
	- set file_path_train and file_path_test
	- speciy normalize, moving_average_window, fill_time_gaps, etc
3. override _define_models
	- create one or more Model objects. 
	- call add_model, passing the model as an argument
4. override _define_model_input_output_parameters
	- create a list containing one or more Model_Input_Output_Parameters objects
	- call set_input_output_parameters_list, passing the list as an argument
5. in the main python function, create an instance of your Experiment class
	- call set_experiment_root_path, passing the directory it sould write output to 
	- call run_experiment
