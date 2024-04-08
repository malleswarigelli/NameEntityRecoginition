import os
import sys
import numpy as np
import pandas as pd
from pandas import DataFrame


from ner.configuration.gcloud import GCloud
from ner.constants import *
from ner.entity.config_entity import DataTransformationConfig
from ner.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact
from ner.logger import logging
from ner.exception import NerException
from ner.utils.utils import MainUtils




class DataTransformation:    
    def __init__(self, data_transformation_config:DataTransformationConfig,
                 data_ingestion_artifact:DataIngestionArtifact) -> None:
        """
        :param data_transformation_config: configuration for data transformation (obj of DataTransformationConfig class)
        :param data_ingestion_artifact: artifact of DataIngestion component
        """
        try:
            self.data_ingestion_artifact= data_ingestion_artifact
            self.data_transformation_config= data_transformation_config
            self.gcloud= GCloud() # to push some o/p files
            self.utils= MainUtils()
            
        except Exception as e:
            raise NerException(e,sys)
        
    def splitting_data(self, df:DataFrame)->dict:
        """
        Method Name :   splitting_data
        Description :   This method splits the data into train, test, val sets 
        
        Output      :   dict
        On Failure  :   Write an exception log and then raise an exception
        """
               
        logging.info("Entered the splitting_data method of Data transformation class")
        try:
            # Taking subset of data for training
            df = df[0:1000]

            labels = [i.split() for i in df["labels"].values.tolist()] # each row would be 1 list, [['O', 'O', 'B-per', 'B-geo', 'O' etc]]
            
            unique_labels = set()
            for lb in labels:
                [unique_labels.add(i) for i in lb if i not in unique_labels] # o/p set {'B-art','B-geo','B-per','B-org','B-tim','O'} etc

            labels_to_ids = {k: v for v, k in enumerate(unique_labels)} # {'B-art':0,'B-geo':1,'B-per':2,'B-org':3,'B-tim':4,'O':5}
            ids_to_labels = {v: k for v, k in enumerate(unique_labels)}

            df_train, df_val, df_test = np.split(
                df.sample(frac=1, random_state=42),
                [int(0.8 * len(df)), int(0.9 * len(df))],
            )

            logging.info("Exited the splitting_data method of Data transformation class")
            return (
                labels_to_ids,
                ids_to_labels,
                df_train,
                df_val,
                df_test,
                unique_labels,
            )

        except Exception as e:
            raise NerException(e, sys) from e
        
        
        
    def initiate_data_transformation(self,)->DataTransformationArtifact:
        """
        Method Name :   initiate_data_transformation
        Description :   This method initiates the data transformation components of training pipeline 
        
        Output      :   DataTransformationArtifact
        On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Entered the initiate_data_transformation method of Data transformation class")
        try:
            # Creating Data transformation directory
            os.makedirs(self.data_transformation_config.data_transformation_dir,exist_ok=True) # artifacts/data_transformation_artifacts
            logging.info(f"Created {os.path.basename(self.data_transformation_config.data_transformation_dir)} directory.") # data_transformation_artifacts
            
            # load ner.csv data
            df = pd.read_csv(self.data_ingestion_artifact.csv_data_file_path)
            
            (
                labels_to_ids,
                ids_to_labels,
                df_train,
                df_val,
                df_test,
                unique_labels,
            ) = self.splitting_data(df=df)
            logging.info("Splitted the data")
            
            # we need .pkl files for ease

            labels_to_ids_pkl= self.utils.dump_pickle_file(output_filepath=self.data_transformation_config.labels_to_ids_path, data=labels_to_ids)            
            logging.info(f"Saved the labels to ids pickle file to Artifacts directory. File name - {os.path.basename(self.data_transformation_config.labels_to_ids_path)}")

            ids_to_labels_pkl= self.utils.dump_pickle_file(output_filepath=self.data_transformation_config.ids_to_labels_path,data=ids_to_labels)
            logging.info(f"Saved the ids to labels pickle file to Artifacts directory. File name - {os.path.basename(self.data_transformation_config.ids_to_labels_path)}")

            # push ids_to_labels.pkl to gcloud bucket since we need for predictions
            self.gcloud.sync_folder_to_gcloud(
                gcp_bucket_url=BUCKET_NAME,
                filepath=self.data_transformation_config.ids_to_labels_gcp_path,
                filename=IDS_TO_LABELS_FILE_NAME,
            )
            logging.info(f"Uploaded the ids to labels pickle file to Google cloud storage. File name - {os.path.basename(self.data_transformation_config.ids_to_labels_path)}")

            df_train_pkl= self.utils.dump_pickle_file(output_filepath=self.data_transformation_config.df_train_path, data=df_train)
            logging.info(f"Saved the train df pickle file to Artifacts directory. File name - {os.path.basename(self.data_transformation_config.df_train_path)}" )

            df_val_pkl= self.utils.dump_pickle_file(output_filepath=self.data_transformation_config.df_val_path, data=df_val)
            logging.info(f"Saved the val df pickle file to Artifacts directory. File name - {os.path.basename(self.data_transformation_config.df_val_path)}")

            df_test_pkl= self.utils.dump_pickle_file(output_filepath=self.data_transformation_config.df_test_path, data=df_test)
            logging.info(f"Saved the test df pickle file to Artifacts directory. File name - {os.path.basename(self.data_transformation_config.df_test_path)}")

            unique_labels_pkl= self.utils.dump_pickle_file(output_filepath=self.data_transformation_config.unique_labels_path, data=unique_labels)
            logging.info(f"Saved the unique labels pickle file to Artifacts directory. File name - {os.path.basename(self.data_transformation_config.unique_labels_path)}")

            data_transformation_artifact = DataTransformationArtifact(
                labels_to_ids_path= labels_to_ids_pkl,
                ids_to_labels_path= ids_to_labels_pkl,
                df_train_path= df_train_pkl,
                df_val_path= df_val_pkl,
                df_test_path= df_test_pkl,
                unique_labels_path= unique_labels_pkl,
            )
            logging.info("Exited the initiate_data_transformation method of Data transformation class")
            return data_transformation_artifact

        except Exception as e:
            raise NerException(e, sys) from e