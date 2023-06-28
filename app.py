from flask import Flask, render_template, request, redirect, url_for, session, flash

from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'clothing_store'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM login")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', data=data)

@app.route('/index', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO login (email, password) VALUES (%s, %s)", (email, password))
    mysql.connection.commit()
    cur.close()

    return "Registration successful"

@app.route('/products')
def products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, price, image FROM products")
    products = cur.fetchall()
    cur.close()

    return render_template('products.html', products=products)

@app.route('/upload', methods=['POST'])
def upload():
    name = request.form['name']
    price = request.form['price']
    image = request.files['image'].read()

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO products (name, price, image) VALUES (%s, %s, %s)", (name, price, image))
    mysql.connection.commit()
    cur.close()

    return "Upload successful"

if __name__ == '__main__':
    app.run()
