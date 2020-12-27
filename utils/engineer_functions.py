from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import nltk
import numpy as np

import pandas as pd

from utils.clean import clean_text


def check_deleted_data(data):
    try:
        null_review = float(review)
        if math.isnan(null_review):
            return True
        return False
    except:
        return False

def check_deleted_text(text):
    new_data = []
    for data in text:
        if check_deleted_data(data):
            new_data.append(1)
        else:
            new_data.append(0)
    return new_data

def fuzzy_check_reviews(text, fuzzy_match_list, mode):
    print("Fuzzy Matching...")
    match = fuzzy_match_results(fuzzy_match_list,text)

    print("Fuzzy Matching Completed...")

    match_df = pd.DataFrame(match,columns = ['brand', 'score'])
    match_df['probability_brand'] = fuzzy_score(list((match_df['score'])))
    match_df['class_assignment'] = 0

    match_df.loc[match_df.probability_brand >= 1, "class_assignment"] = 1

    return list(match_df['class_assignment'])

def check_sample_text(text):
    return [1 if 'sample' in data else 0 for data in text]

def fuzzy_match_results(matching_list, text_list):
    return list(map(lambda x: process.extractOne(x, matching_list, scorer=fuzz.token_set_ratio,processor=lambda x: x), text_list))

def fuzzy_score(score_list):
    return [(score / (102-score)) for score in score_list]

def temp_new_text(text):
    new_text = []
    for data in text:
        new_text.append(check_null_text(data))
    return new_text

def check_null_text(text):
    try:
        null_data = float(text)
        if math.isnan(null_data):
            return ""
        else:
            return str(text)
    except:
        return str(text)