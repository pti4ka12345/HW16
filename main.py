import json
import pprint

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import prettytable
import row_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db: SQLAlchemy = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order = db.relationship("Order")
    executor = db.relationship("User")


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    address = db.Column(db.String(200))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer = db.relationship("User")
    executor = db.relationship("User")


db.create_all()

with open('users_data.json', 'r', encoding='utf-8') as f:
    text = json.load(f)

for user_data in text:
    new_user = User(
    id=user_data["id"],
    first_name=user_data["first_name"],
    last_name=user_data["last_name"],
    age=user_data["age"],
    email=user_data["email"],
    role=user_data["role"],
    phone=user_data["phone"]
    )

pprint.pprint(new_user)
# with db.session.begin():
#     db.session.add_all(users)


# session = db.session()
# cursor_offer = session.execute("SELECT * from offer").cursor
# mytable = prettytable.from_db_cursor(cursor_offer)
# cursor_order = session.execute("SELECT * from order").cursor
# mytable1 = prettytable.from_db_cursor(cursor_order)
# cursor_user = session.execute("SELECT * from user").cursor
# mytable3 = prettytable.from_db_cursor(cursor_user)



# if __name__ == '__main__':
    # app.run()
    # print(mytable)