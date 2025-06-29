from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
db = SQLAlchemy(app)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/menu')
def menu():
    items = MenuItem.query.all()
    return render_template("menu.html", items=items)

@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form['name']
    price = request.form['price']
    new_item = MenuItem(name=name, price=float(price))
    db.session.add(new_item)
    db.session.commit()
    return redirect('/menu')

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        item_name = request.form['item']
        quantity = int(request.form['quantity'])
        order = Order(item_name=item_name, quantity=quantity)
        db.session.add(order)
        db.session.commit()
        return redirect('/order')
    orders = Order.query.all()
    return render_template("orders.html", orders=orders)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
