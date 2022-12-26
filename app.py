from crypt import methods
from distutils.command.config import config
from distutils.command.upload import upload
import json
from unittest import result
from urllib import response
import re
import pandas as pd
import sqlite3
from flask import Flask, jsonify, render_template
from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
from unidecode import unidecode

app = Flask(__name__)
app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
        'title':LazyString(lambda:'Binar Acadey Gold Challange - Data Scientist'),
        'version':LazyString(lambda:'1.0.0'),
        'description':LazyString(lambda:'Membuat API Cleansing Data')
    },
    host = LazyString(lambda:request.host)
)
swagger_config = {
    "headers":[],
    "specs":[
        {
            "endpoint":'docs',
            "route":'/docs.json',
        }
    ],
    "static_url_path":"/flasgger_static",
    "swagger_ui":True,
    "specs_route":"/docs/"
}
swagger = Swagger(app, template=swagger_template, config=swagger_config)

def connect_to_db():
    conn = sqlite3.connect('datas/challanger.db')
    conn.row_factory = sqlite3.Row
    return

def remove_punct(s):
    return re.sub(r"[^\w\d\s]+", "",s)

def replace_ascii(s):
    return unidecode

def remove_ascii2(s):
    return re.sub(r"\\x[A-Za-z0-9./]+","", unidecode(s))

def remove_byte(s):
    return bytes(s, 'utf-8').decode('utf-8', 'ignore')

def remove_newlines(s):
    return re.sub(r'\n', ' ',s)

def remove_morespace(s):
    return re.sub('  +', '',s)

def remove_newlines_text(s):
    return re.sub(r'\n.{0}', ' ', s)

@swag_from('docs/config_post.yml', methods=['POST'])
@app.route('/', methods=['POST'])
def remove_punct_poct():
    s = request.get_json(force=True)

    print(s['text'])
    result=remove_byte(s['text'])
    result=remove_punct(result)
    conn = sqlite3.connect('datas/challanger.db')
    conn.commit()
    conn.close()
    return jsonify({'Cleaned Text':result})

@swag_from('docs/config_file.yml', methods=['POST'])
@app.route("/get-text", methods=['GET'])
def get_text():
    Text_input = request.args.get('TextInput')
    get_text = {
        "text":f"hasil bersih{Text_input}"
    }
   
    return jsonify(get_text)

@swag_from('docs/config_form.yml', methods=['POST'])
@app.route("/upload-file", methods=['POST'])
def upload_file():
    file = request.files["file"]
    df = pd.read_csv(file, encoding='ISO-8859-1')
    df['CleanedTweet'] = df['Tweet'].apply(remove_ascii2)
    df['CleanedTweet1'] = df['CleanedTweet'].apply(remove_byte)
    df.drop(df.columns[13], axis=1, inplace=True)
    df['CleanedTweet2'] = df['CleanedTweet1'].apply(remove_newlines)
    df.drop(df.columns[13], axis=1, inplace=True)
    df['CleanedTweet3'] = df['CleanedTweet2'].apply(remove_newlines_text)
    df.drop(df.columns[13], axis=1, inplace=True)
    df['CleanedTweet4'] = df['CleanedTweet3'].apply(remove_punct)
    df.drop(df.columns[13], axis=1, inplace=True)
    df['CleanedTweet'] = df['CleanedTweet4'].apply(remove_morespace)
    df.drop(df.columns[13], axis=1, inplace=True)
    conn = sqlite3.connect("datas/challenge.db")
    df.to_sql('Challenge_Data', con=conn, index=False, if_exists='append')
    df.to_csv("clean_data.csv", sep = ";")
    conn.close()
    return jsonify({
        "text":"File berhasil diupload!!!"
    })

if __name__ == '__main__':
    app.run()