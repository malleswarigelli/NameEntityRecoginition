# **Fine-tuning BERT for named-entity recognition**

In this project, we used **BertForTokenClassification** which is included in the [Transformers library](https://github.com/huggingface/transformers) by HuggingFace. This model has BERT as its base architecture, with a token classification head on top, allowing it to make predictions at the token level, rather than the sequence level. Named entity recognition is typically treated as a token classification problem.
- This is a **transfer learning** approach, i.e. first pretraining on a large neural network in an unsupervised way, and then fine-tuning that neural network on a task of interest. In this case, BERT is a neural network pretrained on 2 tasks: masked language modeling and next sentence prediction. Now, we are going to fine-tune this network on a NER dataset. Fine-tuning is supervised learning, so this means we will need a labeled dataset.

If you want to know more about BERT, I suggest the following resources:
* the original [paper](https://arxiv.org/abs/1810.04805)
* Jay Allamar's [blog post](http://jalammar.github.io/illustrated-bert/) as well as his [tutorial](http://jalammar.github.io/a-visual-guide-to-using-bert-for-the-first-time/)

# Goal: Build an end to end pipeline for Named Entity Recognition (NER) by a pretrained Huggingface transformer, BERT and deploy to google cloud platform using Docker, CI/CD tool: CircleCI. 
- We implemented pretrained HuggingFace Transformer, BERT model [bert-base-cased](https:huggingface.co/google-bert/bert-base-cased) to predict the IOB tagging of a custom text or a custom sentence in a token level (NLP Token classification task)
- NER is the process of identifying and classifying named entities into predefined entity categories.
- Project structure is made with a data science project template. This template ensured modularity, reusability, and maintainability of the code. It included modules for logging, exception handling, and utilities.

# Flow of End to End robust automatic pipeline:

![NER_End to End_Architexture](https://github.com/malleswarigelli/NameEntityRecoginition/assets/84688050/99ccaee1-35f3-49b9-9492-bf4f9e8b9f00): 
# **Downloading and preprocessing the data**
Named entity recognition (NER) uses a specific annotation scheme **[IOB-tagging](https://en.wikipedia.org/wiki/Inside%E2%80%93outside%E2%80%93beginning_(tagging)**, which stands for Inside-Outside-Beginning. Each tag indicates whether the corresponding word is *inside*, *outside* or at the *beginning* of a specific named entity. The reason this is used is because named entities usually comprise more than 1 word. 

- Let's have a look at an example. If you have a sentence like "Barack Obama was born in Hawaï", then the corresponding tags would be   [B-PERS, I-PERS, O, O, O, B-GEO]. B-PERS means that the word "Barack" is the beginning of a person, I-PERS means that the word "Obama" is inside a person, "O" means that the word "was" is outside a named entity, and so on. So one typically has as many tags as there are words in a sentence.

For training a DL model for NER, it requires data in IOB format. There are many annotation tools which let you create these kind of annotations automatically (such as Spacy's [Prodigy](https://prodi.gy/), [Tagtog](https://docs.tagtog.net/) or [Doccano](https://github.com/doccano/doccano)). You can also use Spacy's [biluo_tags_from_offsets](https://spacy.io/api/goldparse#biluo_tags_from_offsets) function to convert annotations at the character level to IOB format.

Here, we used a NER dataset from Kaggle that is already in IOB format. One has to go to this web page, download the dataset, add to GCP bucket. You can directly unzip it, and upload the csv file to this notebook. Let's print out the first few rows of this csv file contains sentense(text), IOB tags (labels)
![data](https://github.com/malleswarigelli/NameEntityRecoginition/assets/84688050/384f6f57-d36c-41bd-9e53-0f18f3742341)
- dataset (~50k rows)
- There are 17 different category tags: {'B-art', 'B-eve', 'B-geo', 'B-gpe', 'B-nat', 'B-org', 'B-per', 'B-tim', 'I-art', 'I-eve', 'I-geo', 'I-gpe', 'I-nat', 'I-org', 'I-per', 'I-tim', 'O'}

## Training pipeline:
- Data Ingestion: ingested .zip file from GCP bucket, unzip to .csv file. It contains text and label columns. Data validation is not required here, since the NLP dataset is simple with 2 columns.
- Data Transformation: Read ner.csv to pandas dataframe, split into train, test, val sets, create 2 dictionaries: one that maps individual tags to indices, and one that maps indices to their individual tags. This is necessary in order to create the labels (as DL needs numbers = indices, rather than words = tags), all these saved as pickle files.
- Model Trainer: pretrained Huggingface BERT transformer `bert-based-case` model is trained on the custom dataset. 
- Model Evaluation: evaluated the model's performance on a test dataset and calculated metrics accuracy.
- Model Pusher: the model with highest accuracy is pushed to GCP bucket 
## Prediction pipeline: 
- For user provided text data apply tokenizer for vector embedding, predict the named entity with trained BERT model from GCP bucket and classify them.  
- WebApplication: Built FASTAPI web application
## Deployment: 
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
