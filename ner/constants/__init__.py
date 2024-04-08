import os
from datetime import datetime

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

ARTIFACTS_DIR = os.path.join("artifacts", TIMESTAMP)
LOGS_DIR = "logs"
LOGS_FILE_NAME = "ner.log"


MODELS_DIR = "models"
BEST_MODEL_DIR = "best_model"



# data_ingestion
DATA_INGESTION_ARTIFACTS_DIR = "DataIngestion"
GCP_DATA_FILE_NAME = "archive.zip"
CSV_DATA_FILE_NAME = "ner.csv"

# data_transformation constants
DATA_TRANSFORMATION_ARTIFACTS_DIR = "DataTransformation"
LABELS_TO_IDS_FILE_NAME = "labels_to_ids.pkl"
IDS_TO_LABELS_FILE_NAME = "ids_to_labels.pkl"
DF_TRAIN_FILE_NAME = "df_train.pkl"
DF_VAL_FILE_NAME = "df_val.pkl"
DF_TEST_FILE_NAME = "df_test.pkl"
UNIQUE_LABELS_FILE_NAME = "unique_labels.pkl"

# model_training constants
MODEL_TRAINING_ARTIFACTS_DIR= "ModelTrainer"
LEARNING_RATE= 5e-3
EPOCHS= 1
BATCH_SIZE= 2
BERT_MODEL_INSTANCE_NAME= "bert_model_instance.pt"
TOKENIZER_FILE_NAME="tokenizer.pkl"

# model_evaluation constants
MODEL_EVALUATION_ARTIFACTS_DIR = "ModelEvaluation"
BUCKET_NAME = "ner-using-bert-1"
GCP_MODEL_NAME = "model.pt"


APP_HOST = "0.0.0.0"
APP_PORT = 8080