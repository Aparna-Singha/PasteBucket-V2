from flask import Flask , render_template
from pymongo.mongo_client import MongoClient
from flask import request
from flask import jsonify
import os

print("Starting server")

uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')

# Create a new client and connect to the server
client = MongoClient(uri)
print(client)

# Send a ping to confirm a successful connection
database = client["test"]
collection = database["test2"]
user_data = database["users"]

app = Flask(__name__)

# {
#     "_id": "data",
#     "value": {
#         "0": {
#             "id": 0,
#             "name": "John Doe",
#             "content": "Hello, World!"
#         },
#         "1": {
#             "id": 1,
#             "name": "Jane Doe",
#             "content": "Hello, World!"
#         }
#     }
# },
# {
#     "_id": "count",
#     "value": 2
# }




@app.route('/') #end points
def hello_world():
    return render_template('index.html')

@app.route('/')
def about():
    return 'This is the about page.'

@app.route('/sign-up', methods=['POST'])
def sign_up():
    data = request.json

    if 'username' not in data or 'password' not in data:
        return jsonify({
            'status': 400,
            'message': 'Invalid data'
        })

    if user_data.find_one({'username': data['username']}):
        return jsonify({
            'status': 409,
            'message': 'User already exists'
        })

    user_data.insert_one(data)
    return jsonify({
        'status': 200,
        'message': 'Registered successfully'
    })

@app.route('/sign-in', methods=['POST'])
def sign_in():
    data = request.json

    if 'username' not in data or 'password' not in data:
        return jsonify({
            'status': 400,
            'message': 'Invalid data'
        })

    user = user_data.find_one({
        'username': data['username']
    })

    if not user:
        return jsonify({
            'status': 404,
            'message': 'User not found'
        })
    
    if user['password'] != data['password']:
        return jsonify({
            'status': 401,
            'message': 'Invalid password'
        })
    
    return jsonify({
        'status': 200,
        'message': 'Logged in successfully'
    })

@app.route('/data', methods=['POST'])
def data_api():
    json = request.json

    username = json['username']
    data = json['data']
    count = json['count']

    if not username:
        return jsonify({
            'message': 'Invalid data'
        })

    if not collection.find_one({'_id': username}):
        collection.insert_one({
            '_id': username,
            'value': data,
            'count': count
        })
        
        print('Data saved successfully')
        return jsonify({'message': 'Data saved successfully'})
    
    collection.update_one(
        {'_id': username},
        {'$set': {
            'value': data,
            'count': count
        }}
    )
    
    print('Data saved successfully')
    return jsonify({'message': 'Data saved successfully'})

@app.route('/data/<username>', methods=['GET'])
def get_data(username):
    data = collection.find_one({'_id': username})
    if not data:
        return jsonify({
            'value': {},
            'count': 0
        })
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=3000
    )
