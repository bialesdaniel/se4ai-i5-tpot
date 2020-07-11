import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.kernel_approximation import Nystroem, RBFSampler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=None)

# Average CV score on the training set was: -1.1167856167286092
exported_pipeline = make_pipeline(
    Nystroem(gamma=0.30000000000000004, kernel="laplacian", n_components=6),
    RBFSampler(gamma=0.55),
    ExtraTreesRegressor(bootstrap=True, max_features=0.9000000000000001, min_samples_leaf=13, min_samples_split=20, n_estimators=100)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
