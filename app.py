from flask import Flask,redirect,url_for,render_template,request
from pymongo import MongoClient
from bson import ObjectId
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def dashboard():
    fruit = list(db.fruit.find({}))
    return render_template('dashboard.html', fruit=fruit)

@app.route('/index',methods=['GET','POST'])
def index():
    fruit = list(db.fruit.find({}))
    return render_template('index.html', fruit=fruit)

@app.route('/addfruit',methods=['GET','POST'])
def addfruit():
    if request.method == 'POST' :
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        nama_gambar = request.files['gambar']

        if nama_gambar :
            nama_file_asli = nama_gambar.filename
            nama_file_gambar = nama_file_asli.split('.')[-1]
            file_path = f'static/assets/imgfruit/{nama_file_gambar}'
            nama_gambar.save(file_path)
        else :
            nama_gambar = None

        doc = {
            'nama' : nama,
            'harga' : harga,
            'deskripsi' : deskripsi,
            'foto' : nama_file_gambar
        }

        db.fruit.insert_one(doc)
        return redirect(url_for('index'))
    return render_template('AddFruit.html')

@app.route('/edit/<_id>',methods=['GET','POST'])
def edit(_id):
    if request.method == 'POST' :
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        nama_gambar = request.files['gambar']
        doc = {
            'nama' : nama,
            'harga' : harga,
            'deskripsi' : deskripsi,
        }

        if nama_gambar :
            nama_file_asli = nama_gambar.filename
            nama_file_gambar = nama_file_asli.split('.')[-1]
            file_path = f'static/assets/imgfruit/{nama_file_gambar}'
            nama_gambar.save(file_path)
            doc['foto'] = nama_file_gambar

        db.fruit.update_one({'_id': ObjectId(_id)}, {'$set': doc})
        return redirect(url_for("index"))

    id = ObjectId(_id)
    data = db.fruit.find({'_id':id})
    return render_template('EditFruit.html',data=data)

@app.route('/delete/<_id>',methods=['GET','POST'])
def delete(_id):
    db.fruit.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)