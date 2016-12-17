from flask import Flask, jsonify
from flask import Response
from flask import json
from flask import request
import redis
from _mysql_exceptions import IntegrityError, OperationalError
from model import Orders, db, CreateDB

app = Flask(__name__)
#CreateDB()
@app.route('/')
def index():
    return 'Hello world!\n'
    
@app.route('/v1/expenses', methods=['POST', 'GET'])
def expenses():
    CreateDB()
    try:
        if request.method == 'POST':
            jayson = request.get_json(force=True)
            name = jayson['name']
            email = jayson['email']
            category = jayson['category']
            description = jayson['description']
            link = jayson['link']
            estimated_costs = jayson['estimated_costs']
            submit_date = jayson['submit_date']
            order = Orders(name, email, category, description, link, estimated_costs, submit_date, 'PENDING','')
            try:
                db.session.add(order)
                db.session.flush
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({"Session message": e.message})

            jsonString = {"id": order.id,
                          "name": order.customerName,
                          "email": order.customerEmail,
                          "category": order.category,
                          "description": order.description,
                          "link": order.link,
                          "estimated_costs": order.estimatedCost,
                          "submit_date": order.submitDate,
                          "status": order.status,
                          "decision_date": ""}
            response = Response(response=json.dumps(jsonString), status=201, mimetype="application/json")
            return response
        else:

            orders = Orders.query.all()
            if None != orders:
                orders_dict = {}
                for order in orders:
                    orders_dict[order.id] = {
                        "id": order.id,
                        "name": order.customerName,
                        "email": order.customerEmail,
                        "category": order.category,
                        "description": order.description,
                        "link": order.link,
                        "estimated_costs": order.estimatedCost,
                        "submit_date": order.submitDate,
                        "status": order.status,
                        "decision_date": ""
                    }
                return json.dumps(orders_dict), 200
            else:
                return jsonify({"message": "No results found"}), 404
    except Exception as e:
        return jsonify({"message": e.message})


@app.route('/v1/expenses/<int:orderId>', methods=['GET', 'PUT', 'DELETE'])
def getExpenses(orderId):
    try:

        if request.method == 'PUT':
            order = Orders.query.filter_by(id=orderId).first()
            if None != order:
                jayson = request.get_json(force=True)

                if None != jayson["estimated_costs"]:
                    order.estimatedCost = jayson["estimated_costs"]
                db.session.flush
                db.session.commit()

                return "Accepted", 202
            else:
                jsonString = {"message": "No Results Found"}
                return jsonify(jsonString), 404

        elif request.method == 'GET':
            print orderId
            order = Orders.query.filter_by(id=orderId).first()
            if None != order:
                jsonString = {
                    "id": order.id,
                    "name": order.customerName,
                    "email": order.customerEmail,
                    "category": order.category,
                    "description": order.description,
                    "link": order.link,
                    "estimated_costs": order.estimatedCost,
                    "submit_date": order.submitDate,
                    "status": order.status,
                    "decision_date": ""}

                response = Response(response=json.dumps(jsonString), status=200, mimetype="application/json")
                return response

            else:
                jsonString = {"message": "No Results Found"}
                return jsonify(jsonString), 404

        elif request.method == 'DELETE':
            order = Orders.query.get(orderId)
            if None != order:
                db.session.delete(order)
                db.session.flush
                db.session.commit()
                return jsonify({"message": "Order " order " deleted"}), 204
            else:
                jsonString = {"message": "No Results Found"}
                return jsonify(jsonString), 404
    except Exception as e:
        return jsonify({"message": e.message})


@app.route('/createdb')
def createDatabase():
    HOSTNAME = 'localhost'
    database = CreateDB()
    return json.dumps({'status':True})

@app.route('/createtbl')
def createUserTable():
    try:
        db.create_all()
        return json.dumps({'status': True})
    except Exception as e:
        return jsonify({"message": e.message})

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
