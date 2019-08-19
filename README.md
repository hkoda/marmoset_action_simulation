# marmoset_action_simulation

(NOT YET COMPLETED OF DESCRIPTIONS)
This repo is the code of the manuscripts, Hiroki Koda *et al* (Title or DOI will appear immediately after the journal acceptance), simulating the touch place of the marmoset action experiments.

## Requirements
- Python 3.6.7
- numpy 1.16.4

## Graphical descriptions of the model
In this model, the dots (marmoset touch location) were generated from several rules:

---

- 1. The first dot is generated from the [bivariate Gaussian distributions](https://en.wikipedia.org/wiki/Multivariate_normal_distribution) with (0,0) mean parameter ($\mu_{g}$) and $
\begin{pmatrix}
250^{2} & 0 \\
0 & 250^{2} \\
\end{pmatrix}
$covariance matrix ($\Sigma_{g}$). This Gaussian distribution with large SD is called as "**Global Process (GP)**", hereafter.
<img src="figures_for_readme/process_global_first_touch.png" width="500">
The heatmap of probability density of GP. The dot (yellow) is generated from the GP.
<!-- ![](figures_for_readme/process_global_first_touch.png) -->

---

- 2. Next (second) dot is generated from each of GP **OR** the other bivariate Gaussian distribution of the mean parameter ($\mu_{l}$) set as the previous dot (grey dot in the next fig) and the covariance matrix ($\Sigma_{l}$) set as $\begin{pmatrix}
25^{2} & 0 \\
0 & 25^{2} \\
\end{pmatrix}
$. The latter process aims to simulate the marmoset actions of touching the visible dot. This Gaussian distribution with large SD is called as "**Local Process (LP)**", hereafter.

<img src="figures_for_readme/process_global_second_touch_both_global.png" width="500">

The second dot (yellow) is generated from the GP as well as the first dot (black), with the heatmap of the probability density of GP.


<img src="figures_for_readme/process_global_second_touch_local.png" width="500">

The second dot (yellow) is generated from the LP, determined by the first dot (black), with the heatmap of the probability density (red colorations) of LP.

## Flowchart of simulations

<img src="figures_for_readme/first_process.png">


<img src="figures_for_readme/loop_process.png">


## Summary of parameters used in our simulations
- $\mu_{g} = (0,0)$
- $\Sigma_{g} = 
\begin{pmatrix}
250^{2} & 0 \\
0 & 250^{2} \\
\end{pmatrix}
$
- $n_{iteration} = 10000$