# Diversity Scoring on MovieLens

## Overview

In this repository we implement Spotify's [Generalist-Specialist score](https://dl.acm.org/doi/abs/10.1145/3366423.3380281) 
on the [MovieLens dataset](https://grouplens.org/datasets/movielens/).

The code here accompanies the Medium article "Different Strokes for Different Folks at Spotify".


## Installation

We recommend using Anaconda to create a virtual environment. Install the requirements via
```
conda install --yes --file requirements.txt 
```
or if using `pip`, run
```
pip install -r requirements.txt
```

## Running the Notebook

To run the notebook, simply start a Jupyter notebook session via `jupyter notebook`.
Training of the model and scoring the generalist-specialist scores of all users 
on the MovieLens dataset can be time consuming.
