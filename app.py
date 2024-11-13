# pylint: disable=trailing-whitespace,line-too-long,invalid-name,import-error
'''initializes the Flask application and defines the routes and functions for handling various requests'''
import os
import sqlite3
from flask import Flask, render_template,request, jsonify, send_from_directory
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()
api_key = os.getenv('PINECONE_API_KEY')

pc = Pinecone(api_key=api_key)
index_name = "furniture"
index = pc.Index(index_name)

model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

app = Flask(__name__,template_folder='templates',static_folder='static')

def get_db_connection():
    '''Establish connection to the SQLite database'''
    connection = sqlite3.connect('Products.db')
    connection.row_factory = sqlite3.Row
    return connection

global id_list 
id_list = []

@app.route('/')
def home():
    '''Rendering the home page'''
    return render_template('index.html')

@app.route('/catalog/<path:filename>')
def serve_catalog(filename):
    '''Serve a file from the 'catalog' directory'''
    return send_from_directory('catalog', filename)

@app.route("/api/ImageSearch", methods=['POST'])
def UploadImageFunction():
    '''For uploading images handeling'''
    file = request.files['file']
    print(file)
    file_path = "temp_uploaded_image.jpeg"
    file.save(file_path)

    img = image.load_img(file_path, target_size=(224, 224))  
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  
    img_array = preprocess_input(img_array)

    features = model.predict(img_array)
    embedding = features.flatten()
    print(embedding)
    
    response = index.query(
    namespace="ns1",
    vector=embedding.tolist(),
    top_k=5,
    include_values=False,
    include_metadata=True,
    )
    
    print(response['matches'])
    id_list = []
    for info in response['matches']:
        print(round(info['score'],2))
        
        if round(info['score'],2) >= 0.70: 
            id_list.append(info['id'])
            print(id_list)
            
    if id_list: 
        conn = get_db_connection()
        all_products = []
        for product_id in id_list:
            product = conn.execute('SELECT * FROM ProductDetails WHERE product_id = ?', (product_id,)).fetchone()
            all_products.append(product)
        conn.close()
            
        Furniture_name,Furniture_price,Furniture_type,Furniture_material,Furniture_color,Furniture_features,Furniture_url = [],[],[],[],[],[],[]
        furcount = 0
        for product in all_products:
            furcount += 1
            Furniture_name.append(product['name'])
            Furniture_price.append(product['price'])
            Furniture_type.append(product['type'])
            Furniture_material.append(product['material'])
            Furniture_color.append(product['color'])
            Furniture_features.append(product['features'])
            Furniture_url.append(product['image_url'])
        
        print(Furniture_name,Furniture_price,Furniture_type,Furniture_material,Furniture_color,Furniture_features,Furniture_url,sep='\n')
        
        return jsonify({
            'BackendResponse':"Image send to Backend",
            'FurName':Furniture_name,
            'FurPrice':Furniture_price,
            'FurType':Furniture_type,
            'FurMaterial':Furniture_material,
            'FurColor':Furniture_color,
            'FurFeatures':Furniture_features,
            'FurImage':Furniture_url,
            'FurCount':furcount})
        
    else:
        return jsonify({
            'BackendResponse': 0,
            'FurName': [],
            'FurPrice': [],
            'FurType': [],
            'FurMaterial': [],
            'FurColor': [],
            'FurFeatures': [],
            'FurImage': [],
            'FurCount': 0
        })
    
if __name__ == "__main__":
    app.run(debug=True)