from flask import Flask, request, make_response, jsonify
#figure out how to use jsonify
from flask_cors import CORS
from flask_migrate import Migrate
import ipdb

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods =['GET', 'POST'])
def messages():
    if request.method == 'GET':
        all_messages = Message.query.all() 
        messages_dict = [message.to_dict() for message in all_messages]
        return make_response(messages_dict)      

    elif request.method == 'POST':
        params = request.json
        # ipdb.set_trace()
        new_message = Message(body=params['body'], username=params["username"])

        db.session.add(new_message)
        db.session.commit()

        return make_response(new_message.to_dict())

@app.route('/messages/<int:id>', methods =['PATCH'])
def messages_by_id(id):
    found_message = Message.query.get(id)
    params = request.json
    ipdb.set_trace()
    setattr(found_message, 'body', params['body'])
    return ''

if __name__ == '__main__':
    app.run(port=5555)
