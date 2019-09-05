# coding: utf-8
# This script is prepared for the figure generation of the readme.md file. 
# Need numpy, matpotlib, scipy, PIL and graphiviz.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import multivariate_normal
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from graphviz import Digraph

def mk_graph():
    fontsize = '40'
    fontcolor = 'black'
    pw = '3'
    g = Digraph(comment = 'Graph',format='png')
    # g.attr(rankdir='LR')
    g.attr(dpi='300')
    # g.attr(margin='0.1') 

    g.node('a', '', image='process_global_first_touch.png',shape='none',
    fontsize = fontsize,
    fontcolor = fontcolor,
    # margin='0'
    )

    g.node('b', '', image='process_global_second_touch_both_global.png',shape='none',
    fontsize = fontsize,
    fontcolor = fontcolor,
    # margin='-10'
    )
    g.node('c', '', image='process_global_second_touch_local.png',shape='none',
    fontsize = fontsize,
    fontcolor = fontcolor
    )

    g.edge('a','b',penwidth = pw,label='π',fontsize=fontsize)
    g.edge('a','c',penwidth = pw,label='1- π',fontsize=fontsize)
    g.render('first_process')
    print('done.')

def mk_graph_loop():
    fontsize = '40'
    fontcolor = 'black'
    pw = '3'
    g = Digraph(comment = 'Graph',format='png')
    # g.attr(rankdir='LR')
    g.attr(dpi='300')
    # g.attr(margin='0.1') 

    g.node('0', '', image='process_n_1_status.png',shape='none',
    fontsize = fontsize,
    fontcolor = fontcolor,
    # margin='0'
    )

    g.node('1', '', image='process_n_status.png',shape='none',
    fontsize = fontsize,
    fontcolor = fontcolor,
    # margin='-10'
    )
    g.node('2', '', image='attend_dot_chosen.png',shape='none',
    fontsize = fontsize,
    fontcolor = fontcolor
    )
    g.node('3', '', image='process_n_status_lp.png',shape='none',
    fontsize = fontsize,
    fontcolor = fontcolor
    )

    g.edge('0','1',penwidth = pw,label='π',fontsize=fontsize)
    g.edge('0','2',penwidth = pw,label='1-π',fontsize=fontsize)
    g.edge('2','3',penwidth = pw,label='',fontsize=fontsize)
    g.edge('3','0',penwidth = pw,label='Loop for\nthe next trial',fontsize=fontsize, headport='e',tailport = 'e')
    g.edge('1','0',penwidth = pw,label='Loop for\nthe next trial',fontsize=fontsize, headport='w',tailport = 'w')
    g.body.append('{rank=same; 1; 3;}')

    g.render('loop_process')
    print('done.')

def mk_local_process(mu):
    x = np.linspace(-500.0, 500.0, 200)
    y = np.linspace(-500.0, 500.0, 200)
    X, Y = np.meshgrid(x, y)

    f = lambda x, y: multivariate_normal(mu, [[25**2,0],[0,25**2]]).pdf([x, y])
    Z = np.vectorize(f)(X, Y)

    # heatmap
    plt.pcolor(X,Y,Z,cmap='Reds')

def generate_dot_by_LP(n_points,color,mu):
    # plot one dot generated from MN
    x_1,y_1 = np.random.multivariate_normal(mu, [[25**2,0],[0,25**2]],n_points).T
    plt.plot(x_1,y_1,marker = 'o',linestyle = '', markersize = 3, color=color)

    # # Label
    plt.xlabel('$x$', size=12)
    plt.ylabel('$y$', size=12)

def mk_global_process():
    x = np.linspace(-500.0, 500.0, 200)
    y = np.linspace(-500.0, 500.0, 200)
    X, Y = np.meshgrid(x, y)

    f = lambda x, y: multivariate_normal([0,0], [[250**2,0],[0,250**2]]).pdf([x, y])
    Z = np.vectorize(f)(X, Y)

    # heatmap
    plt.pcolor(X,Y,Z,cmap='Blues')

def generate_dot_by_GP(n_points,color):
    # plot one dot generated from MN
    x_1,y_1 = np.random.multivariate_normal([0,0], [[250**2,0],[0,250**2]],n_points).T
    plt.plot(x_1,y_1,marker = 'o',linestyle = '', markersize = 3,color=color)

    # plt.colorbar()

    # # Label
    plt.xlabel('$x$', size=12)
    plt.ylabel('$y$', size=12)

def mk_first_dot_generation():
    plt.clf()
    fig = plt.figure(figsize=(6,6))
    plt.xlim([-500,500])

    mk_global_process()
    np.random.seed(1000)
    generate_dot_by_GP(1,'yellow')

    # Title
    plt.title('First place generation')

    # Save
    plt.savefig('process_global_first_touch.png',dpi=300)

