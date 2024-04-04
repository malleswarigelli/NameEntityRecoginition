
from dataclasses import dataclass
import os
from ner.constants import *


@dataclass
class DataIngestionConfig:
    def __init__(self):
        self.data_ingestion_dir:str= os.path.join(ARTIFACTS_DIR, DATA_INGESTION_DIR_NAME)
        self.gcp_data_file_path:str= os.path.join(self.data_ingestion_dir, GCP_DATA_FILE_NAME)
        self.output_data_file_path:str= self.data_ingestion_dir
        self.csv_data_file_path:str= os.path.join(self.data_ingestion_dir, CSV_DATA_FILE_NAME)
        
        