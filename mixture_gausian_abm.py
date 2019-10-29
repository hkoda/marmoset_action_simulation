# coding: utf-8

import numpy as np
from numpy.random import *
import random
import pickle
import datetime

def simple_moving_average(touch_locs):
    # calculating the simple moving averages (SMAs) of the consecutive 10 points. 
    # In our simulations, we generate 200 points (containing x and y coordinates) 
    # of simulated marmoset touch locations; therefore, 191 values of SMAs are calculated. 
    touch_locs_sma = np.zeros(shape=(191,2)) # set zero vectors to be stored SMAs.
    b=np.ones(10)/10 # N of smoothing points, here set 10.
    touch_locs_sma[:,0] = np.convolve(touch_locs[:,0],b,"valid") # x-axis
    touch_locs_sma[:,1] = np.convolve(touch_locs[:,1],b,"valid") # y-axis
    return touch_locs_sma

def generate_touch_locs(n_touch,mu,sigma_global,sigma_local,pi):
    # algorithm generating the new locations depending on the previous locations.

    # First, making a vector for saving the locations.
    touch_locs = np.zeros(shape=(200,2)) 

    # The first locations is generated from the bivariate Gaussian distributions (mean:= mu, standard deviation:= sigma_global).
    touch_locs[0] = multivariate_normal(mu, sigma_global, 1)

    # loop generating the next location by generate_next_loc() methods.
    for i in range(1,200):
        if i <= 10:
            touch_locs[i] = generate_next_loc(touch_locs[:i],mu,sigma_global,sigma_local,pi) 
        else:
            touch_locs[i] = generate_next_loc(touch_locs[i-10-1:i],mu,sigma_global,sigma_local,pi)
    return touch_locs

def generate_next_loc(touch_locs,mu,sigma_global,sigma_local,pi):
    # method returns the next dot based on the preivous dots' place with the parameter pi, mixuture ratio.

    # Choice each of the two states (global or local process). The states are binary assined:
    # Global state:= 1, local state := 0.
    # The probabilities of each state is defined by the mixture ratio. 
    state = np.random.choice([1,0], size = 1, p = [pi,1-pi])

    # Case of global process.
    # Next dot is generated from the bivaiate Gaussian distributions with mean:= mu(here set as (0,0)) and standard deviations of global process (here set as 250).
    if state:
        new_loc = multivariate_normal(mu, sigma_global, 1)
    
    # Case of local process.
    # First, choose one dot ('attend dot') from the dots appeard on the monitor. 
    # Next, the new dot is generated from the bivariate Gaussian distribution with mean:= place of the attend dot and standard deviations of local process (here set as 250 * r)
    else:
        attend_loc = touch_locs[np.random.choice(len(touch_locs)), :]
        new_loc = multivariate_normal(attend_loc, sigma_local, 1)
    return new_loc

def mk_pi_s(r):
    # making the lists of mixture ratios, pi_s, here. 
    # Mixture ratio is the probablities to switch the two states of dot generations (i.e., global process or local process) for the next touch location generations.
    # For example, "pi = 0.1" means the probability that the next dot is generated from the global process is 10 %, while those from the local process is 90 %.
    # this method makes the list of pi_s := [0.01,0.02,0.03,....,0.1,0.2,0.3....,1].
    if r == 0.1:
        pi_s = [i * 0.01 for i in range(21)]
        pi_s.extend([j * 0.1 for j in range(3,11)])
    else:
        pi_s = [i * 0.1 for i in range(11)]
    return pi_s

def main():
    # Main process of simulations.

    # Get the date-time info when we simulated.
    today_str = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    # set mean parameter (for bivariate Gaussian distribution) as (0,0). 
    mu = (0,0)

    # set global (large) standard deviation parameter (for bivariate Gaussian distribution) as 250.
    sd_global = 250

    # ratio parameter. ratio(r) := sd_local/sd_global
    # i.e., when ratio = 0.1, the local (small) standard deviation parameter is 250 x 0.1 = 25. 
    r = 0.1

    # define the covariance matrix of bivariate Gaussian distribution.
    sigma_global = [[sd_global**2,0],[0,sd_global**2]]

    # iteration number for the simulations.
    iteration_n = 10000

    # define sigma_local, covariance matrix of the local process.
    sigma_local = [[(sd_global * r) ** 2,0],[0,(sd_global * r) ** 2]]

    # compute mixture ratio lists.
    pi_s = mk_pi_s(r)

    # prepare np array for SD values (dim=1), axis (dim=2), and pi values (dim=3).
    sma_sd_s = np.zeros(shape=(2,iteration_n,len(pi_s))) 
    touch_locs_s = np.zeros(shape=(200,2,iteration_n,len(pi_s)))

    # loop for each of the mixture ratios ('pi_s') of simulations
    for k, pi in enumerate(pi_s):
        print("start pi = %f" %pi)
        
        # sub-loop by iteration numbers
        for i in range(iteration_n):
            touch_locs = generate_touch_locs(200,mu,sigma_global,sigma_local,pi)
            touch_locs_s[:,:,i,k] = touch_locs
            # Finally compute the standard deviation of the simple moving avarage valuse of simulated marmoset places for each of mixture ratio, 'pi_s'
            sma_sd_s[:,i,k] = np.std(simple_moving_average(touch_locs),axis = 0) 

    # Save the simulation date in the 'results' directories. 
    # Results directory should be made prior to the simulations.
    with open('results/mixture_gausian_abm_sd_r1_%s.pickle' % today_str,'wb') as f_1:
        pickle.dump(sma_sd_s, f_1)
    with open('results/mixture_gausian_abm_agent_raw_r1_%s.pickle' % today_str,'wb') as f_2:
        pickle.dump(touch_locs_s,f_2)
    print('Simulation successfully saved')

if __name__ == '__main__':
    main()