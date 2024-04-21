from flask import Flask, render_template, jsonify, request, redirect
import json
import os
from flask.helpers import url_for
import pandas as pd
import similar
import keywords

app = Flask(__name__)

word_df = pd.DataFrame()
no_df = pd.DataFrame()


@app.route('/')
def start_page():
    return render_template('index.html')


@app.route('/extraction')
def extraction():
    return render_template('extraction.html')


@app.route('/similarity')
def similarity():
    return render_template('similarity.html')


@app.route('/get_table_data', methods=['POST'])
def get_table_data():
    if request.method == 'POST':
        text = request.form.get("text")
        lang = request.form.get("lang")
        print(text)
        print(lang)
        word_df, no_df = similar.similarity(text, lang)
        print('send data')
        print(no_df)
        json_tdata = word_df.to_dict(orient='records')
        json_cdata = no_df.to_dict(orient='records')
        # json_dict = {}
        # json_dict['data'] = json.loads(json_data)
        return jsonify({'tableData': json_tdata, 'chartData': json_cdata})


@app.route('/get_keywords', methods=['POST'])
def get_keywords():
    if request.method == 'POST':
        text = request.form.get("text")
        lang = request.form.get("lang")
        print(text)
        print(lang)
        wordsdata = keywords.get_keywords(text, lang)
        json_wdata = wordsdata.to_dict(orient='records')
        print(json_wdata)
        return jsonify({'wordsData': json_wdata})


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8094, debug=True)
