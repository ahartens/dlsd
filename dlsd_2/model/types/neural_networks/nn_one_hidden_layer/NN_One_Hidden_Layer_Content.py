from dlsd_2.model.types.neural_networks.decorators import tf_attributeLock
import tensorflow as tf
from dlsd_2.model.Model_Content import *

'''
    Simplest deep neural network that can be created

    Model is created in three steps for clarity.
    1. prediction : forward path through the neural network through a single hidden 
        layer to make an inference using a given input
    2. optimize : add derivative nodes to the graph and minimize the error using gradient descent
    3. error : compare prediction and target values
    tf_attributeLock decorator ensures that 1. operation nodes are only added to the graph
    once and that 2. nodes contained within are given a variable_scope name

    Alex Hartenstein 14/10/2016

==============================================================================
'''


class NN_One_Hidden_Layer_Content(Model_Content):
    
    def __init__(self, data, target, number_hidden_nodes, learning_rate, rnn_number_steps=None):
        super(NN_One_Hidden_Layer_Content, self).__init__()
        logging.debug("\tAdding NN_One_Hidden_Layer_Content")
        self.data_placeholder = data
        self.target_placeholder = target
        self.n_input = int(self.data_placeholder.get_shape()[1])
        self.n_hidden = number_hidden_nodes
        self.n_output = int(self.target_placeholder.get_shape()[1])
        self.learningRate = learning_rate
        self.rnn_number_steps = rnn_number_steps
        logging.info("NN_One_Hidden_Layer #input : %d   #hidden : %d   #output : %d   learningRate : %.2f"%(self.n_input,self.n_hidden,self.n_output,self.learningRate))
        self.addAttributes()

    def addAttributes(self):
        self.prediction
        self.error
        self.optimize
        self.evaluation
 
    @tf_attributeLock
    def prediction(self):
        logging.debug("Adding Prediction nodes to the graph")
        with tf.name_scope('layer1'):
            weights = tf.Variable(tf.truncated_normal((self.n_input,self.n_hidden),stddev=0.1), name="lay1_weights")
            bias = tf.Variable(tf.constant(0.1,shape=[self.n_hidden]), name = "lay1_bias")
            out_layer1 = tf.nn.sigmoid(tf.matmul(self.data_placeholder,weights)+bias, name = "lay1_output")
        with tf.name_scope('layer2'):
            weights = tf.Variable(tf.truncated_normal((self.n_hidden,self.n_output),stddev=0.1), name="lay2_weights")
            bias = tf.Variable(tf.constant(0.1,shape=[self.n_output]), name="lay2_bias")
            out_layer2 = tf.nn.sigmoid(tf.matmul(out_layer1,weights)+bias, name = "lay2_output")
        return out_layer2
       
    @tf_attributeLock
    def optimize(self):
        logging.debug("Adding Optimize nodes to the graph")
        optimizer = tf.train.GradientDescentOptimizer(self.learningRate, name = "gradientDescent")
        optimizer_op = optimizer.minimize(self.error,name="minimizeGradientDescent")
        return optimizer_op
    
    @tf_attributeLock
    def error(self):
        logging.debug("Adding Error nodes to the graph")
        # using l2 norm (sum of) square error
        final_error = tf.square(tf.sub(self.target_placeholder,self.prediction),name="myError")
        #tf.histogram_summary("final_error",final_error)
        mean = tf.reduce_mean(final_error,0)
        #tf.histogram_summary("mean_error",mean)
        return final_error

    @tf_attributeLock
    def evaluation(self):
        logging.debug("Adding Evaluation nodes to the graph")
        # using l2 norm (sum of) square error
        final_error = tf.abs(tf.sub(self.target_placeholder,self.prediction,name="myEvaluationError"))
        #tf.histogram_summary("evaluation_final_error",final_error)
        mean = tf.reduce_mean(final_error)
        #tf.scalar_summary("evaluation_mean_error",mean)
        return mean