import ast
import pandas as pd


def extract_review_activity(df):
    cols=['review_id','acc_num','asin','sortTimestamp','rating','helpfulVotes','reviewCount','title','text','images_posted','verifiedPurchase']
    
    extracted_data = []
    for index, row in df.iterrows():
        print("Extracting {} out of {}...".format(index+1,len(df)))
        contribution_data = check_empty_data(row['reviewer_contributions'])
        if contribution_data != []:
            count = 0
            for data in contribution_data:
                new_data = extract_data(dict(data))
                if new_data != []:
                    extracted_data.append([review_id,acc_num,asin,sortTimestamp,rating,helpfulVotes,reviewCount,title,text,images_posted,verifiedPurchase])
                    count += 1
                    print("Added {} out of {} from reviewer contribution...".format(count,len(data)))

            print("Reviewer Activity Dataset currently has {} rows...\n".format(len(extracted_data)))

    review_activity_df = pd.DataFrame(extracted_data,columns=cols)
    
    print("Starting preprocessing on Reviewer Activity Dataset soon..")
    return review_activity_df.drop_duplicates(subset='review_id')

def check_empty_data(row):
    try:
        return ast.literal_eval(row)
    except:
        return []

def extract_data(data):
    if 'ideas' not in data['id']:
        try:
            acc_num = row['acc_num']
            review_id = data['externalId']
            sortTimestamp = data['sortTimestamp']
            text = data['text']
            asin = data['product']['asin']
            verifiedPurchase = data['verifiedPurchase']
            rating = rating_value(data)
            helpfulVotes = helpfulVotes_value(data)
            reviewCount = reviewCount_value(data)
            title = title_value(data)
            images_posted = image_posted_value(data)

            return [review_id,acc_num,asin,sortTimestamp,rating,helpfulVotes,reviewCount,title,text,images_posted,verifiedPurchase]
        except:
            return []
    return []

def helpfulVotes_value(data):
    if 'helpfulVotes' not in data:
        return 0
    return data['helpfulVotes']

def image_posted_value(data):
    if 'images' not in data:
        return 0
    return len(data['images'])

def rating_value(data):
    if 'rating' not in data:
        return 0
    return data['rating']

def reviewCount_value(data):
    if 'reviewCount' not in data:
        return 0
    return data['reviewCount']

def title_value(data):
    if 'title' not in data:
        return ''
    return data['title']

