#!/usr/bin/env python3
import numpy as np
if not __file__.endswith('_em_gaussian.py'):
    print('ERROR: This file is not named correctly! Please name it as LastName_em_gaussian.py (replacing LastName with your last name)!')
    exit(1)

DATA_PATH = "/u/cs246/data/em/" #TODO: if doing development somewhere other than the cycle server (not recommended), then change this to the directory where your data file is (points.dat)
DATA_PATH = "/"

def parse_data(args):
    num = float
    dtype = np.float32
    data = []
    with open(args.data_file, 'r') as f:
        for line in f:
            data.append([num(t) for t in line.split()])
    dev_cutoff = int(.9*len(data))
    train_xs = np.asarray(data[:dev_cutoff],dtype=dtype)
    dev_xs = np.asarray(data[dev_cutoff:],dtype=dtype) if not args.nodev else None
    return train_xs, dev_xs

def init_model(args):
    # Randomly initialize model based on given number of clusters

    # Set seed
    seed = 12345

    if args.cluster_num:
        lambdas = np.zeros(args.cluster_num)
        mus = np.zeros((args.cluster_num,2))
        if not args.tied:
            sigmas = np.zeros((args.cluster_num,2,2))
        else:
            sigmas = np.zeros((2,2))
        #TODO: randomly initialize clusters (lambdas, mus, and sigmas)
        num_dim = 2 # Because the given data file has dimension of 2
        K = args.cluster_num

        # Uniform prior
        lambdas = np.tile(1/args.cluster_num,(K))
        # Set seed
        np.random.seed(seed)
        # Gerenate mu from uniform distribution
        mus = np.random.uniform(0,1,(mus.shape))
        
        if not args.tied:
            for k in range(K):
                sigmas[k] = np.eye(num_dim)
        else:
            # Returns a 2-D array with ones on the diagonal and zeros elsewhere.
            sigmas = np.eye(num_dim)
    # Initialize model using given file
    else:
        lambdas = []
        mus = []
        sigmas = []
        with open(args.clusters_file,'r') as f:
            for line in f:
                #each line is a cluster, and looks like this:
                #lambda mu_1 mu_2 sigma_0_0 sigma_0_1 sigma_1_0 sigma_1_1
                lambda_k, mu_k_1, mu_k_2, sigma_k_0_0, sigma_k_0_1, sigma_k_1_0, sigma_k_1_1 = map(float,line.split())
                lambdas.append(lambda_k)
                mus.append([mu_k_1, mu_k_2])
                sigmas.append([[sigma_k_0_0, sigma_k_0_1], [sigma_k_1_0, sigma_k_1_1]])
        lambdas = np.asarray(lambdas)
        mus = np.asarray(mus)
        sigmas = np.asarray(sigmas)
        args.cluster_num = len(lambdas)

    #TODO: do whatever you want to pack the lambdas, mus, and sigmas into the model variable (just a tuple, or a class, etc.)
    #NOTE: if args.tied was provided, sigmas will have a different shape
    model = (lambdas, mus, sigmas)
    return model

def train_model(model, train_xs, dev_xs, args):
    from scipy.stats import multivariate_normal
    #NOTE: you can use multivariate_normal like this:
    #probability_of_xn_given_mu_and_sigma = multivariate_normal(mean=mu, cov=sigma).pdf(xn)
    #TODO: train the model, respecting args (note that dev_xs is None if args.nodev is True)
    #initializations

    # Extract the number of data points
    num_data = train_xs.shape[0]
    # Extract the number of clusters
    K = args.cluster_num
    # Extract initial parameters
    lambdas, mus, sigmas = extract_parameters(model)
    # Initialize the ksi for all clusters
    ksi_matrix = np.zeros((num_data,K))

    # Initliaze lists to store ll (log-likelihood) for dev and train
    ll_train = []
    ll_dev = []

    
    for iteration in range(args.iterations):
        # Expectation step
        for k in range(K):
            if args.tied:
                ksi_matrix[:,k] = lambdas[k]*multivariate_normal.pdf(train_xs, mean=mus[k], cov=sigmas)
            else:
                ksi_matrix[:,k] = lambdas[k]*multivariate_normal.pdf(train_xs, mean=mus[k], cov=sigmas[k])

        # Normalization
        a = np.transpose(np.tile(ksi_matrix.sum(1),(K,1)))
        ksi_matrix = ksi_matrix/a

        # Maximization
        for k in range(K):
            # Update mu
            mus[k] = np.dot(ksi_matrix[:,k],train_xs)/np.sum(ksi_matrix[:,k])
            
            # Initialize for next step
            zero_mean = train_xs - mus[k]
            sum_ksi = np.sum(ksi_matrix[:,k])

            # Update lambda
            lambdas[k] = sum_ksi/num_data

            # Update sigma
            if args.tied:
                sigmas += np.dot(np.transpose(zero_mean)*ksi_matrix[:,k],zero_mean)
            else:
                sigmas[k] = np.dot(np.transpose(zero_mean)*ksi_matrix[:,k],zero_mean)/sum_ksi   

        # If the covariance matrix is the same
        if args.tied:
            sigmas = sigmas/num_data

        # Update model
        model = (lambdas, mus, sigmas)

        # Calculate log likelihood for training dataset
        ll_train.append(average_log_likelihood(model,train_xs,args))

        # If use dev dataset, calculate the log likelihood for dev dataset also
        if not args.nodev:
            ll_dev.append(average_log_likelihood(model,dev_xs,args))

    # # Plotting the change of log likelihood
    # import matplotlib.pyplot as plt
    # x = np.arange(0,args.iterations,1)
    # fig, ax = plt.subplots()
    # ax.plot(x, ll_train)
    # if not args.nodev:
    #     ax.plot(x, ll_dev)

    # titlename = 'Iteration = ' + str(args.iterations) + ', K = ' + str(args.cluster_num)

    # ax.set(xlabel='iterations', ylabel='Log Likelihood', title=titlename)

    # if not args.nodev: #if dev is true
    #     plt.legend(['train','dev'])
    # else:
    #     plt.legend('train')
    # plt.show()

    return model

