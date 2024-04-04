import os
import sys
from zipfile import ZipFile


from ner.configuration.gcloud import GCloud
from ner.constants import *
from ner.entity.config_entity import DataIngestionConfig
from ner.entity.artifact_entity import DataIngestionArtifact
from ner.logger import logging
from ner.exception import NerException




class DataIngestion:    
    def __init__(self, data_ingestion_config:DataIngestionConfig, gcloud: GCloud) -> None:
        """
        :param data_ingestion_config: configuration for data ingestion (obj of DataIngestionConfig class)
        :param gcloud: get data from to gcloud
        """
        try:
            self.data_ingestion_config= data_ingestion_config
            self.gcloud= gcloud
        except Exception as e:
            raise NerException(e,sys)
        
    def get_data_from_gcp(self, bucket_name:str, file_name:str, path:str)-> ZipFile:
        """
        Method Name :   get_data_from_gcp
        Description :   This method extracts data from gcloud bucket to zip file
        
        Output      :   data is returned as artifact of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered get_data_from_gcp method of DataIngestion class")
        try:
            self.gcloud.sync_folder_from_gcloud(gcp_bucket_url=bucket_name,
                                                    filename=file_name,
                                                    destination=path)
            logging.info("Exited get_data_from_gcp method of DataIngestion class")
        except Exception as e:
            raise NerException(e,sys)
    
    def unzip_data(self, input_file_path:str, output_file_path:str)-> None:
        """
        Method Name :   unzip_data
        Description :   This method unzips data to csv file
        
        Output      :   csv data is returned as artifact of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered get_data_from_gcp method of DataIngestion class")
        try:
            #loading .zip file and extract all content
            with ZipFile(input_file_path, "r") as zipobj:
                zipobj.extractall(path=output_file_path)
            logging.info("Exited unzip_data method of DataIngestion class")
            
        except Exception as e:
            raise NerException(e,sys)
    
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Method Name :   initiate_data_ingestion
        Description :   This method initiates the data ingestion components of training pipeline 
        
        Output      :   DataIngestionArtifact
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered initiate_data_ingestion method of DataIngestion class")        
        try:
            # create data_ingestion dir inside artifacts dir
            os.makedirs(self.data_ingestion_config.data_ingestion_dir, exist_ok=True)
            logging.info(f"Created {os.path.basename(self.data_ingestion_config.data_ingestion_dir)} directory.")
            
            # Getting data from GCP
            self.get_data_from_gcp(bucket_name=BUCKET_NAME,
                                   file_name=GCP_DATA_FILE_NAME, 
                                   path=self.data_ingestion_config.gcp_data_file_path)
            logging.info(f"Got the file from Google cloud storage. Filename {os.path.basename(self.data_ingestion_config.gcp_data_file_path)}")
            
            # unzip data
            self.unzip_data(
                            input_file_path=self.data_ingestion_config.gcp_data_file_path, 
                            output_file_path=self.data_ingestion_config.output_data_file_path)
            logging.info(f"Extracted data from {os.path.basename(self.data_ingestion_config.gcp_data_file_path)} into {os.path.basename(self.data_ingestion_config.csv_data_file_path)}")
            
        
            data_ingestion_artifact= DataIngestionArtifact(
                                        zip_data_file_path=self.data_ingestion_config.gcp_data_file_path,
                                        csv_data_file_path= self.data_ingestion_config.csv_data_file_path)
            
            logging.info("Exited initiate_data_ingestion method of DataIngestion class")
            
            return data_ingestion_artifact
        except Exception as e:
            raise NerException(e,sys)
    