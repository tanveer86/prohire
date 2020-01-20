from flask import Flask, json, jsonify, request, make_response
import csv
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask_cors import CORS
import math

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/prohire"
mongo = PyMongo(app)

# this function is for reading cars data from csv file and adding to mongodb
@app.route("/addcars")
def adding_speakers():
    with open("cars.csv", encoding="ISO-8859-1") as csv_list:
        car_list = csv.DictReader(csv_list)
        for each_line in car_list:
            mongo.db.cars.insert_one(
                {
                    "manufacturer": each_line["manufacturer"],
                    "name": each_line["name"],
                    "description": each_line["description"],
                    "color": each_line["color"],
                    "fueltype": each_line["fueltype"],
                    "mileage": each_line["mileage"],
                    "seatingcapacity": each_line["seatingcapacity"],
                    "image": each_line["image"],
                    "image2": each_line["image2"],
                    "image3": each_line["image3"],
                    "price": each_line["price"]
                })
    return dumps({"states": "sucess"})

@app.route("/listcars")
def list_cars():
    all_cars = mongo.db.cars.find()
    return dumps(all_cars)

@app.route("/car/<car_id>")
def car_detail(car_id):
    car_data = mongo.db.cars.find_one({"_id": ObjectId(car_id)})
    return dumps(car_data)

@app.route('/booking/create', methods=["POST"])
def create():
    carbook = {}
    carbook['customerName'] = request.json['customerName']
    carbook['customerEmail'] = request.json['customerEmail']
    carbook['customerDrop'] = request.json['customerDrop']
    carbook['customerPhone'] = request.json['customerPhone']
    carbook['customerDL'] = request.json['customerDL']
    carbook['customerPay'] = request.json['customerPay']
    carbook['customerMessage'] = request.json['customerMessage']
    carbook['carId'] = request.json['carId']
    carbook['carName'] = request.json['carName']
    carbook['carImage'] = request.json['carImage']
    carbook['bookingFrom'] = request.json['bookingFrom']
    carbook['bookingTo'] = request.json['bookingTo']
    mongo.db.booking.insert_one(carbook)
    return dumps(carbook)