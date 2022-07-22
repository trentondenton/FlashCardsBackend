from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
cors = CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(100), unique=False)
    back = db.Column(db.String(144), unique=False)

    def __init__(self, front, back):
        self.front = front
        self.back = back


class CardSchema(ma.Schema):
    class Meta:
        fields = ('front', 'back')


card_schema = CardSchema()
cards_schema = CardSchema(many=True)

# Endpoint to Create a New Card
@app.route('/card', methods=['POST'])
def add_card():
    front = request.json['front']
    back = request.json['back']
    new_card = Card(front, back)

    db.session.add(new_card)
    db.session.commit()

    card = Card.query.get(new_card.id)
    return card_schema.jsonify(card)

# Endpoint to query all cards
@app.route('/cards', methods=['GET'])
def get_cards():
    all_cards = Card.query.all()
    result = cards_schema.dump(all_cards)
    return jsonify(result)

# Endpoint to query one card
@app.route('/card/<id>', methods=['GET'])
def get_card(id):
    card = Card.query.get(id)
    return card_schema.jsonify(card)

# Endpoint to update a card
@app.route('/card/<id>', methods=['PUT'])
def update_card(id):
    card = Card.query.get(id)
    front = request.json['front']
    back = request.json['back']

    card.front = front
    card.back = back

    db.session.commit()
    return card_schema.jsonify(card)

# Endpoint to delete a card
@app.route('/card/<id>', methods=['DELETE'])
def delete_card(id):
    card = Card.query.get(id)
    db.session.delete(card)
    db.session.commit()

    return 'Card was successfully deleted!'


if __name__ == '__main__':
    app.run(debug=True)





