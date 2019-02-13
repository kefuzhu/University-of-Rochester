#!/usr/bin/env python3
import numpy as np
from io import StringIO

# Signature: Kefu Zhu

NUM_FEATURES = 124 #features are 1 through 123 (123 only in test set), +1 for the bias
DATA_PATH = "/u/cs246/data/adult/" #TODO: if doing development somewhere other than the cycle server, change this to the directory where a7a.train, a7a.dev, and a7a.test are
# DATA_PATH = "adult/"

#returns the label and feature value vector for one datapoint (represented as a line (string) from the data file)
def parse_line(line):
    tokens = line.split()
    x = np.zeros(NUM_FEATURES)
    y = int(tokens[0])
    y = max(y,0) #treat -1 as 0 instead, because sigmoid's range is 0-1
    for t in tokens[1:]:
        parts = t.split(':')
        feature = int(parts[0])
        value = int(parts[1])
        x[feature-1] = value
    x[-1] = 1 #bias
    return y, x

#return labels and feature vectors for all datapoints in the given file
def parse_data(filename):
    with open(filename, 'r') as f:
        vals = [parse_line(line) for line in f]
        (ys, xs) = ([v[0] for v in vals],[v[1] for v in vals])
        return np.asarray([ys],dtype=np.float32).T, np.asarray(xs,dtype=np.float32).reshape(len(xs),NUM_FEATURES,1) #returns a tuple, first is an array of labels, second is an array of feature vectors

def init_model(args):
    w1 = None
    w2 = None

    if args.weights_files:
        with open(args.weights_files[0], 'r') as f1:
            w1 = np.loadtxt(f1)
        with open(args.weights_files[1], 'r') as f2:
            w2 = np.loadtxt(f2)
            w2 = w2.reshape(1,len(w2))
    else:
        #TODO (optional): If you want, you can experiment with a different random initialization. As-is, each weight is uniformly sampled from [-0.5,0.5).
        np.random.seed(args.seed)
        w1 = np.random.rand(args.hidden_dim, NUM_FEATURES) #bias included in NUM_FEATURES
        w2 = np.random.rand(1, args.hidden_dim + 1) #add bias column

    #At this point, w1 has shape (hidden_dim, NUM_FEATURES) and w2 has shape (1, hidden_dim + 1). In both, the last column is the bias weights.

    #TODO: Replace this with whatever you want to use to represent the network; you could use use a tuple of (w1,w2), make a class, etc.
    model = (w1,w2)

    return model

def train_model(model, train_ys, train_xs, dev_ys, dev_xs, args):
    #TODO: Implement training for the given model, respecting args
