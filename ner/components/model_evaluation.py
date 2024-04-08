import os
import sys
import torch
import numpy as np
import pandas as pd
from pandas import DataFrame
from torch.utils.data import DataLoader
from ner.components.model_trainer import DataSequence

from ner.configuration.gcloud import GCloud
from ner.constants import *
from ner.entity.config_entity import ModelEvaluationConfig
from ner.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifacts
from ner.logger import logging
from ner.exception import NerException
from ner.utils.utils import MainUtils


class ModelEvaluation():
    def __init__(self, data_transformation_artifact:DataTransformationArtifact,
                 model_trainer_artifact:ModelTrainerArtifact,
                 model_evaluation_config:ModelEvaluationConfig                 
                 ) -> None:
        
        """
        :param model_evaluation_config: configuration for model evaluation (obj of ModelEvaluationConfig class)
        :param data_transformation_artifact: artifact of DataTransformation component
        :param model_trainer_artifact: artifact of ModelTrainer component
        
        """
        try:         
            self.model_evaluation_config= model_evaluation_config
            self.model_trainer_artifact= model_trainer_artifact
            self.data_transformation_artifact= data_transformation_artifact
            self.gcloud= GCloud()
            self.utils= MainUtils()
            
        except Exception as e:
            raise NerException(e,sys)
        
    def evaluate(self, model:object, df_test:DataFrame) -> float:
        """
        Method Name :   evaluate
        Description :   This function loads tokenizer.pkl, labels_to_ids.pkl from model_trainer_artifacts, trained model and do predictions on test data, 
        
        Output      :   Returns model evaluation artifact (trained_model_accuracy and is_model_accepted)
        On Failure  :   Write an exception log and then raise an exception
        """
              
        logging.info(f"Entered evaluate method of ModelEvaluation")
        
        try: 
            # load tokenizer.pkl, labels_to_ids.pkl file
            tokenizer= self.utils.load_pickle_file(filepath= self.model_trainer_artifact.tokenizer_file_path)
            logging.info(f"Loaded tokenizer.pkl file from model_trainer_artifact")
            labels_to_ids= self.utils.load_pickle_file(filepath= self.data_transformation_artifact.labels_to_ids_path)
            logging.info(f"Loaded labels_to_ids.pkl file from data_transformation_artifact")
            
            test_dataset= DataSequence(df= df_test, tokenizer=tokenizer, labels_to_ids=labels_to_ids)
            logging.info(f"Loaded test data for evaluation")
            
            test_dataloader= DataLoader(test_dataset, batch_size=1)
            
            # GPU setup
            use_cuda= torch.cuda.is_available()
            device= torch.device("cuda" if use_cuda else "cpu")
            
            if use_cuda:
                model= model.cuda()
                
            total_acc_test=0.0
            
            for test_data, test_label in test_dataloader:
                test_label = test_label.to(device)
                mask = test_data["attention_mask"].squeeze(1).to(device)
                input_id = test_data["input_ids"].squeeze(1).to(device)
                _, logits = model(input_id, mask, test_label)

                for i in range(logits.shape[0]):
                    logits_clean = logits[i][test_label[i] != -100]
                    label_clean = test_label[i][test_label[i] != -100]

                    predictions = logits_clean.argmax(dim=1)
                    acc = (predictions == label_clean).float().mean()
                    total_acc_test += acc

            val_accuracy = total_acc_test / len(df_test)

            print(f"Test Accuracy: {val_accuracy: .3f}")

            logging.info("Exited the evaluate method of Model evaluation class")
            return val_accuracy

        except Exception as e:
            raise NerException(e, sys) from e                        
        
        
    def initiate_model_evaluation(self,) -> ModelEvaluationArtifacts:
        """
        Method Name :   initiate_model_evaluation
        Description :   This function initiates a model evaluation steps
        
        Output      :   Returns model evaluation artifact
        On Failure  :   Write an exception log and then raise an exception
        """
              
        logging.info(f"Entered initiate_model_evaluation method of ModelEvaluation class")
        try: 
           
           os.makedirs(self.model_evaluation_config.model_training_artifacts_dir, exist_ok=True)
           logging.info(f"Created {os.path.basename(self.model_evaluation_config.model_training_artifacts_dir)} directory.")
           
           # load current trained model
           model= torch.load(self.model_trainer_artifact.bert_model_train_path)
           logging.info(f"Loaded {model} from model_trainer_artifact")
           
           # load test.pkl file
           test_pkl= self.utils.load_pickle_file(filepath= self.data_transformation_artifact.df_test_path)
           logging.info(f"Loaded test.pkl file from data_transformation_artifact")
           
           trained_model_accuracy= self.evaluate(model=model, df_test=test_pkl)
           logging.info(f"Current trained model accuracy on test dataset is - {trained_model_accuracy}")
           
           # loading production model from google container registry (GCR)
           self.gcloud.sync_folder_from_gcloud(gcp_bucket_url= BUCKET_NAME, 
                                                      filename= GCP_MODEL_NAME, 
                                                      destination= self.model_evaluation_config.gcp_model_path) 
           # Checking whether data file exists in the artifacts directory or not
           if os.path.exists(self.model_evaluation_config.gcp_local_path) == True:
               logging.info("GCP model file available in the root directory")
               
               gcp_model = torch.load(self.model_evaluation_config.gcp_local_path, map_location=torch.device('cpu'))
               logging.info("GCP model loaded")
               
               gcp_model_accuracy = self.evaluate(model=gcp_model, df_test= test_pkl)
               logging.info(f"Calculated the gcp model's Test accuracy. - {gcp_model_accuracy}")
               
               tmp_best_model_score = (0 if gcp_model_accuracy is None else gcp_model_accuracy)
           
           else:
               tmp_best_model_score = 0
               logging.info("GCP model is not available locally for comparison.")
                
           model_evaluation_artifact = ModelEvaluationArtifacts(
                trained_model_accuracy=trained_model_accuracy,
                is_model_accepted=trained_model_accuracy > tmp_best_model_score)
           
           logging.info("Exited the initiate_model_evaluation method of Model evaluation class")
           return model_evaluation_artifact

        except Exception as e:
            raise NerException(e, sys) from e
           