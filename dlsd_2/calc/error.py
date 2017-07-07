import numpy as np

def mae(prediction, target):
	''' 
		mean average error 
	'''
	return np.mean(np.absolute(prediction - target),axis=0)

def mape(prediction,target):
	''' 
		mean average percentage error 
	'''
	n = target.shape[0]
	return (100/float(n))*(np.sum(np.abs((target-prediction)/target),axis=0))


class Error_Function:
	def __init__(self):
		self.name = None

	def calc_error_with_prediction_and_target(self, prediction, target):
		raise NotImplementedError

class MAE(Error_Function):
	def __init__(self):
		self.name = "MAE"

	def calc_error_with_prediction_and_target(self, prediction, target):
		return mae(prediction,target)

class MAPE(Error_Function):
	def __init__(self):
		self.name = "MAPE"

	def calc_error_with_prediction_and_target(self, prediction, target):
		return mape(prediction,target)