# 
    # If we use dev set
    if dev_xs is not None:
        import time
        # Record start time of experiment
        start = time.time()
        # Initialize variables to store the best experiment result
        best_error_iteration = None
        best_lr = None
        best_iter = None
        # Initialize the global best model (Use the original model)
        global_best_model = extract_weights(model)
        # Experiment with different learning rate
        for lr in args.lr:
            # Initialize the local variables for experiment result using current learning rate
            local_best_model = extract_weights(model)
            local_iter = None
            # Initialize a vector to store the current experiment result
            error_iteration = np.empty(args.iterations)
            print('Learning Rate = {}'.format(lr))
            print('-'*30)
            # Extract the weights
            w1,w2 = extract_weights(model)
            # Track the number of iterations
            num_iter = 1
            # While the number of iteractions does not go beyond the maximum
            while num_iter <= args.iterations:
                # Initialize the error variable to zero
                error = 0
                # Loop through each pair of (x,y) in the training dataset
                for x,y in zip(train_xs,train_ys):
                    # Feed forward
                    y_hat,hidden_layer,a1,a2 = forward(x,w1,w2)
                    # Error function: E = 0.5(y_hat - y)^2
                    error += (1/2) * np.power((y_hat - y), 2)
                    # Backpropagation
                    w1,w2 = backprop(x,y,y_hat,hidden_layer,w1,w2,a1,a2,lr)
                # Record the current error
                error_iteration[num_iter-1] = error
                # Show the training progress
                if args.iterations <= 10: #
                    print('Iteration #{}: {}.'.format(num_iter,float(np.round(error,2))))
                else:
                    if num_iter % round(args.iterations/10) == 0:
                        print('Iteration #{}: {}.'.format(num_iter,float(np.round(error,2))))
                # Increment the iteraction number
                num_iter += 1

                # Compare the performance between the current weight vector and the best weight vector so far
                if test_accuracy(local_best_model, dev_ys, dev_xs) < test_accuracy((w1,w2), dev_ys, dev_xs):
                    # Make a deep copy of the current weight vector and set it as the best local model
                    local_best_model = (np.copy(w1),np.copy(w2))
                    local_iter = num_iter
            
            # Print the accuracy of current best model
            print('Best model dev accuracy: {}'.format(test_accuracy(local_best_model, dev_ys, dev_xs)))
            print('-'*30)

            # If the current model is better than the global best model
            if test_accuracy(global_best_model, dev_ys, dev_xs) < test_accuracy(local_best_model, dev_ys, dev_xs):
                # Reset values of variables to store the best experiment result
                best_error_iteration = np.copy(error_iteration)
                best_lr = lr
                best_iter = local_iter
        # Record end time of experiment
        end = time.time()
        # Show the experiment time
        print('Experiment took {} minutes'.format(round((end-start)/60),2))
        # Print the accuracy of current best model
        print('Best model dev accuracy: {}, Learning Rate = {}, Iteration = {}'
              .format(test_accuracy(global_best_model, dev_ys, dev_xs),
                      best_lr,
                      best_iter))
        # Return the best model
        return global_best_model

    # If dev set is not used
    else:
        # Extract the weights
        w1,w2 = extract_weights(model)
        # Track the number of iterations
        num_iter = 1
        # Initialize the hidden layer (+1 for the bias term)
        # hidden_layer = np.ones(len(w1)+1)
        # While the number of iteractions does not go beyond the maximum
        while num_iter <= args.iterations:
            # Initialize the error variable to zero
            error = 0
            # Loop through each pair of (x,y) in the training dataset
            for x,y in zip(train_xs,train_ys):
                # Feed forward
                # y_hat,hidden_layer,a1,a2 = forward(x,hidden_layer,w1,w2)
                y_hat,hidden_layer,a1,a2 = forward(x,w1,w2)
                # Error function: E = 0.5(y_hat - y)^2
                error += (1/2) * np.power((y_hat - y), 2)
                # Backpropagation
                w1,w2 = backprop(x,y,y_hat,hidden_layer,w1,w2,a1,a2,args.lr)
            
            # Show the training progress
            if args.iterations <= 10: #
                print('Iteration #{}: {}.'.format(num_iter,float(np.round(error,2))))
            else:
                if num_iter % round(args.iterations/10) == 0:
                    print('Iteration #{}: {}.'.format(num_iter,float(np.round(error,2))))
            # Increment the iteraction number
            num_iter += 1
        # Model (w1,w2,hidden_layer) after the training
        model = (w1,w2)
    # Return the model
    return model

def forward(x,w1,w2):

    # Record a1
    a1 = np.dot(w1,x)
    # Construct the hidden layer (with bias term)
    hidden_layer = np.append(sigmoid(a1),1)
    # Record a2
    a2 = np.dot(w2,hidden_layer)
    # hidden_layer -> yhat
    y_hat = sigmoid(a2)

    return y_hat,hidden_layer,a1,a2

def backprop(x,y,y_hat,hidden_layer,w1,w2,a1,a2,lr):
    '''
    '''

    # 1-Hidden Layer Nerual Network Structure:
    # ----------------------------------------------------------------
    # x = z0
    # x*w1 = a1, sigmoid(a1) = z1 (hidden layer)
    # z1*w2 = a2, sigmoid(a2) = yhat

    # Step 1
    # ----------------------------------------------------------------
    # Calculate the gradient and update w2 (except the bias term)

    # (1) Error function: E = 0.5(y_hat - y)^2
    # (2) yhat = sigmoid(a2)
    # (3) a2 = w2·z1 (z1 = hidden_layer)

    # Chain Rule: dw2(E) = dyhat(E)·dw2(yhat)
    #                    = dyhat(E)·[da2(yhat)·dw2(a2)]
    #                    = delta_2·dw2(a2) 
    #             - delta_2 = dyhat(E)·da2(yhat)
    #               - dyhat(E) = yhat - y
    #               - da2(yhat) = sigmoid_derivative(yhat)
    #             - dw2(a2) = z1 (hidden_layer)

    # Step 2
    # ----------------------------------------------------------------
    # Calculate the gradient and update w1 (except the bias term)

    # Chain Rule: dw1(E) = da1(E)·dw1(a1)      
    #                    = [dz1(E)·da1(z1)]·dw1(a1)
    #                    = [da2(E)·dz1(a2)]·da1(z1)·dw1(a1)
    #                    = [da2(E)]·dz1(a2)·da1(z1)·dw1(a1)
    #                    = [dyhat(E)·da2(yhat)]·dz1(a2)·da1(z1)·dw1(a1)
    #                    = delta_2·dz1(a2)·da1(z1)·dw1(a1)
    #                    = delta_1·dw1(a1)
    #             - delta_1 = delta_2·dz1(a2)·da1(z1)
    #               - delta_2 = see Step 1
    #               - dz1(a2) = w2 (Note: we need to trim away the bias term from w2)
    #               - da1(z1) = sigmoid_derivative(a1)
    #             - dw1(a1) = z0 (x)

    delta_2 = np.dot((y_hat - y), sigmoid_derivative(a2))
    dw2 = delta_2 * hidden_layer
    delta_1 = (np.transpose(w2)[:-1] * delta_2) * sigmoid_derivative(a1)
    dw1 = np.dot(delta_1, np.transpose(x))

    w1 = w1 - lr * dw1
    w2 = w2 - lr * dw2

    return w1,w2

