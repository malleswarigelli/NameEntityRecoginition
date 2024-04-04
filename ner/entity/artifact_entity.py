

from dataclasses import dataclass
import os
from ner.constants import *

# Data Ingestion Artifacts
@dataclass
class DataIngestionArtifact:
    zip_data_file_path:str
    csv_data_file_path:str
    
# Data Transformation Artifacts
@dataclass
class DataTransformationArtifact:
    labels_to_ids_path:str
    ids_to_labels_path:str
    df_train_path:str
    df_val_path:str
    df_test_path:str
    unique_labels_path:str