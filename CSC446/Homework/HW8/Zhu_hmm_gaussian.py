#!/usr/bin/env python3
import numpy as np
if not __file__.endswith('_hmm_gaussian.py'):
    print('ERROR: This file is not named correctly! Please name it as Lastname_hmm_gaussian.py (replacing Lastname with your last name)!')
    exit(1)

DATA_PATH = "/u/cs246/data/em/" #TODO: if doing development somewhere other than the cycle server (not recommended), then change this to the directory where your data file is (points.dat)

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
    if args.cluster_num:
        mus = np.zeros((args.cluster_num,2))
        if not args.tied:
            sigmas = np.zeros((args.cluster_num,2,2))
        else:
            sigmas = np.zeros((2,2))
        transitions = np.zeros((args.cluster_num,args.cluster_num)) #transitions[i][j] = probability of moving from cluster i to cluster j
        initials = np.zeros(args.cluster_num) #probability for starting in each state
        #TODO: randomly initialize clusters (mus, sigmas, initials, and transitions)

        # Set seed
        seed = 12345
        np.random.seed(seed)

        # Initialize mu
        mus = np.random.rand(args.cluster_num, 2)
        # Initialize sigmas
        if not args.tied:
            sigmas = np.array([np.eye(2) for i in range(args.cluster_num)])
        else:
            sigmas = np.eye(2)
        # Initialize transition matrix
        transitions = np.random.rand(args.cluster_num,args.cluster_num)
        # Normalize each row to have sum of 1
        transitions = transitions/transitions.sum(axis=1,keepdims=1)
        # Initialize initial distribution
        initials = np.array([1/args.cluster_num for i in range(args.cluster_num)])

    else:
        mus = []
        sigmas = []
        transitions = []
        initials = []
        with open(args.clusters_file,'r') as f:
            for line in f:
                #each line is a cluster, and looks like this:
                #initial mu_1 mu_2 sigma_0_0 sigma_0_1 sigma_1_0 sigma_1_1 transition_this_to_0 transition_this_to_1 ... transition_this_to_K-1
                vals = list(map(float,line.split()))
                initials.append(vals[0])
                mus.append(vals[1:3])
                sigmas.append([vals[3:5],vals[5:7]])
                transitions.append(vals[7:])
        initials = np.asarray(initials)
        transitions = np.asarray(transitions)
        mus = np.asarray(mus)
        sigmas = np.asarray(sigmas)
        args.cluster_num = len(initials)

    #TODO: Do whatever you want to pack mus, sigmas, initals, and transitions into the model variable (just a tuple, or a class, etc.)
    model = {'initials':initials, 'transitions':transitions, 'mus':mus, 'sigmas':sigmas}

    return model

def emission(x, mu, sigma):
    from scipy.stats import multivariate_normal
    # Compute the emission probability based on gaussian distribution
    # print('mu:{}'.format(mu))
    # print('sigma:{}'.format(sigma))
    return multivariate_normal.pdf(x, mean=mu, cov=sigma)

def forward(model, data, args):
    from scipy.stats import multivariate_normal
    from math import log
    alphas = np.zeros((len(data),args.cluster_num))
    log_likelihood = 0.0
    #TODO: Calculate and return forward probabilities (normalized at each timestep; see next line) and log_likelihood
    #NOTE: To avoid numerical problems, calculate the sum of alpha[t] at each step, 
    #      normalize alpha[t] by that value, and increment log_likelihood by the log of the value you normalized by.
    #      This will prevent the probabilities from going to 0, and the scaling will be cancelled out in 
    #      train_model when you normalize (you don't need to do anything different than what's in the notes). 
    #      This was discussed in class on April 3rd.

    # Extract model parameters
    initials, transitions, mus, sigmas = extract_parameters(model)

    # Forward
    for t in range(len(data)):
        # Base case (First observation)
        if t == 0:
            for i in range(args.cluster_num):
                if not args.tied:
                    alphas[t,i] = initials[i] * emission(x=data[t], mu=mus[i], sigma=sigmas[i])
                else:
                    alphas[t,i] = initials[i] * emission(x=data[t], mu=mus[i], sigma=sigmas)
        # Dynamic programming
        else:
            for i in range(args.cluster_num):
                if not args.tied:
                    # ∑jP(Xt|Zt=i)⋅P(Zt=i|Zt−1=j)⋅α(t−1,j)
                    alphas[t,i] = np.sum(alphas[t-1,:] * transitions[:,i]) * emission(x=data[t], mu=mus[i], sigma=sigmas[i])
                else:
                    # ∑jP(Xt|Zt=i)⋅P(Zt=i|Zt−1=j)⋅α(t−1,j)
                    alphas[t,i] = np.sum(alphas[t-1,:] * transitions[:,i]) * emission(x=data[t], mu=mus[i], sigma=sigmas)

        # # Normalization
        Z = np.sum(alphas[t,:])
        alphas[t,:] = alphas[t,:]/Z
        # Compute and add the log likelihood
        log_likelihood = log_likelihood + np.log(Z)

    return alphas, log_likelihood

