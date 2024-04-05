
from dataclasses import dataclass
import os
from ner.constants import *


@dataclass
class DataIngestionConfig:
    def __init__(self):
        self.data_ingestion_dir:str= os.path.join(ARTIFACTS_DIR, DATA_INGESTION_ARTIFACTS_DIR)
        self.gcp_data_file_path:str= os.path.join(self.data_ingestion_dir, GCP_DATA_FILE_NAME)
        self.output_data_file_path:str= self.data_ingestion_dir
        self.csv_data_file_path:str= os.path.join(self.data_ingestion_dir, CSV_DATA_FILE_NAME)
        
@dataclass
class DataTransformationConfig:
    def __init__(self):
        self.data_transformation_dir:str= os.path.join(ARTIFACTS_DIR, DATA_TRANSFORMATION_ARTIFACTS_DIR)
        self.labels_to_ids_path:str= os.path.join(self.data_transformation_dir,LABELS_TO_IDS_FILE_NAME) #labels_to_ids.pkl
        self.ids_to_labels_path:str= os.path.join(self.data_transformation_dir,IDS_TO_LABELS_FILE_NAME) # ids_to_labels.pkl
        self.ids_to_labels_gcp_path:str= os.path.join(self.data_transformation_dir)
        self.df_train_path:str= os.path.join(self.data_transformation_dir,DF_TRAIN_FILE_NAME) # "df_train.pkl"
        self.df_val_path:str= os.path.join(self.data_transformation_dir,DF_VAL_FILE_NAME) # "df_val.pkl"
        self.df_test_path:str= os.path.join(self.data_transformation_dir, DF_TEST_FILE_NAME) # "df_test.pkl"
        self.unique_labels_path:str= os.path.join(self.data_transformation_dir, UNIQUE_LABELS_FILE_NAME) # "unique_labels.pkl"
        
        