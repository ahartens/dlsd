from dlsd_2.model.types.neural_networks.nn_one_hidden_layer.NN_One_Hidden_Layer_Content import *


class LSTM_One_Hidden_Layer_Content(NN_One_Hidden_Layer_Content):
    
    @tf_attributeLock
    def prediction(self):
        debugInfo(__name__,"Adding LSTM Prediction nodes to the graph")
        
        cell = tf.nn.rnn_cell.LSTMCell(num_units=self.n_hidden,state_is_tuple=True)
        
        outputs,last_states = tf.nn.dynamic_rnn(
            cell=cell,inputs=self.data,dtype=tf.float32)

        last_output = outputs[:,self.rnn_number_steps-1,:]
        # outputs contains an tensor with shape ( batch size, rnn_sequence_length , n_hidden)
        # only the rnn layers or connected! to create the output layer of proper size need a new activation function!
        # activation function for output layer
        with tf.name_scope('outputLayer'):
            weights = tf.Variable(tf.truncated_normal((self.n_hidden,self.n_output),stddev=0.1), name="lay2_weights")
            bias = tf.Variable(tf.constant(0.1,shape=[self.n_output]), name="lay2_bias")
            out_layer2 = tf.nn.sigmoid(tf.matmul(last_output,weights)+bias, name = "lay2_output")
        return out_layer2
    