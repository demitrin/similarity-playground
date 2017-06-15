# Jaccard Similarity Data Simulations

## Installation

For this project, we use pip to install all of the required libraries.
Install the libraries in the requirements.

```
pip install requirements.txt -r
```

Next, we need to install datasketch from the fork located [here](https://github.com/demitrin/datasketch-fork).
Start by cloning the repository into this project. Then run
```
cd datasketch-fork
python setup.py install
```

Now, you should have all of the required libraries for the project.

## How to run simulations
The following steps are required to run the simulations:

1. Generate exact similarity measurements from original data
2. Generate exact similar sets from the exact similarity measurements for desired thresholds
3. Generate approximate similar sets from either minhash or lsh methods
4. Compare similar sets, calculating precision/recall

Next, I will outline how to do each of the steps above.

### Generate Exact Similarity
