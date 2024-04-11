# NameEntityRecognition

- Build end to end DL pipeline by implementing BERT for Named Entity Recognition (NER) and deploy to google cloud platform. 
- This means that we have trained BERT model to predict the IOB tagging of a custom text or a custom sentence in a token level (NLP Token classification task)
- NER is the process of identifying and classifying named entities into predefined entity categories.

## Workflows

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