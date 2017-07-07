import tensorflow as tf



'''
	Called within a machine learning model before defining a model attribute. Has two purposes:

	1. Ensures that a model attribute is only added to the tensorflow graph ONCE
	2. Creates a variable_scope for the graph nodes defined within the enclosed attribute

	source : https://danijar.com/structuring-your-tensorflow-models/

	Alex Hartenstein 14/10/2016

'''

import functools
def tf_attributeLock(function):
    attribute = '_cache_' + function.__name__
    @property
    @functools.wraps(function)
    def decorator(self):
        if not hasattr(self,attribute):
            with tf.variable_scope(function.__name__):
                setattr(self,attribute,function(self))
        return getattr(self,attribute)
    return decorator