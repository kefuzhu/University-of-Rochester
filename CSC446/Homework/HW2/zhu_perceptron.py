#!/usr/bin/python3
# Signature: Kefu Zhu
import numpy as np
#TODO: understand that you should not need any other imports other than those already in this file; if you import something that is not installed by default on the csug machines, your code will crash and you will lose points

NUM_FEATURES = 124 #features are 1 through 123 (123 only in test set), +1 for the bias
DATA_PATH = "/u/cs246/data/adult/" #TODO: if you are working somewhere other than the csug server, change this to the directory where a7a.train, a7a.dev, and a7a.test are on your machine

#returns the label and feature value vector for one datapoint (represented as a line (string) from the data file)
def parse_line(line):
    tokens = line.split()
    x = np.zeros(NUM_FEATURES)
    y = int(tokens[0])
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
        return np.asarray(ys), np.asarray(xs) #returns a tuple, first is an array of labels, second is an array of feature vectors

def perceptron(train_ys, train_xs, dev_ys, dev_xs, args):
    # Initialize weight vector to be all zeros
    weights = np.zeros(NUM_FEATURES)
    
    # TODO: implement perceptron algorithm here, respecting args
    
    # If we use dev set
    if dev_xs is not None:
        # Initialize best_weights to record the best weights so far based on the test on dev set
        best_weights = weights
    
    # Track the number of iterations
    num_iter = 0
    # While the number of iteractions does not go beyond the maximum
    while num_iter < args.iterations:
        # # Make a deep copy of weight vector before next iteration
        # old_weights = np.array([w for w in weights])
        # Loop through each pair of (x,y) in the training dataset
        for x,y in zip(train_xs,train_ys):
            # Classify current data point based on current weights
            y_hat = np.sign(np.dot(np.transpose(weights),x))
            # If we classify incorrectly
            if y_hat!=y:
                # Update the weight vector
                weights = np.add(weights,np.array(args.lr*y*x))
        
        # If the dev set has been used
        if dev_xs is not None:
            # Compare the performance between the current weight vector and the best weight vector so far
            if test_accuracy(best_weights, dev_ys, dev_xs) < test_accuracy(weights, dev_ys, dev_xs):
                # Make a deep copy of the current weight vector and set it as the best one
                best_weights = np.array([w for w in weights])
        
        # Increment the number of iteraction
        num_iter += 1
        # Print the progress
        if args.iterations <= 10: #
            print('# of iterations: {}'.format(num_iter))
        else:
            if num_iter % round(args.iterations/10) == 0:
                print('# of iterations: {}'.format(num_iter))

        
#         # If after the iteration, the weight vector has not been changed 
#         # (every data point is classified correctly)
#         if np.array_equal(old_weights,weights):
#             # Return the current weight vector
#             return weights

    # If the dev set is not used
    if dev_xs is None:
        # Return the current weight vector (result from the last iteration)
        return weights
    # If the dev set is used
    else:
        # Return the best weight vector among all iteration results
        return best_weights

def test_accuracy(weights, test_ys, test_xs):
    accuracy = 0.0

    # TODO: implement accuracy computation of given weight vector on the test data (i.e. how many test data points are classified correctly by the weight vector)

    # Predict the value of y for test dataset based on given weight vector
    test_yhat = [np.sign(np.dot(weights,x)) for x in test_xs]
    # Compute the classification accuracy in the test set
    accuracy = sum(test_yhat == test_ys)/len(test_ys)
    # Round the accuracy to 8 decimals
    accuracy = round(accuracy,8)

    return accuracy

def main():
    import argparse
    import os

    parser = argparse.ArgumentParser(description='Basic perceptron algorithm.')
    parser.add_argument('--nodev', action='store_true', default=False, help='If provided, no dev data will be used.')
    parser.add_argument('--iterations', type=int, default=50, help='Number of iterations through the full training data to perform.')
    parser.add_argument('--lr', type=float, default=1.0, help='Learning rate to use for update in training loop.')
    parser.add_argument('--train_file', type=str, default=os.path.join(DATA_PATH,'a7a.train'), help='Training data file.')
    parser.add_argument('--dev_file', type=str, default=os.path.join(DATA_PATH,'a7a.dev'), help='Dev data file.')
    parser.add_argument('--test_file', type=str, default=os.path.join(DATA_PATH,'a7a.test'), help='Test data file.')
    args = parser.parse_args()

    """
    At this point, args has the following fields:

    args.nodev: boolean; if True, you should not use dev data; if False, you can (and should) use dev data.
    args.iterations: int; number of iterations through the training data.
    args.lr: float; learning rate to use for training update.
    args.train_file: str; file name for training data.
    args.dev_file: str; file name for development data.
    args.test_file: str; file name for test data.
    """
    train_ys, train_xs = parse_data(args.train_file)
    dev_ys = None
    dev_xs = None
    if not args.nodev:
        dev_ys, dev_xs= parse_data(args.dev_file)
    test_ys, test_xs = parse_data(args.test_file)
    weights = perceptron(train_ys, train_xs, dev_ys, dev_xs, args)
    accuracy = test_accuracy(weights, test_ys, test_xs)
    print('Test accuracy: {}'.format(accuracy))
    print('Feature weights (bias last): {}'.format(' '.join(map(str,weights))))

if __name__ == '__main__':
    main()
