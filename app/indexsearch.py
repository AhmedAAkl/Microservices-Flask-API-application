from elasticsearch import Elasticsearch
import pandas as pd
import ast
from app.model import analyze_hotel_data
from datetime import datetime
from flask import Flask, jsonify, request


es = Elasticsearch('http://localhost:9200')


# index hotels method
def index_hotels(data, watson_data):
    print(watson_data)
    for hotel_name in data.name.unique():   # for loop on unique hotels name
        final_data = {}
        one_hotel = data[data.name == hotel_name] # get data of that unique hotel name
        #normalized_emotions = analyze_hotel_data(one_hotel)

        # get most important data
        new_hotel_data = one_hotel[['name', 'reviews.text']]
        reviews_list = new_hotel_data['reviews.text'].tolist()
        #final_data['name'] = hotel_name
        #final_data['reviews'] = reviews_list
        #tone_analysis_data = watson_data

        #print(reviews_list)
        #print(watson_data[hotel_name])
        final_data[hotel_name] = {
            'review': reviews_list,
            'Tone_analysis': watson_data[hotel_name]
        }
        #final_data['Tone_analysis'] = watson_data[hotel_name]   # add the output of tone analyzer to data dict.
        #print(final_data)

        # save the final_data dictionary to the elastic Search
        es.index(index="hotels_a",body = final_data)
        return final_data

'''
def search_hotel(query): # search by hotel name
    output = es.search(index='hotels_a', body={'query': {'match': {'name': query}}})
    return output
'''
#from app.model import analyze_hotel_data
#w_data =
#index_hotels(data)
#print(search_hotel('Hotel Russo Palace'))
# print(es)
