from sklearn.compose import ColumnTransformer

from pipelines.multilabel_binarizer import create_mlb_pipeline
from transformers.ExtractReleaseDateFeatures import ExtractReleaseDateFeatures
from pipelines.constants import MULTILABEL_BINARIZER_COLUMNS, RELEASE_DATE_COLUMNS, PASSTHROUGH_COLUMNS
from config.config import get_verbosity

def create_data_clean_pipeline():
    verbosity = get_verbosity('pipeline')
    return ColumnTransformer([
        ('multilabel_binarizer', create_mlb_pipeline(verbose=verbosity), MULTILABEL_BINARIZER_COLUMNS),
        ('release_date', ExtractReleaseDateFeatures(), RELEASE_DATE_COLUMNS),
        ('passthrough_columns','passthrough', PASSTHROUGH_COLUMNS)
    ],remainder='drop',verbose=verbosity)