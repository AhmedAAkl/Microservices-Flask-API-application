

from watson_developer_cloud import ToneAnalyzerV3
import pandas as pd
from collections import Counter

# create a tone analyzer instance, insert your credentials
tone_analyzer = ToneAnalyzerV3(
    iam_apikey= '',
    version='',
    url=''
)


# this method calculates the normalized emotion scores for each hotel
def get_normalized_score(hotels_scores):

    num_emotions = len(hotels_scores)
    #print(hotels_scores)
    # create empty dict of emotions
    emotions = ['Anger', 'Disgust', 'Fear', 'Joy', 'Sadness', 'Analytical', 'Confident', 'Tentative', 'Openness',
                'Conscientiousness', 'Extraversion', 'Agreeableness', 'Emotional Range']
    normalized_scores = {el:0 for el in emotions}

    for item in hotels_scores:
        for key in item:
            if key in normalized_scores:
                normalized_scores[key] = normalized_scores[key] + item[key]
            else:
                pass

    for k,v in normalized_scores.items():
        normalized_scores[k] = v / num_emotions

    #print(type(normalized_scores))

    return normalized_scores


'''
def preprocess_data(hotel_data):

    # drop columns with null values
    hotel_data.drop(['reviews.doRecommend', 'reviews.id', 'reviews.userCity', 'reviews.userProvince'], axis=1,inplace=True)

    return hotel_data
'''


def analyze_hotel_data(hotel_data):
    hotel_emotions_lst = []
    for index, review in hotel_data['reviews.text'].iteritems():
        analyzer_output = tone_analyzer.tone(review, content_type='text/plain').get_result()
        hotel_emotions_dict = {}
        for cat in analyzer_output['document_tone']['tone_categories']:
            for tone in cat['tones']:
                # Append the attributes to the data
                hotel_emotions_dict[tone['tone_name']] = tone['score']
        hotel_emotions_lst.append(hotel_emotions_dict)

    normalized_emotions = get_normalized_score(hotel_emotions_lst)
    return normalized_emotions


'''
normalized_hotels_emotions = []
for hotel_name in hotels_data.name.unique(): # for loop on unique hotels name
    one_hotel = hotels_data[hotels_data.name == hotel_name] # get data of that unique hotel name
    hotel_emotions_lst = []
    for index, review in one_hotel['reviews.text'].iteritems():
        analyzer_output = tone_analyzer.tone(review, content_type='text/plain').get_result()
        hotel_emotions_dict = {}
        for cat in analyzer_output['document_tone']['tone_categories']:
            for tone in cat['tones']:
                # Append the attributes to the data
                hotel_emotions_dict[tone['tone_name']] = tone['score']
        hotel_emotions_lst.append(hotel_emotions_dict)

    normalized_emotions = get_normalized_score(hotel_emotions_lst)
    normalized_hotels_emotions.append(normalized_emotions)
    print(len(hotel_emotions_lst))
    print(normalized_emotions)

#print(hotel_emotions_lst)
'''