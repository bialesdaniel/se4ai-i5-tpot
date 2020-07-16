from sklearn.pipeline import Pipeline 
from transformers.MultiLabelStringToArray import MultiLabelStringToArray
from transformers.MultiLabelBinarizerTransformer import MultiLabelBinarizerTransformer

def create_mlb_pipeline(verbose=False):
    return Pipeline([
        ('multilabel_str_to_array',MultiLabelStringToArray()),
        ('binarizer', MultiLabelBinarizerTransformer()),
    ],verbose=verbose)
