
from dataclasses import dataclass
import os
from ner.constants import *


@dataclass
class DataIngestionConfig:
    data_ingestion_dir:str= os.path.join(ARTIFACTS_DIR, DATA_INGESTION_ARTIFACTS_DIR)
    gcp_data_file_path:str= os.path.join(data_ingestion_dir, GCP_DATA_FILE_NAME)
    output_data_file_path:str= data_ingestion_dir
    csv_data_file_path:str= os.path.join(data_ingestion_dir, CSV_DATA_FILE_NAME)
        
@dataclass
class DataTransformationConfig:
    data_transformation_dir:str= os.path.join(ARTIFACTS_DIR, DATA_TRANSFORMATION_ARTIFACTS_DIR)
    labels_to_ids_path:str= os.path.join(data_transformation_dir,LABELS_TO_IDS_FILE_NAME) #labels_to_ids.pkl
    ids_to_labels_path:str= os.path.join(data_transformation_dir,IDS_TO_LABELS_FILE_NAME) # ids_to_labels.pkl
    ids_to_labels_gcp_path:str= os.path.join(data_transformation_dir)
    df_train_path:str= os.path.join(data_transformation_dir,DF_TRAIN_FILE_NAME) # "df_train.pkl"
    df_val_path:str= os.path.join(data_transformation_dir,DF_VAL_FILE_NAME) # "df_val.pkl"
    df_test_path:str= os.path.join(data_transformation_dir, DF_TEST_FILE_NAME) # "df_test.pkl"
    unique_labels_path:str= os.path.join(data_transformation_dir, UNIQUE_LABELS_FILE_NAME) # "unique_labels.pkl"
    
@dataclass
class ModelTrainerConfig:
    model_training_dir= os.path.join(ARTIFACTS_DIR, MODEL_TRAINING_ARTIFACTS_DIR) # ModelTrainer
    bert_model_instance_path= os.path.join(model_training_dir, GCP_MODEL_NAME) # "model.pt"
    tokenizer_file_path= os.path.join(model_training_dir, TOKENIZER_FILE_NAME) #tokenizer.pkl"
    tokenizer_file_gcp_path= os.path.join(model_training_dir) # ModelTrainer
    
@dataclass
class ModelEvaluationConfig:
    model_evaluation_dir= os.path.join(ARTIFACTS_DIR, MODEL_EVALUATION_ARTIFACTS_DIR) #ModelEvaluation dir
    gcp_model_path:str= os.getcwd() # get model to current working directory
    gcp_local_path:str= GCP_MODEL_NAME # "model.pt"
    
@dataclass
class ModelPusherConfig:
    bucket_name:str= BUCKET_NAME # "ner-using-bert-1"
    model_name:str= GCP_MODEL_NAME # "model.pt"
    upload_model_path: str = os.path.join(ARTIFACTS_DIR, MODEL_TRAINING_ARTIFACTS_DIR) # artifacts/ModelTrainer
    
@dataclass
class ModelPredictorConfig:
    tokenizer_local_path:str= TOKENIZER_FILE_NAME # tokenizer.pkl"
    ids_to_labels_local_path:str= IDS_TO_LABELS_FILE_NAME # "ids_to_labels.pkl"
    best_model_dir:str= BEST_MODEL_DIR # "best_model"
    best_model_from_gcp_path:str= os.path.join(BEST_MODEL_DIR) # /best_model
    best_model_path:str= os.path.join(BEST_MODEL_DIR, GCP_MODEL_NAME) # best_model/model.pt
    