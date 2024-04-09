import os
import sys
from ner.constants import *
from ner.exception import NerException
from ner.pipeline.train_pipeline import TrainingPipeline


def training():
    try:
        train_pipeline= TrainingPipeline()
        train_pipeline.run_pipeline()
        
    except Exception as e:
            raise NerException(e, sys)
        
        
if __name__ == "__main__":
    training()