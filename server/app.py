'''server/app.py - main api app declaration'''
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os
import csv
from predictor.predictor import predict_users

'''Main wrapper for app creation'''
app = Flask(__name__, static_folder='../build')
CORS(app)


##
# API routes
##

@app.route('/api/users')
def items():
    print('get users data--------->>>>>>>>>>')
    users = []

    csv_path = os.path.join(os.path.dirname(__file__), 'predictor/data/test-bank.csv')
    # get part of test data
    # 60;"self-employed";"married";"primary";"no";362;"no";"yes";"cellular";29;"jul";816;6;-1;0;"unknown";"yes"
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            elif line_count < 16:
                users.append({
                    "age": int(row[0]),
                    "job": row[1],
                    "marital": row[2],
                    "education": row[3],
                    "default": row[4],
                    "balance": int(row[5]),
                    "housing": row[6],
                    "loan": row[7],
                    "contact": row[8],
                    "day": int(row[9]),
                    "month": row[10],
                    "duration": int(row[11]),
                    "campaign": int(row[12]),
                    "pdays": int(row[13]),
                    "previous": int(row[14]),
                    "poutcome": row[15],
                    "actual_subscription": row[16]
                })
                line_count += 1
            else:
                break

    return jsonify(users)


@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()

    users = predict_users(data)

    return jsonify(users)



##
# View route
##

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    '''Return index.html for all non-api routes'''
    # pylint: disable=unused-argument
    return send_from_directory(app.static_folder, 'index.html')