def backward(model, data, args):
    from scipy.stats import multivariate_normal
    betas = np.zeros((len(data),args.cluster_num))
    #TODO: Calculate and return backward probabilities (normalized like in forward before)
    
    # Extract model parameters
    initials, transitions, mus, sigmas = extract_parameters(model)

    # Base case β(T,i)=1
    betas[len(data)-1,:] = 1

    # Backward
    for t in reversed(range(len(data)-1)):
        for i in range(args.cluster_num):
            # Dynamic programming
            tmp_beta = 0
            for j in range(args.cluster_num):
                if not args.tied:
                    # ∑jβ(t+1,j)⋅P(Xt+1|Zt+1=j)⋅P(Zt+1=j|Zt=i)
                    tmp_beta += betas[t+1,j] * transitions[i,j] * emission(x=data[t+1], mu=mus[j], sigma=sigmas[j])
                else:
                    tmp_beta += betas[t+1,j] * transitions[i,j] * emission(x=data[t+1], mu=mus[j], sigma=sigmas)
                
            # Assign the sum of probabily from all states
            betas[t,i] = tmp_beta
        # Normalization
        betas[t,:] = betas[t,:]/np.sum(betas[t,:])

    return betas

def train_model(model, train_xs, dev_xs, args):
    from scipy.stats import multivariate_normal
    #TODO: train the model, respecting args (note that dev_xs is None if args.nodev is True)

    # Extract the number of data points
    num_data = train_xs.shape[0]
    # Extract the number of clusters (number of hidden states)
    K = args.cluster_num
    # Extract initial parameters
    initials, transitions, mus, sigmas = extract_parameters(model)

    # Initliaze lists to store ll (log-likelihood) for dev and train
    ll_train = []
    ll_dev = []

    for num_iter in range(args.iterations):
        ####################
        # Expectation step #
        ####################

        # Forward
        alphas,_ = forward(model, train_xs, args)
        # Backward
        betas = backward(model, train_xs, args)
        # Initialize the ksi matrix
        ksi_matrix = np.zeros((num_data,K,K))
        # Initialize the gamma matrix 
        gamma_matrix = np.zeros((num_data,K))

        for t in range(num_data):
            for i in range(K):
                gamma_matrix[t,i] = alphas[t,i] * betas[t,i]

            for i in range(K):
                for j in range(K):
                    if t != 0:
                        ksi_matrix[t,i,j] = alphas[t-1,i] * betas[t,j] * transitions[i,j] * emission(x=train_xs[t], mu=mus[j], sigma=sigmas[j])
            # Normalization
            gamma_matrix[t,] = gamma_matrix[t,]/np.sum(gamma_matrix[t,])
            if t!=0:
                ksi_matrix[t,] = ksi_matrix[t,]/np.sum(ksi_matrix[t,])

        #####################
        # Maximization step #
        #####################

        # Update

        # Update initial distribution
        initials = gamma_matrix[0,]
        for i in range(args.cluster_num):
            # Update mu
            mus[i] = np.dot(gamma_matrix[:,i], train_xs) / np.sum(gamma_matrix[:,i])
            # Update sigma
            if not args.tied:
                sigmas[i] = np.dot(gamma_matrix[:,i] * (train_xs - mus[i]).T, (train_xs - mus[i])) / np.sum(gamma_matrix[:,i])
            else:
                sigmas += np.dot(gamma_matrix[:,i] * (train_xs - mus[i]).T, (train_xs - mus[i]))
            # Update transition matrix
            for j in range(args.cluster_num):
                transitions[i,j] = np.sum(ksi_matrix[:,i,j]) / np.sum(gamma_matrix[:,i])

        if args.tied:
            sigmas = sigmas / train_xs.shape[0]

        # Update model
        model = {'initials':initials, 'transitions':transitions, 'mus':mus, 'sigmas':sigmas}

        # Calculate log likelihood for training dataset
        ll_train.append(average_log_likelihood(model,train_xs,args))

        # If use dev dataset, calculate the log likelihood for dev dataset also
        if not args.nodev:
            ll_dev.append(average_log_likelihood(model,dev_xs,args))

        # Show the training progress
        if args.iterations <= 10: #
            print('Iteration #{}'.format(num_iter))
        else:
            if num_iter % round(args.iterations/10) == 0:
                print('Iteration #{}'.format(num_iter))
            elif num_iter == (args.iterations - 1):
                print('Iteration #{}'.format(num_iter+1))

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
    #TODO: implement average LL calculation (log likelihood of the data, divided by the length of the data)
    #NOTE: yes, this is very simple, because you did most of the work in the forward function above
    ll = 0.0

    _,log_likelihood = forward(model, data, args)

    ll = log_likelihood / data.shape[0]

    return ll

def extract_parameters(model):
    #TODO: Extract initials, transitions, mus, and sigmas from the model and return them (same type and shape as in init_model)
    initials = model['initials']
    transitions = model['transitions']
    mus = model['mus']
    sigmas = model['sigmas']

    return initials, transitions, mus, sigmas

def main():
    import argparse
    import os
    print('Gaussian') #Do not change, and do not print anything before this.
    parser = argparse.ArgumentParser(description='Use EM to fit a set of points')
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
    nll_train = average_log_likelihood(model, train_xs, args)
    print('Train LL: {}'.format(nll_train))
    if not args.nodev:
        nll_dev = average_log_likelihood(model, dev_xs, args)
        print('Dev LL: {}'.format(nll_dev))
    initials, transitions, mus, sigmas = extract_parameters(model)
    if args.print_params:
        def intersperse(s):
            return lambda a: s.join(map(str,a))
        print('Initials: {}'.format(intersperse(' | ')(np.nditer(initials))))
        print('Transitions: {}'.format(intersperse(' | ')(map(intersperse(' '),transitions))))
        print('Mus: {}'.format(intersperse(' | ')(map(intersperse(' '),mus))))
        if args.tied:
            print('Sigma: {}'.format(intersperse(' ')(np.nditer(sigmas))))
        else:
            print('Sigmas: {}'.format(intersperse(' | ')(map(intersperse(' '),map(lambda s: np.nditer(s),sigmas)))))

if __name__ == '__main__':
    main()
