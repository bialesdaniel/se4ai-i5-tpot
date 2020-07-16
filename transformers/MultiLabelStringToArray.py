import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class MultiLabelStringToArray(BaseEstimator, TransformerMixin):
    """
    This shapes the data to be passed into the MultiLabelBinarizer. It takes
    columns that are array-like strings and turns them into arrays.
    """
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        df = X.copy()
        for column_name in df.columns:
            df[column_name] = self._transform_column_to_array(df[column_name])
        return df

    def _transform_column_to_array(self, pd_column):
        transformed_column = pd_column.copy()
        
        # replace null cells with empty array
        transformed_column.loc[transformed_column.isnull()] = transformed_column.loc[
            transformed_column.isnull()
        ].apply(lambda x: '[]')

        # parse string into array
        transformed_column = transformed_column.apply(self._parse_arraystr)
        return transformed_column

    def _parse_arraystr(self, str):
        """
        Applies a number of rules to turn an array looking string into an array
          - remove brackets
          - remove quotes
          - remove extra spaces
          - deliminate by comma
          - remove empty string entries in the array
        """
        str_without_brackets = str.replace("[","").replace("]","")
        str_without_quotes = str_without_brackets.replace("'","")
        str_without_spaces = str_without_quotes.replace(" ","")
        list_with_empties = str_without_spaces.split(',')
        if '' in list_with_empties:
            while("" in list_with_empties) : 
                list_with_empties.remove("") 
        return np.array(list_with_empties)
 