def mk_second_dot_generation():
    plt.clf()
    fig = plt.figure(figsize=(6,6))
    plt.xlim([-500,500])

    mk_global_process()
    np.random.seed(1000)
    generate_dot_by_GP(1,'black')
    np.random.seed(1001)
    generate_dot_by_GP(1,'yellow')

    # Title
    # plt.title('First place generation')
    plt.title('Second place generation')

    # Save
    plt.savefig('process_global_second_touch_both_global.png',dpi=300)

def mk_second_dot_generation_LP():
    plt.clf()
    fig = plt.figure(figsize=(6,6))
    plt.xlim([-500,500])

    mk_global_process()
    np.random.seed(1000)
    generate_dot_by_GP(1,'black')
    np.random.seed(1000)
    mk_local_process(
        mu = np.random.multivariate_normal([0,0], [[250**2,0],[0,250**2]],1).T
    )
    np.random.seed(1000)
    generate_dot_by_LP(
        1,
        'yellow',
        mu = np.random.multivariate_normal([0,0], [[250**2,0],[0,250**2]],1),
        )

    # Title
    # plt.title('First place generation')
    plt.title('Second place generation')

    # Save
    plt.savefig('process_global_second_touch_local.png',dpi=300)

def plot_scatter_GP():
    plt.clf()
    fig = plt.figure(figsize=(6,6))
    plt.xlim([-500,500])
    np.random.seed(1001)
    x_1,y_1 = np.random.multivariate_normal([0,0], [[250**2,0],[0,250**2]],10).T
    plt.plot(x_1,y_1,marker = 'o',linestyle = '', markersize = 3,color='black')

    # # Label
    plt.xlabel('$x$', size=12)
    plt.ylabel('$y$', size=12)
    plt.title('$n-1$-th status of dots in the screen')

    # Save
    plt.savefig('process_n_1_status.png',dpi=300)

    plt.clf()
    fig = plt.figure(figsize=(6,6))
    plt.xlim([-500,500])

    np.random.seed(1001)
    mk_global_process()
    x_1,y_1 = np.random.multivariate_normal([0,0], [[250**2,0],[0,250**2]],10).T
    plt.plot(x_1[1:],y_1[1:],marker = 'o',linestyle = '', markersize = 3,color='black')
    x_1,y_1 = np.random.multivariate_normal([0,0], [[250**2,0],[0,250**2]],1).T
    plt.plot(x_1,y_1,marker = 'o',linestyle = '', markersize = 5,color='yellow')

    # # Label
    plt.xlabel('$x$', size=12)
    plt.ylabel('$y$', size=12)
    # Title
    # plt.title('First place generation')
    plt.title('$n$-th status of dots in the screen')

    # Save
    plt.savefig('process_n_status.png',dpi=300)

def plot_scatter_LP():
    plt.clf()
    fig = plt.figure(figsize=(6,6))
    plt.xlim([-500,500])
    np.random.seed(1001)
    x_1,y_1 = np.random.multivariate_normal([0,0], [[250**2,0],[0,250**2]],10).T
    plt.plot(x_1,y_1,marker = 'o',linestyle = '', markersize = 3,color='black')
    plt.plot(x_1[2],y_1[2],marker = 'o',linestyle = '', markersize = 8,color='green')
    # # Label
    plt.xlabel('$x$', size=12)
    plt.ylabel('$y$', size=12)
    plt.title('Attend dot Randomly chosen from $10$ dots in the screen')

    # Save
    plt.savefig('attend_dot_chosen.png',dpi=300)

    plt.clf()
    fig = plt.figure(figsize=(6,6))
    plt.xlim([-500,500])

    np.random.seed(1001)
    print(x_1[2],y_1[2])
    mk_local_process([x_1[2],y_1[2]])
    x_1,y_1 = np.random.multivariate_normal([0,0], [[250**2,0],[0,250**2]],10).T
    plt.plot(x_1[1:],y_1[1:],marker = 'o',linestyle = '', markersize = 3,color='black')
    generate_dot_by_LP(
        1,
        'yellow',
        mu = [x_1[2],y_1[2]],
        )    
    # plt.plot(x_1,y_1,marker = 'o',linestyle = '', markersize = 5,color='yellow')

    # # Label
    plt.xlabel('$x$', size=12)
    plt.ylabel('$y$', size=12)
    # Title
    # plt.title('First place generation')
    plt.title('$n$-th status of dots in the screen')

    # Save
    plt.savefig('process_n_status_lp.png',dpi=300)

def main():    
    # mk_first_dot_generation()
    # mk_second_dot_generation()
    # mk_second_dot_generation_LP()
    # plot_scatter_GP()
    # plot_scatter_LP()
    mk_graph()
    mk_graph_loop()

if __name__ == "__main__":
    main()