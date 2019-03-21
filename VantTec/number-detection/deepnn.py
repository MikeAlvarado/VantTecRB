import tensorflow as tf
import numpy as np
import os
import fnmatch
import cv2
import sys
import tempfile
import math as m

def make_graph(x):
  """make_graph builds the graph for a deep net for classifying digits.
  Args:
    x: an input tensor with the dimensions (N_examples, 875), where 875 is 25 X 35.
  Returns:
    A tuple (y, keep_prob). y is a tensor of shape (N_examples, 3), with values
    equal to the logits of classifying the digit into one of 3 classes (the
    digits 1-3). keep_prob is a scalar placeholder for the probability of
    dropout.
  """
  # Reshape to use within a convolutional neural net.
  # Last dimension is for "features" - there is only one here, since images are
  # grayscale
  with tf.name_scope('reshape'):
    x_image = tf.reshape(x, [-1, 25, 35, 1])

  # First convolutional layer - maps one grayscale image to 32 feature maps.
  with tf.name_scope('conv1'):
    W_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

  # Pooling layer - downsamples by 2X.
  with tf.name_scope('pool1'):
    h_pool1 = max_pool_2x2(h_conv1)

  # Second convolutional layer -- maps 32 feature maps to 64.
  with tf.name_scope('conv2'):
    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

  # Second pooling layer.
  with tf.name_scope('pool2'):
    h_pool2 = max_pool_2x2(h_conv2)

  # Fully connected layer 1 -- after 2 round of downsampling, our 25x35 image
  # is down to 6x7x64 feature maps -- maps this to 1024 features.
  with tf.name_scope('fc1'):
    W_fc1 = weight_variable([7 * 9 * 64, 1024])
    b_fc1 = bias_variable([1024])

    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 9 * 64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

  # Dropout - controls the complexity of the model, prevents co-adaptation of
  # features.
  with tf.name_scope('dropout'):
    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

  # Map the 1024 features to 3 classes, one for each dock number (1,2,3)
  with tf.name_scope('fc2'):
    W_fc2 = weight_variable([1024, 3])
    b_fc2 = bias_variable([3])

    y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
  return y_conv, keep_prob

def conv2d(x, W):
  """conv2d returns a 2d convolution layer with full stride."""
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
  """max_pool_2x2 downsamples a feature map by 2X."""
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

def weight_variable(shape):
  """weight_variable generates a weight variable of a given shape."""
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  """bias_variable generates a bias variable of a given shape."""
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def train(data_set, save_location='saved_model'):
  x = tf.placeholder(tf.float32, [None, 875], name='img')

  # Define loss and optimizer
  y_ = tf.placeholder(tf.float32, [None, 3], name='actual')

  # Build the graph for the deep net
  y_conv, keep_prob = make_graph(x)

  with tf.name_scope('prediction'):
    predicted_y = tf.argmax(y_conv, 1)

  with tf.name_scope('loss'):
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits_v2(labels=y_, logits=y_conv)
  
  cross_entropy = tf.reduce_mean(cross_entropy)

  with tf.name_scope('adam_optimizer'):
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

  with tf.name_scope('accuracy'):
    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
    correct_prediction = tf.cast(correct_prediction, tf.float32)
  accuracy = tf.reduce_mean(correct_prediction)

  with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(2000):
      batch = data_set.batch(20)
      
      if i % 100 == 0:
        train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
        print('step %d, training accuracy %g' % (i, train_accuracy))
      
      train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
    
    test = data_set.test()

    print('Saving graph to: %s' % save_location)
    
    tf.saved_model.simple_save(sess, 
        save_location, 
        inputs={'img': x, 'dropout': keep_prob }, 
        outputs={'prediction': predicted_y})

    print('test accuracy %g' % accuracy.eval(feed_dict={x: test[0], y_: test[1], keep_prob: 1.0}))

def predict(img, model='saved_model'):
  #img = cv2.imread(img, 0)
 
  print(img.shape)

  predictor = tf.contrib.predictor.from_saved_model(model)
 
  res = predictor({ 'img': [img.flatten()], 'dropout': 1 })

  return res['prediction'][0] + 1

def main(argv):
  if argv[1] == 'train':
    print('Training set dir: {}'.format(argv[2]))
    data_set = TrainData(argv[2])
    
    if(len(argv) > 3):
      train(data_set, argv[3])
    else:
      train(data_set)
  elif argv[1] == 'predict':
    if len(argv) > 3:
      predict(argv[2], argv[3])
    else:
      predict(argv[2])
  else:
    print('Usage: {} [predict,train] (options)'.format(argv[0]))
    print('    options: predict <img> (<model>)')
    print('             train <dataset dir> (<save location>)')

class TrainData:
  def __init__(self, dir):
    self.files = []
    self.offset = 0
    
    if dir[-1] != '/':
      dir += '/'

    for file in os.listdir(dir):
      if fnmatch.fnmatch(file,'*.png'):
          self.files.append(dir + file)

    # Save floor(5%) + 1 of dataset for testing
    self.test_n = 1 + m.floor(len(self.files) * 0.05)
    self.train_n = len(self.files) - self.test_n

    print('Found {} images'.format(len(self.files)))
    print('Using {} for training'.format(self.train_n))
    print('Using {} for testing'.format(self.test_n))

  def batch(self, n):
    x = []
    y = []
    
    for i in range(self.offset, self.offset + n):
      i = i % self.train_n
      
      img = cv2.imread(self.files[i], 0)

      x.append(img.flatten())

      if self.files[i][-5] == '1':
        y.append([1,0,0])
      elif self.files[i][-5] == '2':
        y.append([0,1,0])
      else:
        y.append([0,0,1])
    
    self.offset += n

    return [x,y]

  def test(self):
    x = []
    y = []

    for i in range(self.train_n, self.train_n + self.test_n):
      img = cv2.imread(self.files[i], 0)
      
      x.append(img.flatten())

      if self.files[i][-5] == '1':
        y.append([1,0,0])
      elif self.files[i][-5] == '2':
        y.append([0,1,0])
      else:
        y.append([0,0,1])

    return [x,y]

if __name__ == '__main__':
  main(sys.argv)
