from flask import Flask, jsonify, request
from pymongo import MongoClient
from extensions.extensions import mongo
from flask_cors import CORS

app = Flask (__name__)
app.config ['MONGO_URI'] = 'mongodb+srv://admin:123@cluster0.95hrdhh.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(app.config['MONGO_URI'])
db = client['itemFoodDb']
mongo.init_app(app)

CORS(app)

@app.route('/')
def index():
    return "hello"

if __name__ == "__main__":
    app.run(debug=True)

#Get metoda za dohvacanje svih proizvoda u cartu
@app.route('/app/cart', methods=['GET'])
def data():
    allData = db['cart'].find()
    dataJson = []
    for data in allData:
        id = data['_id']
        name = data['name']
        price = data['price']
        img = data['img']
        quantity = data['quantity']
        dataDict = {
            'id': str(id),
            'name': name,
            'price': price,
            'img': img,
            'quantity': quantity
        }
        dataJson.append(dataDict)
    return jsonify(dataJson)

#Post metoda za dodavanje prozivoda u cart
@app.route('/app/cart/dodaj', methods=['POST'])
def adddata():

        allData = db['cart'].find()
        body = request.get_json()
        print(body)
        id = body.get('_id')
        name = body.get('name')
        price = body.get('price')
        img = body.get('img')
        quantity = int(body.get('quantity'))
        category = body.get('category')
        flag = False

        for artikl in allData:
            print(artikl)
            if artikl['name'] == name:

                novaKolicina = int(artikl['quantity']) + 1
                db['cart'].delete_one({ "_id" : artikl['_id'] })
                db['cart'].insert_one({
                '_id': artikl['_id'],
                'name': name,
                'price': price,
                'img': img,
                'quantity': novaKolicina,
                'category': category
                })
                flag = True

                return jsonify({
                        'status': 'Data posted to MongoDB!',
                    })

        if flag == False:
            db['cart'].insert_one({
                        'name': name,
                        'price': price,
                        'img': img,
                        'quantity': quantity,
                        'category': category
                    })
            return jsonify({
                        'status': 'Data posted to MongoDB!',
                    })
        
        
#Post metoda za brisanje proizvoda u cart-u
@app.route('/app/cart/umanji', methods=['POST'])
def umanjiKolicinu():
    
        allData = db['cart'].find()
        body = request.get_json()
        print(body)
        id = body.get('id')
        name = body.get('name')
        price = body.get('price')
        img = body.get('img')
        quantity = int(body.get('quantity'))
        category = body.get('category')

        print(id)

        for artikl in allData:
            if artikl['name'] == name:
                if quantity == 1:
                    db['cart'].delete_one({ "_id" : artikl['_id'] })
                    return jsonify({
                                'status': 'Data posted to MongoDB!',
                            })
                else:
                    novaKolicina = int(artikl['quantity']) - 1
                    print(novaKolicina)
                    db['cart'].delete_one({ "_id" : artikl['_id'] })
                    db['cart'].insert_one({
                        '_id': artikl['_id'],
                        'name': name,
                        'price': price,
                        'img': img,
                        'quantity': novaKolicina,
                        'category': category
                        })

                    return jsonify({
                        'status': 'Data posted to MongoDB!',
                    })

#Get metoda za dohvacanje svih prozivoda
@app.route('/items', methods=['GET']) 
def data2():
    allData = db['itemFood'].find() 
    dataJson = []
    for data in allData:
        id = data['_id']
        name = data['name']
        price = data['price']
        img = data['img']
        quantity = data['quantity']
        category = data['category']
        dataDict = {       
            'id': str(id),
            'name': name,
            'price': price,
            'img': img,
            'quantity': quantity,
            'category': category
        }
        dataJson.append(dataDict) 
    print(dataJson)
    return jsonify(dataJson)