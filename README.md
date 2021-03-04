# Flashgg Prototype

Toy package to try out features for the new Flashgg framework.

## Installation

First, clone the repo and access it:
```
git clone git@github.com:maxgalli/flashgg-prototype.git
cd flashgg-prototype
```
If you have Conda, an environment (containing more way more packages than the ones actually needed at the time of writing) can be created running:
```
conda env create -f flashgg_env.yml
```
To install the prototype, two main ways are suggested:

- **users**: ```python setup.py install```
- **developer**: ```pip install -e .``` (automatically detects the changes with no need to install again)

## Run simple test

To try out the basic features:
```
cd examples
python process_sample1.root
```
