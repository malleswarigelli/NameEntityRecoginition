# NameEntityRecognition

- Build an end to end pipeline for Named Entity Recognition (NER) by a pretrained Huggingface transformer, BERT and deploy to google cloud platform using Docker, CI/CD tool: CircleCI. 
- We implemented pretrained HuggingFace Transformer, BERT model to predict the IOB tagging of a custom text or a custom sentence in a token level (NLP Token classification task)
- NER is the process of identifying and classifying named entities into predefined entity categories.
- Project structure is made with a data science project template. This template ensured modularity, reusability, and maintainability of the code. It included modules for logging, exception handling, and utilities.

# Flow of End to End robust automatic pipeline:

![NER_End to End_Architexture](https://github.com/malleswarigelli/NameEntityRecoginition/assets/84688050/99ccaee1-35f3-49b9-9492-bf4f9e8b9f00)
## Training pipeline:
- Data Ingestion: ingested .zip file from GCP bucket, unzip to .csv file. It contains text and label columns. Data validation is not required here, since the NLP dataset is simple with 2 columns.
- Data Transformation: Read ner.csv to pandas dataframe, split into train, test, val sets, extract labels column to get unique_labels, assign values to labels and are saved as pickle files.
- Model Trainer: trained pretrained BERT transformer model on the prepared dataset. 
- Model Evaluation: evaluated the model's performance on a test dataset and calculated metrics accuracy.
- Model Pusher: the model with highest accuracy is pushed to GCP bucket 
## Prediction pipeline: 
- For user provided text data apply tokenizer for vector embedding, predict the named entity with trained BERT model from GCP bucket and classify them.
  
- WebApplication: Built FASTAPI web application
- Deployed the pipeline to GCP virtual machine using containers Docker, GCP artifact registry, CI/CD tool: CircleCI


## Files to update for each component
 - constants
 - config_entity
 - artifact_entity
 - components
 - pipeline
 - app.py



## Live matarials docs

[link](https://docs.google.com/document/d/1UFiHnyKRqgx8Lodsvdzu58LbVjdWHNf-uab2WmhE0A4/edit?usp=sharing)


## Git commands

```bash
git add .

git commit -m "Updated"

git push origin main
```

# install pytorch for cpu (install this for every project)
```bash
pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
```

## GCP Configuration

```bash
# create GCP account
# Gcloud cli download link: https://cloud.google.com/sdk/docs/install#windows

gcloud init # worked with cmd but not with bash
```


## How to run?

```bash
conda create -n nerproject python=3.8 -y
```

```bash
conda activate nerproject
```

```bash
pip install -r requirements.txt
```

```bash
python app.py
```
# GCP CICD Deployment with CircleCI:
- artifact registry --> create a repository
- change line 42,50,72,76,54 in .circleci/config.yml
- Open circleci --> create a project


# Set Environment variables in CircleCI
GCLOUD_SERVICE_KEY --> service account

GOOGLE_COMPUTE_ZONE = asia-south1 # select your choice

GOOGLE_PROJECT_ID

# Create a VM instances & setup scripts
