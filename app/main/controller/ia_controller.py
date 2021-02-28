from flask import request
from flask_restplus import Resource
from zipfile import ZipFile
from ..model.dto import IADto
from sklearn.ensemble import RandomForestClassifier
import joblib
import sklearn
from sklearn.preprocessing import LabelEncoder
from pickle import dump
from pickle import load
import pandas as pd
import os
import json
import pathlib
import warnings

api = IADto.api
_model = IADto.model

with ZipFile(pathlib.Path(__file__).parent / 'controller.zip', 'r') as zipObj:
    zipObj.extractall(pathlib.Path(__file__).parent)

#model = joblib.load(open(pathlib.Path(__file__).parent / 'model.sav', 'rb'))
estimator = None
with warnings.catch_warnings():
      warnings.simplefilter("ignore", category=UserWarning)
      with open(pathlib.Path(__file__).parent /  'model.save', 'rb') as scaler:
        estimator = joblib.load(scaler)


def create_clean_df(matterData):
    df = pd.DataFrame([matterData])

    df = vectorize(df)

    return df

def vectorize(df):
    categorical_cols = [a for a in df.columns if a != 'Year']

    for x in categorical_cols:
        with open(pathlib.Path(__file__).parent /  (x + '.pkl'), 'rb') as scaler:
            le = load(scaler)
            df[x] = le.transform(df[x])
    
    return df

def unvectorize(df):
    with open(pathlib.Path(__file__).parent /  'CourtSumary.pkl', 'rb') as scaler:
        le = load(scaler)
        df['CourtSumary'] = le.inverse_transform(df['CourtSumary'])
    return df

def jsonfy(df):
    result = df.to_json(orient="split")
    parsed = json.loads(result)
    return json.dumps(parsed, indent=4)

@api.route('/')
class Hello(Resource):
    @api.response(201, 'IA predicted.')
    @api.doc('predict value')
    @api.expect(_model, validate=True)
    def post(self):
        data = []
        try:
            df = create_clean_df(request.json)
            resposta = estimator.predict(df)
            df['CourtSumary'] = resposta
            df = unvectorize(df)
            data.append(df['CourtSumary'].to_string(index=False).strip())
            return json.dumps(data) 
        except ValueError:
            data.append('Erro: Não foi encontrado a palavra-chave nos nossos registros atuais')
            return json.dumps(data)
   
