import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import row_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_ASCII'] = False
db: SQLAlchemy = SQLAlchemy(app)

class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    orders = db.relationship('Order', foreign_keys=[order_id])
    executors = db.relationship('User', foreign_keys=[executor_id])

    def to_dict(self):
        return {
        "id": self.id,
        "order_id": self.order_id,
        "executor_id": self.executor_id}

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

    customers = db.relationship('User', foreign_keys=[customer_id])
    executors = db.relationship('User', foreign_keys=[executor_id])

    def to_dict(self):
        return {
        "id": self.id,
        "name": self.name,
        "description": self.description,
        "start_date": self.start_date,
        "end_date": self.end_date,
        "address": self.address,
        "price": self.price,
        "customer_id": self.customer_id,
        "executor_id": self.executor_id}


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def to_dict(self):
        return {
        "id": self.id,
        "first_name": self.first_name,
        "last_name": self.last_name,
        "age": self.age,
        "email": self.email,
        "role": self.role,
        "phone": self.phone}

db.create_all()

for user_data in row_data.users:
    new_user = User(
    id=user_data["id"],
    first_name=user_data["first_name"],
    last_name=user_data["last_name"],
    age=user_data["age"],
    email=user_data["email"],
    role=user_data["role"],
    phone=user_data["phone"]
    )

    db.session.add(new_user)
    db.session.commit()


for order_data in row_data.orders:
    new_order = Order(
    name=order_data["name"],
    description=order_data["description"],
    start_date=order_data["start_date"],
    end_date=order_data["end_date"],
    address=order_data["address"],
    price=order_data["price"],
    customer_id=order_data["customer_id"],
    executor_id=order_data["executor_id"]
    )

    db.session.add(new_order)
    db.session.commit()


for offer_data in row_data.offers:
    new_offer = Offer(
    id=offer_data["id"],
    order_id=offer_data["order_id"],
    executor_id=offer_data["executor_id"]
    )

    db.session.add(new_offer)
    db.session.commit()


@app.route("/users", methods=["POST", "GET"])
def get_all_users():
    if request.method == "GET":
        result = []
        for u in User.query.all():
            result.append(u.to_dict())
        return jsonify(result), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "POST":
        user_data = json.load(request.data)
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"]
        )
        db.session.add(new_user)
        db.session.commit()
        return "", 201

@app.route("/users/<int:uid>", methods=['GET', 'PUT', 'DELETE'])
def users(uid: int):
    if request.method == "GET":
        return jsonify(User.query.get(uid).to_dict())
    elif request.method == "DELETE":
        u = User.query.get(uid)
        db.session.delete(u)
        db.session.commit()
        return "", 204
    elif request.method == "PUT":
        user_data = json.loads(request.data)
        u = User.query.get(uid)
        u.id=user_data["id"],
        u.first_name=user_data["first_name"],
        u.last_name=user_data["last_name"],
        u.age=user_data["age"],
        u.email=user_data["email"],
        u.role=user_data["role"],
        u.phone=user_data["phone"]

        db.session.add(u)
        db.session.commit()
        return "", 204

@app.route("/orders", methods=["POST", "GET"])
def get_all_orders():
    if request.method == "GET":
        result = []
        for ord in Order.query.all():
            result.append(ord.to_dict())
        return jsonify(result), 200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "POST":
        new_order = Order(
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            address=order_data["address"],
            price=order_data["price"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"]
        )
        db.session.add(new_order)
        db.session.commit()
        return "", 201


@app.route("/orders/<int:uid>", methods=['GET', 'PUT', 'DELETE'])
def orders(uid: int):
    if request.method == "GET":
        return jsonify(Order.query.get(uid).to_dict())
    elif request.method == "DELETE":
        ord = Order.query.get(uid)
        db.session.delete(ord)
        db.session.commit()
        return "", 204
    elif request.method == "PUT":
        order_data = json.loads(request.data)
        ord = Order.query.get(uid)
        ord.name = order_data["name"],
        ord.description = order_data["description"],
        ord.start_date = order_data["start_date"],
        ord.end_date = order_data["end_date"],
        ord.address = order_data["address"],
        ord.price = order_data["price"],
        ord.customer_id = order_data["customer_id"],
        ord.executor_id = order_data["executor_id"]
        db.session.add(ord)
        db.session.commit()
        return "", 204

@app.route("/offers", methods=["POST", "GET"])
def get_all_offers():
    if request.method == "GET":
        result = []
        for off in Offer.query.all():
            result.append(off.to_dict())
        return jsonify(result),  200, {'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "POST":
        new_offer = Offer(
            id=offer_data["id"],
            order_id=offer_data["order_id"],
            executor_id=offer_data["executor_id"]
        )

        db.session.add(new_offer)
        db.session.commit()
        return "", 201

@app.route("/offers/<int:uid>", methods=['GET', 'PUT', 'DELETE'])
def offers(uid: int):
    if request.method == "GET":
        return jsonify(Offer.query.get(uid).to_dict())
    elif request.method == "DELETE":
        off = Order.query.get(uid)
        db.session.delete(off)
        db.session.commit()
        return "", 204
    elif request.method == "PUT":
        offer_data = json.loads(request.data)
        off = Offer.query.get(uid)
        off.id = offer_data["id"],
        off.order_id = offer_data["order_id"],
        off.executor_id = offer_data["executor_id"]
        db.session.add(ord)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run()
