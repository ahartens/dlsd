from dlsd_2.model.types.neural_networks.Neural_Network_Model import *
from .NN_One_Hidden_Layer_Content import NN_One_Hidden_Layer_Content


class NN_One_Hidden_Layer(Neural_Network_Model):

	def __init__(self):
		super(NN_One_Hidden_Layer,self).__init__()
		logging.info("Creating Neural Network with One Hidden Layer")
		self.name = "NN_One_Hidden_Layer"

	def _build_model(self):
	    self.graph = tf.Graph()
	    with self.graph.as_default(),tf.device('/cpu:0'):
	        self.input_pl = tf.placeholder(tf.float32,shape=[None,self.model_input.get_number_inputs()],name="input_placeholder")
	        self.target_pl = tf.placeholder(tf.float32,shape=[None,self.model_input.get_number_targets()],name="target_placeholder")
	        self.model_content = NN_One_Hidden_Layer_Content(data = self.input_pl,
	        											target = self.target_pl,
	        											number_hidden_nodes = self.number_hidden_nodes,
	        											learning_rate = self.learning_rate)
	        #self.summary_op = tf.merge_all_summaries()
	        self.saver = tf.train.Saver()
