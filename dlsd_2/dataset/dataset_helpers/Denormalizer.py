
class Denormalizer:
	
	def __init__(self,max_value):
		self.max_value = max_value

	def normalize(self,data):
		return ((data/self.max_value)*.99999999) + 0.00000001

	def denormalize(self,data):
		return (data/.99999999)*self.max_value