# coding: utf-8

import numpy as np
from numpy.random import *
import random
import pickle
import datetime

def simple_moving_average(marmoset_agent):
    marmoset_agent_sma = np.zeros(shape=(191,2))
    b=np.ones(10)/10 # N of smoothing points, here set 10.
    marmoset_agent_sma[:,0] = np.convolve(marmoset_agent[:,0],b,"valid") # x-axis
    marmoset_agent_sma[:,1] = np.convolve(marmoset_agent[:,1],b,"valid") # y-axis
    return marmoset_agent_sma

def cal_2d_distance(marmoset_agent_s):
    l_norm_s = len(marmoset_agent_s[0,0,:])
    norm_s = np.zeros(l_norm_s)
    for i in range(l_norm_s):
        a = marmoset_agent_s[0,:,i]
        b = marmoset_agent_s[-1,:,i]
        norm_s[i] = np.linalg.norm(a-b)
    return norm_s

def generate_agent(n_touch,mu,sigma_global,sigma_local,pi):
    marmoset_agent = np.zeros(shape=(200,2)) 
    marmoset_agent[0] = multivariate_normal(mu, sigma_global, 1)
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
    today_str = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    # mu = (500.0,500.0)
    mu = (0,0)
    sd_global = 250
    ratio_s = [i * 0.1 for i in range(1,11)] # ratio = sd_local_sd_global, set from 0.1 to 1 by 0.1.
    sigma_global = [[sd_global**2,0],[0,sd_global**2]]
    iteration_n = 10000
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