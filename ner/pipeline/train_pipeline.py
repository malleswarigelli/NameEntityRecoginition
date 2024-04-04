import sys
from ner.configuration.gcloud import GCloud
from ner.constants import *
from ner.entity.config_entity import DataIngestionConfig
from ner.entity.artifact_entity import DataIngestionArtifact
from ner.logger import logging
from ner.exception import NerException
from ner.components.data_ingestion import DataIngestion


class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.gcloud= GCloud()
        
    def start_data_ingestion(self)->DataIngestionArtifact:
        """
        This method of TrainPipeline class is responsible for starting data ingestion component
        returns DataIngestionArtifact
        """
        logging.info("Entered the start_data_ingestion method of TrainPipeline class")
        try:
            logging.info("Getting the data from Google cloud")
            # creates data_ingestion object
            data_ingestion= DataIngestion(data_ingestion_config=self.data_ingestion_config,
                                      gcloud=self.gcloud)
            # creates data_ingestion output
            data_ingestion_artifact= data_ingestion.initiate_data_ingestion()
            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )
            return data_ingestion_artifact
        except Exception as e:
            raise NerException(e, sys) from e
        
        
        
        
    def run_pipeline(self, ) -> None:
        """
        This method of TrainPipeline class is responsible for running complete pipeline
        """
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            
        except Exception as e:
            raise NerException(e, sys) from e
        