def sigmoid(x):
    '''
    This function takes an input and transforms it using sigmoid function
    '''

    # return the sigmoid transformation
    return 1/(1+np.exp(-x))

def sigmoid_derivative(x):
    '''
    This function takes an input and return the derivative of its sigmoid function
    '''

    # return the derivative
    return (1-sigmoid(x))*sigmoid(x) 

def test_accuracy(model, test_ys, test_xs):
    accuracy = 0.0
    #TODO: Implement accuracy computation of given model on the test data

    # Extract the weight vector from model
    w1,w2 = extract_weights(model)

    # Predict the value of y for test dataset based on given weight vector
    test_yhat = [forward(x,w1,w2)[0] for x in test_xs]
    
    # Convert the prediction probablity to [0,1]
    test_yhat = [0 if yhat <= 0.5 else 1 for yhat in test_yhat]
    # Format test_yhat to be the same as test_ys
    test_yhat = np.transpose(np.array([test_yhat]))    
    # Compute the classification accuracy in the test set
    accuracy = float(sum(test_yhat == test_ys)/len(test_ys))

    # Return the accuracy
    return accuracy


def extract_weights(model):
    w1 = None
    w2 = None
    #TODO: Extract the two weight matrices from the model and return them (they should be the same type and shape as they were in init_model, but now they have been updated during training)
    w1,w2 = model
    return (w1,w2)

def main():
    import argparse
    import os

    parser = argparse.ArgumentParser(description='Neural network with one hidden layer, trainable with backpropagation.')
    parser.add_argument('--nodev', action='store_true', default=False, help='If provided, no dev data will be used.')
    parser.add_argument('--iterations', type=int, default=5, help='Number of iterations through the full training data to perform.')
    parser.add_argument('--lr', type=float, default=0.1, help='Learning rate to use for update in training loop.')

    weights_group = parser.add_mutually_exclusive_group()
    weights_group.add_argument('--weights_files', nargs=2, metavar=('W1','W2'), type=str, help='Files to read weights from (in format produced by numpy.savetxt). First is weights from input to hidden layer, second is from hidden to output.')
    weights_group.add_argument('--hidden_dim', type=int, default=5, help='Dimension of hidden layer.')
    weights_group.add_argument('--seed', type=int, default=123, help='Seed for randomization.')

    parser.add_argument('--print_weights', action='store_true', default=False, help='If provided, print final learned weights to stdout (used in autograding)')

    parser.add_argument('--train_file', type=str, default=os.path.join(DATA_PATH,'a7a.train'), help='Training data file.')
    parser.add_argument('--dev_file', type=str, default=os.path.join(DATA_PATH,'a7a.dev'), help='Dev data file.')
    parser.add_argument('--test_file', type=str, default=os.path.join(DATA_PATH,'a7a.test'), help='Test data file.')


    args = parser.parse_args()

    """
    At this point, args has the following fields:

    args.nodev: boolean; if True, you should not use dev data; if False, you can (and should) use dev data.
    args.iterations: int; number of iterations through the training data.
    args.lr: float; learning rate to use for training update.
    args.weights_files: iterable of str; if present, contains two fields, the first is the file to read the first layer's weights from, second is for the second weight matrix.
    args.hidden_dim: int; number of hidden layer units. If weights_files is provided, this argument should be ignored.
    args.train_file: str; file to load training data from.
    args.dev_file: str; file to load dev data from.
    args.test_file: str; file to load test data from.
    """
    train_ys, train_xs = parse_data(args.train_file)
    dev_ys = None
    dev_xs = None
    if not args.nodev:
        dev_ys, dev_xs= parse_data(args.dev_file)
    test_ys, test_xs = parse_data(args.test_file)

    model = init_model(args)
    model = train_model(model, train_ys, train_xs, dev_ys, dev_xs, args)
    accuracy = test_accuracy(model, test_ys, test_xs)
    print('Test accuracy: {}'.format(accuracy))
    if args.print_weights:
        w1, w2 = extract_weights(model)
        with StringIO() as weights_string_1:
            np.savetxt(weights_string_1,w1)
            print('Hidden layer weights: {}'.format(weights_string_1.getvalue()))
        with StringIO() as weights_string_2:
            np.savetxt(weights_string_2,w2)
            print('Output layer weights: {}'.format(weights_string_2.getvalue()))

if __name__ == '__main__':
    main()
