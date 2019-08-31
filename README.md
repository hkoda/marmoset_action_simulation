# marmoset_action_simulation


(NOT YET COMPLETED OF DESCRIPTIONS)
This repo is the code of the manuscripts, Hiroki Koda *et al* (Title or DOI will appear immediately after the journal acceptance), simulating the touch place of the marmoset action experiments.

## Requirements
- Python 3.6.7
- numpy 1.16.4
- Tested on Mac OS 10.14.6 or Ubuntu 14.01 (not tested on Windows)

## Usage
- Make directory named as `results` at the same level of the python script `mixture_gausian_abm.py`, before running the code.
- Run the following code in your terminal.

```python mixture_gausian_abm.py```

## Directories
- `mixture_gausin_abm.py`
    Main script of the simulation
- `README.md`
    readme files
- `GP_cov.png`
    PNG file used in README.md
- `LP_cov.png`
    PNG image file used in README.md
- `figures_for_readme`
    Directory including PNG image files and python script generating image files, used in README.md

## Overviews of our model
In this model, the dots (marmoset touch location) were generated from the several rules:
- Rule 1. The first dot (touch location) is generated around the screen center with the **large** standard deviation. In other words, this process is the [bivariate Gaussian distributions](https://en.wikipedia.org/wiki/Multivariate_normal_distribution) with the screen center set as *mean* and large SD. This aims to simulate the marmoset behaviors to touch the screen widely, **independent** of the previous touching behaviors.
- Rule 2. After the second dots (touch locations), the dot is generated from each of the two processes;
    - Sub-rule 2-1. The same process of the first dot generation, of the [bivariate Gaussian distributions](https://en.wikipedia.org/wiki/Multivariate_normal_distribution). The dot is generated **independent** of any previous touching behaviors.  
    - Sub-rule 2-2. The different process consisted of the two steps. First, one of the visible dots (which were the locations the marmoset touched previously) is selected randomly. Then, the next dot is generated around the selected dot with the **small** standard deviations. In other words, this process is the [bivariate Gaussian distributions](https://en.wikipedia.org/wiki/Multivariate_normal_distribution) with the selected dot set as *mean* and large SD. This aims to simulate the marmoset behaviors to touch the location near around one of the visible dots screen, **dependent** on the previous touching behaviors.
- Rule 3. The maximum number of visible dots is 10
    - Sub-rule 3-1. From *1-st* dot until the *10-th* dot, the number of visible dots increases up to 10.
    - Sub-rule 3-2. After the *11-th* dots, the *(i-10)-th* dot is replaced with the *i-th* dot. E.g. When the *11-th* dot is generated, *1-st* dot is simultaneously disappeared from the screen.

## Graphical descriptions of the model
Here I illustrate the example of the dot generation for quick understanding of our model.
- 1. the example of the *first* dot generation (Rule 1)
- 2. the example of the *second* dot generation (Simplest example of Rule 2 and Rule 3(Subrule 3-1.))
- 3. the example of the *n-th* dot generation (Generalized example of Rule 2 and Rule 3(Sub-rule 3-2))
### 1. The example of the first dot generations
The first dot is generated from the [bivariate Gaussian distributions](https://en.wikipedia.org/wiki/Multivariate_normal_distribution) with (0,0) as a mean parameter (&mu;<sub>g</sub>) and <img src="GP_cov.png" height="40" align="middle"> as a covariance matrix (&Sigma;<sub>g</sub>). This Gaussian distribution with large standard deviations(SD) is called as "**Global Process (GP)**", hereafter.

<img src="figures_for_readme/process_global_first_touch.png" width="500">

The heatmap of probability density of GP. The dot (yellow) is generated from the GP.
<!-- ![](figures_for_readme/process_global_first_touch.png) -->

### 2. The example of the second dot generation
The next (second) dot is generated from each of GP **OR** the other bivariate Gaussian distribution of the mean parameter (&mu;<sub>l</sub>) set as the previous dot (grey dot in the next fig) and the covariance matrix (&Sigma;<sub>l</sub>) set as <img src="LP_cov.png" height="40" align="middle">. The latter process aims to simulate the marmoset actions of touching the visible dot nearby. This Gaussian distribution with smaller SD is called as "**Local Process (LP)**", hereafter.

<img src="figures_for_readme/process_global_second_touch_both_global.png" width="500">

The second dot (yellow) is generated from the GP as well as the first dot (black), with the heatmap of the probability density of GP.


<img src="figures_for_readme/process_global_second_touch_local.png" width="500">

The second dot (yellow) is generated from the LP, determined by the first dot (black), with the heatmap of the probability density (red colorations) of LP.


### 3. The example of the n-th dot generations
Similar to the second dot generation, the n-th dot is generated from each of GP **OR** the LP. In the case of LP, the attend dot is chosen from the previous 10 dots (between n-1 th and n-10 th dots), and is set to the mean parameter of LP (&mu;<sub>l</sub>).

<img src="figures_for_readme/process_n_1_status.png" width="500">

The sample figure of the n-1 th status of the screen. The 10 dots are shown.

<img src="figures_for_readme/process_n_status.png" width="500">

The case of GP. The next (n-th) dot (yellow) is generated from the GP, with heatmap of the probability density of GP. 

<img src="figures_for_readme/process_n_status_lp.png" width="500">

The case of LP. The next (n-th) dot (yellow) is generated from the LP. The attend dot is the black dot, the center of the red area. Red area represent the probability density of the LP. 

## Flowchart of simulations

- From the *1-st* dot to the *2-nd* dot. &pi; is the probability to choose the GP process.
<img src="figures_for_readme/first_process.png">

- From the *(n-1)-th* dot to the *n-th* dot. In the case of the LP proceess, there are two steps, i.e., the attend dot selection and the LP process based on the attend dot .
<img src="figures_for_readme/loop_process.png">


## Summary of parameters used in our simulations
- Global Process
    - &mu;<sub>g</sub> = (0,0)
    - &Sigma;<sub>g</sub> = <img src="GP_cov.png" height="40" align="middle">
- Local process
    - &mu;<sub>l</sub> = (x<sub>j</sub>,y<sub>j</sub>)
    - &Sigma;<sub>l</sub> = <img src="LP_cov.png" height="40" align="middle">
    (x<sub>j</sub>,y<sub>j</sub>) means the coordinates of the dot selected among the visible dots
- General settings
    - n<sub>iteration</sub> = 10000
