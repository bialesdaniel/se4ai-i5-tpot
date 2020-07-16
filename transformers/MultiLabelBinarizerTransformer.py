import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MultiLabelBinarizer

class MultiLabelBinarizerTransformer(BaseEstimator, TransformerMixin):
    """
    This tranformer creates a MultiLabelBinarizer for every column passed in.
    """
    def __init__(self):
        self.mlbs = {}
    def fit(self, X, y=None):
        """Fit the MultiLabelBinarizer to the data passed in"""
        df = X.copy()
        for column_name in df.columns:
            mlb = MultiLabelBinarizer()
            mlb.fit(df[column_name])
            # Uncomment the following line if you want to print out the values
            # that the MultiLabelbinarizer discovered.
            #print('Column: {NAME} Values: {VALUES}'.format(NAME=column_name, VALUES=mlb.classes_))
            self.mlbs[column_name] = mlb
        return self
    def transform(self, X, y=None):
        """
        Returns a dataframe with the binarized columns. When applied in a
        ColumnTransformer this will effectively remove the original column and 
        replace it with the binary columns
        """
        df = X.copy()
        binarized_cols = pd.DataFrame()
        for column_name in df.columns:
            mlb = self.mlbs.get(column_name)
            new_cols = pd.DataFrame(mlb.transform(df[column_name]),columns=mlb.classes_)
            binarized_cols = pd.concat([binarized_cols, new_cols], axis=1)
        return binarized_cols