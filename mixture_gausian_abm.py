# coding: utf-8

import numpy as np
from numpy.random import *
import random
import pickle
import datetime

def simple_moving_average(marmoset_agent):
    # calculating the simple moving averages (SMAs) of the consecutive 10 points. In our simulations, we generate 200 points (containing x and y coordinates) of simulated marmoset touch locations; therefore, 191 values of SMAs are calculated. 
    marmoset_agent_sma = np.zeros(shape=(191,2)) # set zero vectors to be stored SMAs.
    b=np.ones(10)/10 # N of smoothing points, here set 10.
    marmoset_agent_sma[:,0] = np.convolve(marmoset_agent[:,0],b,"valid") # x-axis
    marmoset_agent_sma[:,1] = np.convolve(marmoset_agent[:,1],b,"valid") # y-axis
    return marmoset_agent_sma

def cal_2d_distance(marmoset_agent_s):
    # calculating the 2D distance between the first touch locations and the i-th locations. This script is not used for our simulations.
    
    l_norm_s = len(marmoset_agent_s[0,0,:]) # get the size of the vector of simulated marmoset agent.

    norm_s = np.zeros(l_norm_s) # make zero vector for saving the 2D distances calculated below.
    # loop for calculating the 2D distances between 1-st location and i-th location.
    
    for i in range(l_norm_s):
        a = marmoset_agent_s[0,:,i]
        b = marmoset_agent_s[-1,:,i]
        norm_s[i] = np.linalg.norm(a-b) # compute 2D distance and save to the vector.
    
    return norm_s

def generate_agent(n_touch,mu,sigma_global,sigma_local,pi):
    # argolisms generating the new locations depending on the previous locations.

    # First, making a vector for saving the locations.
    marmoset_agent = np.zeros(shape=(200,2)) 

    # The first locations is generated from the bivariate Gaussian distributions (mean:= mu, standard deviation:= sigma_global).
    marmoset_agent[0] = multivariate_normal(mu, sigma_global, 1)

    # loop generating the next location by generate_next_dot() methods.
    for i in range(1,200):
        if i <= 10:
            marmoset_agent[i] = generate_next_dot(marmoset_agent[:i],mu,sigma_global,sigma_local,pi) 
        else:
            marmoset_agent[i] = generate_next_dot(marmoset_agent[i-10-1:i],mu,sigma_global,sigma_local,pi)
    return marmoset_agent

def generate_next_dot(marmoset_agent,mu,sigma_global,sigma_local,pi):
    state = np.random.choice([1,0],1,p=[pi,1-pi])
    if state:
        new_dot = multivariate_normal(mu, sigma_global, 1)
    else:
        attend_dot = marmoset_agent[np.random.choice(marmoset_agent.shape[0]), :]
        new_dot = multivariate_normal(attend_dot, sigma_local, 1)
    return new_dot

def mk_pi_s(r):
    if r == 0.1:
        pi_s = [i * 0.01 for i in range(21)]
        pi_s.extend([j * 0.1 for j in range(3,11)])
    else:
        pi_s = [i * 0.1 for i in range(11)]
    return pi_s

def main():
    # main process of simulations.

    # Get the date-time info when we simulated.
    today_str = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    # set mean parameter (for bivariate Gaussian distribution) as (0,0). 
    mu = (0,0)

    # set global (large) standard deviation parameter (for bivariate Gaussian distribution) as 250.
    sd_global = 250

    # make the lists of ratio parameter. ratio := sd_local/sd_global, set from 0.1 to 1 by 0.1. E.g., when ratio = 0.1, the local (small) standard deviation parameter is 250 x 0.1 = 25.
    ratio_s = [i * 0.1 for i in range(1,11)]

    # define the covariance matrix of bivariate Gaussian distribution.
    sigma_global = [[sd_global**2,0],[0,sd_global**2]]

    # iteration number for the simulations.
    iteration_n = 10000

    # main loop for the simulation
    for n, r in enumerate(ratio_s):
        print('start r = %f' %r)
        sigma_local = [[(sd_global * r) ** 2,0],[0,(sd_global * r) ** 2]]
        pi_s = mk_pi_s(r)
        sma_sd_s = np.zeros(shape=(2,iteration_n,len(pi_s))) # prepare np array for SD values (dim=1), axis (dim=2), and pi values (dim=3).
        marmoset_agent_s = np.zeros(shape=(200,2,iteration_n,len(pi_s)))
        for k, pi in enumerate(pi_s):
            print("start pi = %f" %pi)
            for i in range(iteration_n):
                marmoset_agent = generate_agent(200,mu,sigma_global,sigma_local,pi)
                marmoset_agent_s[:,:,i,k] = marmoset_agent
                sma_sd_s[:,i,k] = np.std(simple_moving_average(marmoset_agent),axis = 0)    
        with open('results/mixture_gausian_abm_sd_r%s_%s.pickle' % (str(n+1),today_str),'wb') as f_1:
            pickle.dump(sma_sd_s, f_1)
        with open('results/mixture_gausian_abm_agent_raw_r%s_%s.pickle' % (str(n+1), today_str),'wb') as f_2:
            pickle.dump(marmoset_agent_s,f_2)
    print('Simulation successfully saved')

if __name__ == '__main__':
    main()