#!/usr/bin/env python3
##########################################################################################
# Author: Jared L. Ostmeyer
# Date Started: 2018-11-09
# Purpose: High level T-cell receptor classification based on CDR3 sequences
##########################################################################################

##########################################################################################
# Libraries
##########################################################################################

import numpy as np
import tensorflow as tf

##########################################################################################
# Load data
##########################################################################################

# Load data
#
xs_tumor_val = np.load('bin/xs_tumor_val.npy')
ps_tumor_val = np.load('bin/ps_tumor_val.npy')
xs_tumor_train = np.load('bin/xs_tumor_train.npy')
ps_tumor_train = np.load('bin/ps_tumor_train.npy')

xs_nontumor_val = np.load('bin/xs_nontumor_val.npy')
ps_nontumor_val = np.load('bin/ps_nontumor_val.npy')
xs_nontumor_train = np.load('bin/xs_nontumor_train.npy')
ps_nontumor_train = np.load('bin/ps_nontumor_train.npy')

##########################################################################################
# Settings
##########################################################################################

step_size = 8
max_steps = 20
num_features = 5

num_filters = 1024

half_batch = 2048
learning_rate = 0.001

num_iterations = 100000000

##########################################################################################
# Operators
##########################################################################################

# Inputs
#
features = tf.placeholder(tf.float32, [2*half_batch, max_steps, num_features])
penalties = tf.placeholder(tf.float32, [2*half_batch, max_steps])
labels = tf.placeholder(tf.float32, [2*half_batch])

# Parameters
#
weights = tf.get_variable(
  'weights', [step_size, num_features, num_filters],
  initializer=tf.variance_scaling_initializer(scale=1.0, mode='fan_in', distribution='uniform', dtype=tf.float32),
  dtype=tf.float32
)
bias = tf.get_variable(
  'bias', [num_filters],
  initializer=tf.constant_initializer(0.0),
  dtype=tf.float32
)

# Evaluate features
#
filters = tf.nn.convolution(features, weights, padding='VALID')

# Aggregate filters
#
scores = tf.reduce_logsumexp(filters, axis=2)-tf.log(tf.cast(num_filters, tf.float32))

# Aggregate kmers
#
logits = tf.reduce_logsumexp(scores+penalties[:,step_size-1:], axis=1)-tf.log(tf.cast(15-step_size, tf.float32))
probabilities = tf.sigmoid(logits)

# Metrics
#
cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=logits, labels=labels))
corrects = tf.equal(tf.round(probabilities), tf.round(labels))
accuracy = tf.reduce_mean(tf.cast(corrects, tf.float32))

# Optimizer
#
index_step = tf.Variable(0, trainable=False)
optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost, global_step=index_step)

# Create operator to initialize session
#
initializer = tf.global_variables_initializer()

##########################################################################################
# Session
##########################################################################################

# Open session
#
with tf.Session() as session:

  # Initialize variables
  #
  session.run(initializer)

  # Iterative training procedure
  #
  for iteration in range(num_iterations):

    # Periodic report
    #
    if iteration%100 == 0:

      # Run the model and optimize
      #
      is_tumor_train = np.random.randint(xs_tumor_train.shape[0], size=half_batch)
      is_nontumor_train = np.random.randint(xs_nontumor_train.shape[0], size=half_batch)
      c_train, a_train, i_step = session.run(
        (cost, accuracy, index_step),
        feed_dict={
          features: np.concatenate(
            [ xs_tumor_train[is_tumor_train,:,:], xs_nontumor_train[is_nontumor_train,:,:] ]
          ),
          penalties: np.concatenate(
            [ ps_tumor_train[is_tumor_train,:], ps_nontumor_train[is_nontumor_train,:] ]
          ),
          labels: np.concatenate(
            [ np.ones(half_batch, dtype=np.float32), np.zeros(half_batch, dtype=np.float32) ]
          )
        }
      )

      # Run the model
      #
      is_tumor_val = np.random.randint(xs_tumor_val.shape[0], size=half_batch)
      is_nontumor_val = np.random.randint(xs_nontumor_val.shape[0], size=half_batch)
      c_val, a_val = session.run(
        (cost, accuracy),
        feed_dict={
          features: np.concatenate(
            [ xs_tumor_val[is_tumor_val,:,:], xs_nontumor_val[is_nontumor_val,:,:] ]
          ),
          penalties: np.concatenate(
            [ ps_tumor_val[is_tumor_val,:], ps_nontumor_val[is_nontumor_val,:] ]
          ),
          labels: np.concatenate(
            [ np.ones(half_batch, dtype=np.float32), np.zeros(half_batch, dtype=np.float32) ]
          )
        }
      )

      # Print report
      #
      print(
        'Batch:', i_step,
        'Cost (Train):', '%4.3f'%(c_train/np.log(2.0)),
        'Accuracy (Train):', '%4.3f'%(100.0*a_train),
        'Cost (Val):', '%4.3f'%(c_val/np.log(2.0)),
        'Accuracy (Val):', '%4.3f'%(100.0*a_val),
        flush=True
      )

    # Run the model and optimize
    #
    is_tumor_train = np.random.randint(xs_tumor_train.shape[0], size=half_batch)
    is_nontumor_train = np.random.randint(xs_nontumor_train.shape[0], size=half_batch)
    session.run(
      optimizer,
      feed_dict={
        features: np.concatenate(
          [ xs_tumor_train[is_tumor_train,:,:], xs_nontumor_train[is_nontumor_train,:,:] ]
        ),
        penalties: np.concatenate(
         [ ps_tumor_train[is_tumor_train,:], ps_nontumor_train[is_nontumor_train,:] ]
        ),
        labels: np.concatenate(
          [ np.ones(half_batch, dtype=np.float32), np.zeros(half_batch, dtype=np.float32) ]
        )
      }
    )

