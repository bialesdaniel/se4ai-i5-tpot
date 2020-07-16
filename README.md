# se4ai-i5-tpot
This repo shows how to use TPOT to train an optimal pipeline to predict how users would rate movies in a movie streaming service. For more information please read the whole [article](https://medium.com/@daniel.biales/automl-taking-tpot-to-the-movies-cf7e6f67f876?source=friends_link&sk=6737cdd9d4cf2ff3c7322ee25f80fe70).


## Installation
To install use whichever python virtual envirnoment you prefer
```bash
virtualenv env
source bin/env/activate
pip install -r requirements.txt
```

## How to use this repo
I created several different ways to explore the code so please choose whichever one works for you.
1. `optimize-pipeline.py` - This is a code implementation of TPOT pipeline optimization. It uses modularized code and is most similar to how you may actually implement TPOT.
2. `notebooks/TPOT_Movies_Explained.ipynb` - I created a python notebook that walks you through the whole process. This includes a lot of description which should help if you didn't understand the code at first look. Run `cd notebooks && jupyter lab TPOT_Movies_Explained.ipynb` to open the notebook.
3. [Google Colab](https://colab.research.google.com/drive/1nsFIhZ13uOkHjBzv_26IqAHXcfBeB9rV?usp=sharing) - If you prefer to work in notebooks and do not care about the code you might want to copy this Google Colab notebook into your drive and play around.


## Running the code
**Warning**: TPOT takes can take a long time to run depending on the number of generations, population size, and dataset size. I mean a really long time! If you run it with 100 generations and 100 population size on the full dataset then it will take somewhere around 200-400 hours. Running with 100 generations, 100 popuation size and a dataset of 10,000 it should finish within 6 hours.

### Locally
After installation just run
```bash
python optimize-pipeline.py
```
If you want to change any of the default options checkout `config/config.py to see what environment variables you need to set.

### Docker
The instructions below allow you to run the code in a docker container locally. You could also publish the docker container and run it elsewhere.
```
docker build -t se4ai/tpot .
docker run --name=tpot --mount type=bind,source="$(pwd)"/tpot-output,target=/app/tpot-output se4ai/tpot
```
**Note**: This process can take up a lot of resources so if your docker container dies try increasing the memory.

### Environment Variables
Many of these environment variables are based on the TPOT tool. For information on their configuration variables read their [documentation](https://epistasislab.github.io/tpot/api/#regression).

`GENERATIONS` - The number of generations TPOT should run. default = 100

`POPULATION_SIZE` = The population size for initializing and generating offspring. default = 100

`TARGET_CACHE_SIZE` = TPOT caches some data to help it run more quickly. This is the number of GB that the cache should be trimmed down to when the cache is cleared. Be warned the cache can grow significantly larger than this number. If you want to prevent the cache from growing too large then lower the `CACHE_CLEAR_FREQUENCY`. default = 1 GB

`CACHE_CLEAR_FREQUENCY` = The frequency with which the cache is cleared in minutes. default = 30 min

`N_JOBS` = Number of CPUs for evaluating pipelines in parallel during the TPOT optimization process. Assigning this to -1 will use as many cores as available on the computer. default = 1

`OUTPUT_DIRECTORY` = The directory to which TPOT will write the cache data, the optimal pipeline code, the joblib files for the cleaning pipeline and prediction pipeline. default = CWD/tpot-output

`DATASET_SIZE` = The amount of data you want to use. This amount will be split into training and test. Assigning this to -1 will use the full dataset. default = -1

`VERBOSITY` = This will control the amount of logging that is output. 0 = none, 1 = minimal, 2 = moderate debug, 3 = everything. default = 0

## Other files
The `download-data.py` script will download the data from a RDS database on AWS. You likely do not have the credentials to download from my database, but if you want to setup your own database you can use this code to pull down data and write them to the CSV files.