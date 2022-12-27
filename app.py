import os
from pickle import GET
from webbrowser import get
import pandas as pd
from flask import Flask, make_response, request, jsonify
import sys
from flask_cors import CORS
import json

# Create Flask's `app` object
app = Flask(__name__)

def determine_age_group(age):
    age = int(age)
    if 16 <= age <= 17:
        return '16-17'
    elif 18 <= age <= 19:
        return '18-19'
    elif 20 <= age <= 24:
        return '20-24'
    elif 25 <= age <= 29:
        return '25-29'
    elif 30 <= age <= 34:
        return '30-34'
    elif 35 <= age <= 44:
        return '35-44'
    elif 45 <= age <= 54:
        return '45-54'
    elif 55 <= age <= 64:
        return '55-64'
    elif 65 <= age <= 69:
        return '65-69'
    else:
        raise Exception('age is not in the predefined range.')

def determine_scaled_scores_range(number_range_list, target_number):
  for number_range in number_range_list:
    if number_range == '-':
      continue
    number_range_split = number_range.split('-')
    if len(number_range_split) == 1:
      if number_range_split[0] == str(target_number):
        return number_range
    elif len(number_range_split) != 1:
      if int(number_range_split[0]) <= int(target_number) <= int(number_range_split[1]):
        return number_range


@app.route("/", methods=['GET'])
def hello():
  data = {
    'title': 'nabin khadka',
    'body': 'ye ma'
    }
  return jsonify(data), 200

@app.route("/", methods=['POST'])
def create_post():
  data = request.json
  print(data)
  print(data['age'])
  age_group = determine_age_group(data['age'])
  scaled_scores_data = pd.read_csv(f'./conversion-data/Age {age_group}.csv')
  raw_scores_list = ['BD', 'SI', 'DS', 'MR', 'VC', 'AR', 'SS', 'VP', 'IN', 'CD']  
  def get_scaled_scores(raw_scores_list, scaled_scores_data, determine_scaled_scores_range, data):
    resultList = {}
    try:
      for each_raw_score in raw_scores_list:
        print(each_raw_score)
        scores_list = scaled_scores_data[f'{each_raw_score}'].tolist()
        print('scores_list data column', scores_list)
        raw_score =  determine_scaled_scores_range(scores_list, data[f'{each_raw_score}']['value'])
        print('raw score we calculated', raw_score)
        scaled_scores = scaled_scores_data.loc[scaled_scores_data[f'{each_raw_score}'] == raw_score, 'Scaled Scores'].values[0]
        print('scaled scores after this calculation', scaled_scores)
        resultList[f'{each_raw_score}'] =  scaled_scores
      return resultList
    except Exception as e:
      print('what went wrong?', e)
  scaled_scores_result = get_scaled_scores(raw_scores_list, scaled_scores_data, determine_scaled_scores_range, data)
  print(scaled_scores_result)

  verbal_comprehension = scaled_scores_result['SI'] + scaled_scores_result['VC'] + scaled_scores_result['IN']
  perc_recognition = scaled_scores_result['BD'] + scaled_scores_result['MR'] + scaled_scores_result['VP']
  working_memory =  scaled_scores_result['DS'] + scaled_scores_result['AR']
  proc_speed = scaled_scores_result['SS'] + scaled_scores_result['CD']
  full_scale_score = verbal_comprehension + perc_recognition + working_memory + proc_speed
  print('full Scale scores are: ', full_scale_score)

  fsiq_data = pd.read_csv(f'./conversion-data/FSIQ.csv')
  
  FSIQ_score = fsiq_data.loc[fsiq_data['Sum of scaled score'] == full_scale_score, 'FSIQ'].values[0]
  print(FSIQ_score)
  return str(FSIQ_score)


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
