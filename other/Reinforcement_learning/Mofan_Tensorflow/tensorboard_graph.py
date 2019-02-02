#!/usr/bin/env python

with tf.name_scope('inputs'):

with tf.name_scope('layer'):
    with tf.name_scope('weight')


with tf.name_scope('loss'):
    loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys-prediction),
        reduction_indices=[1]))

with tf.name_scope('train'):
    train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)


sess = tf.Session()
writer = tf.train.SummaryWriter("logs/",sess.graph)
