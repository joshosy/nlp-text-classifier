# News article classifier
Classifier for news articles about a specific topic of interest.
This repo contains two parts:
1. Scrapy script to scrape news articles from the web and assemble dataset
2. Jupyter notebook to describe model development of news classifer

## News scraping process
Currently scrapes a few specified urls that can be tweaked. 
The Xpath/CSS locators may require updates if the news sites change their DOM significantly. To run this yourself, run *main.py* after inspecting and modifying (if necessary) the spiders defined in *news_scrape/scrape.py*. 
Several scrapy settings are controlled by the config file, modify as desired.

## Data labelling
I manually labelled the dataset into three different classes (0/1/2) for my domain problem.
The first task was defined as distinguishing between classes 0 and 1/2,
The second task is to distinguish between classes 1 and 2.

## NLP model development
To follow the notebook you'll need your own labels.csv and raw_news.csv.
The notebook describes three major steps:
1. Text data augmentation to increase the dataset size and address class imbalance
    1. Sentence shuffling using Spacy parsing model
    2. Synonym replacement using NLTK's WordNet
    3. Roundtrip translation using FSMT (FairSeq MachineTranslation) models from HuggingFace (EN > DE > EN)
    (This takes a fair bit of time so the notebook exports the augmented dataset for future reloads without going thru data augmentation all over again.)
2. Fine-tuning of RoBERTa model on the first classification problem and model evaluation
3. Fine-tuning of RoBERTa model on the second (harder because classes 1 and 2 are subtopics of a common topic) classification problem and model evaluation