from flask import Flask, render_template, jsonify, Response
from pymongo import MongoClient
import gridfs
from bson import ObjectId
import os

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["Medicine"]
collection = db["Details"]
fs = gridfs.GridFS(db)

# Function to upload image and get image_id
def store_image_to_db(image_path):
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return None

    with open(image_path, "rb") as f:
        return fs.put(f, filename=os.path.basename(image_path))

# Products with image references to GridFS
products = [
    {
        "id": 1,
        "name": "Paracetamol Tablets IP 500 mg",
        "category": "painkillers",
        "price": 12,
        "image_path": "static/images/Picture4.png",
        "pack": "Pack of 15 Tablets"
    },
    {
        "id": 2,
        "name": "Ibuprofen Tablets 400 mg",
        "category": "painkillers",
        "price": 15,
        "image_path": "static/images/Picture5.jpg",
        "pack": "Pack of 10 Tablets"
    },
    {
        "id": 3,
        "name": "Amoxicillin Capsules 500 mg",
        "category": "antibiotics",
        "price": 18,
        "image_path": "static/images/Picture6.jpg",
        "pack": "Pack of 12 Capsules"
    },
    {
        "id": 4,
        "name": "Azithromycin Tablets 250 mg",
        "category": "antibiotics",
        "price": 60.0,
        "image_path": "static/images/Picture7.jpg",
        "pack": "Pack of 5 Tablets"
    },
    {
        "id": 5,
        "name": "Aspirin Tablets 75 mg",
        "category": "painkillers",
        "price": 8.0,
        "image_path": "static/images/Picture8.png",
        "pack": "Pack of 14 Tablets"
    },
    {
        "id": 6,
        "name": "Ciprofloxacin Tablets 500 mg",
        "category": "antibiotics",
        "price": 65.0,
        "image_path": "static/images/Picture9.png",
        "pack": "Pack of 10 Tablets"
    },
    {
        "id": 7,
        "name": "Digital Thermometer",
        "category": "equipment",
        "price": 250.0,
        "image_path": "static/images/Picture10.jpg",
        "pack": "1 Unit"
    },
    {
        "id": 8,
        "name": "Blood Pressure Monitor",
        "category": "equipment",
        "price": 1200.0,
        "image_path": "static/images/Picture11.jpg",
        "pack": "1 Unit"
    }
]

# Insert only if collection is empty
if collection.count_documents({}) == 0:
    for product in products:
        image_id = store_image_to_db(product["image_path"])
        if image_id:
            product["image_id"] = str(image_id)
        product.pop("image_path")  # remove image_path before insertion
        collection.insert_one(product)
    print("Products with images inserted successfully!")

# Home route
@app.route('/')
def home():
    return render_template('Find.html')

# Serve image by ID
@app.route('/image/<image_id>')
def get_image(image_id):
    try:
        image = fs.get(ObjectId(image_id))
        return Response(image.read(), mimetype='image/png')
    except:
        return "Image not found", 404

# API route to get products
@app.route('/api/products')
def get_products():
    products = []
    for product in collection.find():
        product['_id'] = str(product['_id'])  # Convert ObjectId to string
        if 'image_id' in product:
            product['image_url'] = f"/image/{product['image_id']}"
        products.append(product)
    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True)
