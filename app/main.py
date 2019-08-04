#!flask/bin/python

import pandas as pd
from flask import Flask, request, render_template, make_response
from app.model import analyze_hotel_data
from app.indexsearch import index_hotels
import pickle

app = Flask(__name__)


data = pd.read_csv('/7282_1.csv',index_col=False)

# I used it for first 100 elements as I have limited 2500 for IBM tone analyzer, which finished during testing :)
data = data.head(100).copy()
print(data.shape)
data = data[data.categories == 'Hotels']
final_data = {}
analysis_data = {}

'''
@app.route('/', methods=['GET','POST'])
def home():
    s = "HI there"
    return s
'''


@app.route('/analyzer', methods=['POST','GET'])
def analyze_data():

    for hotel_name in data.name.unique():  # for loop on unique hotels name
        one_hotel = data[data.name == hotel_name]  # get data of that unique hotel name
        normalized_emotions = analyze_hotel_data(one_hotel)

        #analysis_data['name'] = hotel_name
        #analysis_data['Tone_analysis'] = normalized_emotions  # add the output of tone analyzer to data dict.
        analysis_data[hotel_name] = normalized_emotions
        with open('analysis_data.p', 'wb') as fp:
            pickle.dump(analysis_data, fp, protocol=pickle.HIGHEST_PROTOCOL)

        #print(final_data)
    return analysis_data


@app.route('/indexer', methods=['POST','GET'])
def index_data():

    with open('analysis_data.p', 'rb') as fp:
        analysis_data = pickle.load(fp)
    global final_data
    final_data = index_hotels(data,analysis_data)
    return final_data


if __name__ == '__main__':
    app.run(debug=True)


'''
@app.route('/search', methods=['GET','POST'])
def search():
    #q = request.args.get("q")

    q = request.form.get('q')
    if q is not None:
        resp = search_hotel(q)
        return render_template("index.html", q=q, response=resp)
    return render_template('index.html')
'''