def average_log_likelihood(model, data, args):
    from math import log
    from scipy.stats import multivariate_normal
    #TODO: implement average LL calculation (log likelihood of the data, divided by the length of the data)
    ll = 0.0

    lambdas, mus, sigmas = extract_parameters(model)
    K = args.cluster_num    
    num_data = data.shape[0]


    # ll = sum over z, p(X|Z = z, theta) *P(Z=z|theta)
    l_matrix = np.zeros((num_data,K))

    for k in range(K):
        if args.tied:
            l_matrix[:,k] = multivariate_normal.pdf(data, mean=mus[k], cov=sigmas)*lambdas[k]
        else:
            l_matrix[:,k] = multivariate_normal.pdf(data, mean=mus[k], cov=sigmas[k])*lambdas[k]

    sum_l_matrix = np.sum(l_matrix,1)
    ll = np.sum(np.log(sum_l_matrix))/num_data

    return ll

def extract_parameters(model):
    #TODO: extract lambdas, mus, and sigmas from the model and return them (same type and shape as in init_model)
    lambdas = model[0]
    mus = model[1]
    sigmas = model[2]

    return lambdas, mus, sigmas

def main():
    import argparse
    import os
    print('Gaussian') #Do not change, and do not print anything before this.
    parser = argparse.ArgumentParser(description='Use EM to fit a set of points.')
    init_group = parser.add_mutually_exclusive_group(required=True)
    init_group.add_argument('--cluster_num', type=int, help='Randomly initialize this many clusters.')
    init_group.add_argument('--clusters_file', type=str, help='Initialize clusters from this file.')
    parser.add_argument('--nodev', action='store_true', help='If provided, no dev data will be used.')
    parser.add_argument('--data_file', type=str, default=os.path.join(DATA_PATH, 'points.dat'), help='Data file.')
    parser.add_argument('--print_params', action='store_true', help='If provided, learned parameters will also be printed.')
    parser.add_argument('--iterations', type=int, default=1, help='Number of EM iterations to perform')
    parser.add_argument('--tied',action='store_true',help='If provided, use a single covariance matrix for all clusters.')
    args = parser.parse_args()
    if args.tied and args.clusters_file:
        print('You don\'t have to (and should not) implement tied covariances when initializing from a file. Don\'t provide --tied and --clusters_file together.')
        exit(1)

    train_xs, dev_xs = parse_data(args)
    model = init_model(args)
    model = train_model(model, train_xs, dev_xs, args)
    ll_train = average_log_likelihood(model, train_xs, args)
    print('Train LL: {}'.format(ll_train))
    if not args.nodev:
        ll_dev = average_log_likelihood(model, dev_xs, args)
        print('Dev LL: {}'.format(ll_dev))
    lambdas, mus, sigmas = extract_parameters(model)
    if args.print_params:
        def intersperse(s):
            return lambda a: s.join(map(str,a))
        print('Lambdas: {}'.format(intersperse(' | ')(np.nditer(lambdas))))
        print('Mus: {}'.format(intersperse(' | ')(map(intersperse(' '),mus))))
        if args.tied:
            print('Sigma: {}'.format(intersperse(' ')(np.nditer(sigmas))))
        else:
            print('Sigmas: {}'.format(intersperse(' | ')(map(intersperse(' '),map(lambda s: np.nditer(s),sigmas)))))

if __name__ == '__main__':
    main()
