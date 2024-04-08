
import sys
from ner.configuration.gcloud import GCloud
from ner.constants import *
from ner.entity.config_entity import DataIngestionConfig, DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig
from ner.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifacts, ModelPusherArtifacts
from ner.logger import logging
from ner.exception import NerException
from ner.components.data_ingestion import DataIngestion
from ner.components.data_transformation import DataTransformation
from ner.components.model_trainer import ModelTrainer
from ner.components.model_evaluation import ModelEvaluation
from ner.components.model_pusher import ModelPusher


class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.gcloud= GCloud()
        self.data_transformation_config= DataTransformationConfig()
        self.model_trainer_config= ModelTrainerConfig()
        self.model_evaluation_config= ModelEvaluationConfig()
        self.model_pusher_config= ModelPusherConfig()
        
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
        
    def start_data_transformation(self, data_ingestion_artifact:DataIngestionArtifact)->DataTransformationArtifact:
        """
        This method of TrainPipeline class is responsible for starting data transformation component
        returns DataTransformationArtifact
        """
        logging.info("Entered the start_data_transformation method of TrainPipeline class")
        try:
            data_transformation= DataTransformation(data_transformation_config= self.data_transformation_config,
                                                    data_ingestion_artifact= data_ingestion_artifact)
            data_transformation_artifact= data_transformation.initiate_data_transformation()
            
            logging.info(
                "Exited the start_data_transformation method of TrainPipeline class"
            )
            return data_transformation_artifact
        except Exception as e:
            raise NerException(e, sys) from e  
        
    def start_model_trainer(self, data_transformation_artifacts:DataTransformationArtifact)-> ModelTrainerArtifact:
        """
        This method of TrainPipeline class is responsible for starting model trainer component
        returns ModelTrainerArtifact
        """
        logging.info("Entered the start_model_trainer method of TrainPipeline class")
        try:
            model_trainer_config= ModelTrainer(data_transformation_artifacts= data_transformation_artifacts,
                                               model_trainer_config= self.model_trainer_config)
            model_trainer_artifact= model_trainer_config.initiate_model_trainer()
            logging.info("Exited the start_model_trainer method of TrainPipeline class")
            
            return model_trainer_artifact
        
        except Exception as e:
            raise NerException(e, sys) from e 
        
    def start_model_evaluation(self, data_transformation_artifacts:DataTransformationArtifact,
                               model_trainer_artifact:ModelTrainerArtifact)-> ModelEvaluationArtifacts:
        """
        This method of TrainPipeline class is responsible for starting model evaluation component
        returns ModelEvaluationArtifacts
        """
        logging.info("Entered the start_model_evaluation method of TrainPipeline class")
        try:
            model_evaluation_config= ModelEvaluation(data_transformation_artifact= data_transformation_artifacts,
                                                     model_trainer_artifact= model_trainer_artifact,
                                                     model_evaluation_config= self.model_evaluation_config)
            model_evaluation_artifact= model_evaluation_config.initiate_model_evaluation()
            logging.info("Exited the start_model_evaluation method of TrainPipeline class") 
             
            return model_evaluation_artifact
        
        except Exception as e:
            raise NerException(e, sys) from e 
        
    def start_model_pusher(self, model_evaluation_artifact: ModelEvaluationArtifacts)-> ModelPusherArtifacts:
        """
        This method of TrainPipeline class is responsible for starting model pusher component
        returns ModelPusherArtifacts
        """
        logging.info("Entered the start_model_pusher method of TrainPipeline class")
        try:
            model_pusher_config= ModelPusher(model_evaluation_artifact= model_evaluation_artifact,
                                                     model_pusher_config= self.model_pusher_config)
            model_pusher_artifact= model_pusher_config.initiate_model_pusher()
            logging.info("Exited the start_model_pusher method of TrainPipeline class") 
             
            return model_pusher_artifact
        
        except Exception as e:
            raise NerException(e, sys) from e 
        
    def run_pipeline(self, ) -> None:
        """
        This method of TrainPipeline class is responsible for running complete pipeline
        """
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_transformation_artifact= self.start_data_transformation(data_ingestion_artifact= data_ingestion_artifact)
            model_trainer_artifact= self.start_model_trainer(data_transformation_artifacts= data_transformation_artifact)
            model_evaluation_artifact= self.start_model_evaluation(data_transformation_artifacts=data_transformation_artifact, model_trainer_artifact=model_trainer_artifact)
            model_pusher_artifact= self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)
            
        except Exception as e:
            raise NerException(e, sys) from e
        