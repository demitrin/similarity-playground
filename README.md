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
Use the script `calc_and_store_exact_similarites.py` to ge the exact similarities for the dataset.
To run the script, use
```
python calc_and_store_exact_similarites.py <data_directory> <storage_directory>
```
You will see the data stored in `exact_mitdwh_similarities.json`.

### Generate Exact Similar Sets with Thresholds
To generate the exact similarity thresholds, we will use `calc_and_store_exact_thresholds.py`. 
Simply check that the script has the correct exact similarity json filename in the `__main__` part of the script.
In this case, it should be `'exact_mitdwh_similarities.json'`.

```
python calc_and_store_exact_thresholds.py
```

You will see data stored in `similar_sets-<threshold>.json`.

### Generate Approximate Similar Sets for Minhash
The following scripts are for minhash approximate similarity generation:

1. `reg_mitdwh.py <mitdwh_path>`
2. `ophr_mitdwh.py <mitdwh_path>`
3. `partition_mitdwh.py <mitdwh_path>`
4. `minheap_mitdwh.py <mitdwh_path>`

The outputs from the minhash approximate similarity scripts will be jaccard similarities.
We need to generate similar sets from these similarities. 
To do this, we will use the same script used for the exact similarities.
Modify the glob in `__main__` of `calc_and_store_exact_thresholds.py` to be 

```
*/*/*data.json
```
Then run 
```
python calc_and_store_exact_thresholds.py
```

And the similar sets will be computed and stored in the directories the similarities originated from.


### Generate Approximate Similar Sets for LSH

The following scripts are for lsh approximate similarity generation:


1. `reg_lsh_mitdwh.py <mitdwh_path>`
2. `ophr_lsh_mitdwh.py <mitdwh_path>`
3. `minheap_lsh_mitdwh.py <mitdwh_path>`

These generate similar sets directly.

### Calculate Precision/Recall
We use the script `calc_better_precision_recall.py` to calculate and output precision/recall for each test.
To do this, simply run the script.

```
python calc_better_precision_recall.py
```
This will output the precision/recall into a file `precision_recall.txt`.

