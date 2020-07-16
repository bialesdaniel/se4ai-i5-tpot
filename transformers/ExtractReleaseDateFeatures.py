from sklearn.base import BaseEstimator, TransformerMixin

class ExtractReleaseDateFeatures(BaseEstimator, TransformerMixin):
    """
    This transformer takes a column with a date string formatted as 
    'YYYY-mm-dd', extracts the year and month, and returns a DataFrame with
    those columns.
    """
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        """
        Returns a dataframe with the year and month as integer fields. When 
        applied in a ColumnTransformer this will effectively remove the
        original column and replace it with the new columns.
        """
        df = X.copy()

        # fill nulls values that wont show up in valid data
        df = df.fillna('0000-00-00') 

        df['year'] = df.iloc[:,0].apply(lambda x: str(x)[:4])
        df['month'] = df.iloc[:,0].apply(lambda x: str(x)[5:7])
        df = df.astype({'year':'int64', 'month':'int64'})

        return df.loc[:,['year','month']]