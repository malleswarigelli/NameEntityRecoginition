import os
import sys
from zipfile import Path
import time
from ner.logger import logging
from ner.exception import NerException


class GCloud:
    '''Load and Access data from google cloud'''
    def sync_folder_to_gcloud(self, gcp_bucket_url:str, filepath:Path, filename:str):
        """
        Method: sync_folder_to_gcloud
        Purpose: load data into gcloud
        Args:
            gcp_bucket_url (_type_): str
            filepath (_type_): Path
            filename (_type_): str
        Output: None
        Exception: Raises error
        """
        try:
            command= f"gsutil cp {filepath}/{filename} gs://{gcp_bucket_url}"
            os.system(command)
            logging.info("data loaded into gcloud successfully!")
        except Exception as e:
            raise NerException(e, sys) from e
        
    def sync_folder_from_gcloud(self, gcp_bucket_url:str, filename:str, destination:Path):
        """
        Method: sync_folder_from_gcloud
        Purpose: access data from gcloud
        Args:
            gcp_bucket_url (str): str
            filename (str): str
            destination (Path): Path
        Output: None
        Exception: Raises error
        """
        try:
            command= f"gsutil cp gs://{gcp_bucket_url}/{filename} {destination}"
            os.system(command)
            logging.info(f"data accessed from gcloud into: {destination}")
        except Exception as e:
            raise NerException(e, sys) from e    
        
        
            