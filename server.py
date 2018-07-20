from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat6.db'


db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_posted = db.Column(db.DateTime)
    text = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='message')


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class MessageSchema(ma.ModelSchema):
    class Meta:
        model = Message


@app.route('/', methods=['GET', 'POST', 'DELETE'])
def hello_world():
    if request.method == 'POST':
        data = request.get_json()
        user = data['user']
        message = data['message']

        a = User.query.filter_by(user=user).all()

        if len(a) > 0:
            post2 = Message(text=message, user=a[0], day_posted=datetime.now())
            db.session.add(post2)
            db.session.commit()
        else:
            post1 = User(user=user)
            post2 = Message(text=message, user=post1, day_posted=datetime.now())
            db.session.add_all([post1, post2])
            db.session.commit()
    elif request.method == 'DELETE':
        db.drop_all()
        db.create_all()

    user = User.query.all()
    user_schema = UserSchema(many=True)
    user_out = user_schema.dump(user)

    message = Message.query.all()
    message_schema = MessageSchema(many=True)
    message_out = message_schema.dump(message)

    return jsonify({'user': user_out, 'messages': message_out})


if __name__ == '__main__':
    app.run(debug=True)
