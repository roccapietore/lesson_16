import json
import data
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/elenapolozova/PycharmProjects/hw16/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def make_user_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'email': self.email,
            'role': self.role,
            'phone': self.phone,
        }


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def make_offer_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'executor_id': self.executor_id,
        }


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    start_date = db.Column(db.String(100))
    end_date = db.Column(db.String(100))
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def make_order_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'address': self.address,
            'price': self.price,
            'customer_id': self.customer_id,
            'executor_id': self.executor_id
        }


db.drop_all()
db.create_all()

for order in data.orders:
    new_order = Order(
        id=order["id"],
        name=order["name"],
        description=order["description"],
        start_date=order["start_date"],
        end_date=order["end_date"],
        address=order["address"],
        price=order["price"],
        customer_id=order["customer_id"],
        executor_id=order["executor_id"]
    )

    db.session.add(new_order)
    db.session.commit()

for offer in data.offers:
    new_offer = Offer(
        id=offer["id"],
        order_id=offer["order_id"],
        executor_id=offer["executor_id"]
    )

    db.session.add(new_offer)
    db.session.commit()

for user in data.users:
    new_user = User(
        id=user["id"],
        first_name=user["first_name"],
        last_name=user["last_name"],
        age=user["age"],
        email=user["email"],
        role=user["role"],
        phone=user["phone"]
    )

    db.session.add(new_user)
    db.session.commit()


@app.route("/users", methods=["GET", "POST"])
def get_users():
    if request.method == "GET":
        response = []
        users = User.query.all()
        for user in users:
            response.append(user.make_user_dict())
        return json.dumps(response, ensure_ascii=False)

    elif request.method == "POST":
        req_json = request.json
        new_offer = Offer(**req_json)
        db.session.add(new_offer)
        db.session.commit()
        return "", 201

    return abort(404)


@app.route("/users/<id>",  methods=["GET", "PUT", "DELETE"])
def get_user_by_id(id: int):
    if request.method == "GET":
        user = db.session.query(User).get(id).make_user_dict()
        if not id:
            return abort(404)
        return json.dumps(user, ensure_ascii=False)

    elif request.method == "PUT":
        user = db.session.query(User).get(id)
        req_json = request.json
        user.id = req_json.get("id")
        user.first_name = req_json.get("first_name")
        user.last_name = req_json.get("last_name")
        user.age = req_json.get("age")
        user.email = req_json.get("email")
        user.role = req_json.get("role")
        user.phone = req_json.get("phone")
        db.session.add(user)
        db.session.commit()
        return "", 204

    elif request.method == "DELETE":
        user = db.session.query(User).get(id)
        db.session.delete(user)
        db.session.commit()
        return "", 201

    return abort(404)


@app.route("/orders", methods=["GET", "POST"])
def get_orders():
    if request.method == "GET":
        response = []
        orders = db.session.query(Order).all()
        for order in orders:
            response.append(order.make_order_dict())
        return json.dumps(response, ensure_ascii=False)
    elif request.method == "POST":
        req_json = request.json
        new_order = Order(**req_json)
        db.session.add(new_order)
        db.session.commit()
        return "", 201

    return abort(404)


@app.route("/orders/<id>", methods=["GET", "PUT", "DELETE"])
def get_order_by_id(id: int):
    if request.method == "GET":
        order = db.session.query(Order).get(id).make_order_dict()
        if not id:
            return abort(404)
        return json.dumps(order, ensure_ascii=False)
    elif request.method == "DELETE":
        order = db.session.query(Order).get(id)
        db.session.delete(order)
        db.session.commit()
        return "", 204

    return abort(404)


@app.route("/offers", methods=["GET", "POST"])
def get_offers():
    if request.method == "GET":
        response = []
        offers = db.session.query(Offer).all()
        for offer in offers:
            response.append(offer.make_offer_dict())
        return json.dumps(response, ensure_ascii=False)
    elif request.method == "POST":
        req_json = request.json
        new_offer = Offer(**req_json)
        db.session.add(new_offer)
        db.session.commit()
        return "", 201

    return abort(404)


@app.route("/offers/<id>", methods=["GET", "PUT", "DELETE"])
def get_offer_by_id(id: int):
    if request.method == "GET":
        offer = db.session.query(Offer).get(id).make_offer_dict()
        if not id:
            return abort(404)
        return json.dumps(offer, ensure_ascii=False)

    elif request.method == "PUT":
        offer = db.session.query(Offer).get(id)
        req_json = request.json
        offer.id = req_json.get("id")
        offer.order_id = req_json.get("order_id")
        offer.executor_id = req_json.get("executor_id")
        db.session.add(offer)
        db.session.commit()
        return "", 204

    elif request.method == "DELETE":
        offer = db.session.query(Offer).get(id)
        db.session.delete(offer)
        db.session.commit()
        return "", 204

    return abort(404)


if __name__ == "__main__":
    app.run(port=5009)
