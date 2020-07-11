import numpy as np
import pandas as pd
from sklearn.cluster import FeatureAgglomeration
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=None)

# Average CV score on the training set was: -1.1171558107196211
exported_pipeline = make_pipeline(
    VarianceThreshold(threshold=0.1),
    FeatureAgglomeration(affinity="l2", linkage="complete"),
    GradientBoostingRegressor(alpha=0.8, learning_rate=0.001, loss="ls", max_depth=7, max_features=0.9500000000000001, min_samples_leaf=17, min_samples_split=8, n_estimators=100, subsample=0.6000000000000001)
)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
