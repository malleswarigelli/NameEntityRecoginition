# NameEntityRecognition
NER: DL NLP Token classification task using PyTorch Huggingfacce BERT library

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

# install pytorch for cpu
```bash
pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
```

## GCP Configuration

```bash
# Gcloud cli download link: https://cloud.google.com/sdk/docs/install#windows

gcloud init
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