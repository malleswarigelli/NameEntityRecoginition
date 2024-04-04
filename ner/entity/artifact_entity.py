

from dataclasses import dataclass
import os
from ner.constants import *


@dataclass
class DataIngestionArtifact:
    zip_data_file_path:str
    csv_data_file_path:str