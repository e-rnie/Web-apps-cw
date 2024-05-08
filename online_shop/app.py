from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_very_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    image = db.Column(db.String(100))
    environmental_impact = db.Column(db.Float)

@app.route('/')
def front_page():
    products = Product.query.all()
    return render_template("front_page.html", products=products)

@app.route('/product/<int:product_id>')
def single_product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("single_product.html", product=product)

@app.route('/add_to_basket/<int:product_id>')
def add_to_basket(product_id):
    product = Product.query.get(product_id)
    if product:
        if 'basket' not in session:
            session['basket'] = []
        else:
            # Even if the basket exists, we need to ensure Flask knows it's modified
            session.modified = True

        # Check if the product is already in the basket
        if not any(item['id'] == product.id for item in session['basket']):
            session['basket'].append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'description': product.description,
                'image': product.image,
                'environmental_impact': product.environmental_impact
            })
        return redirect(url_for('view_basket'))
    else:
        return "Product not found", 404

@app.route('/basket')
def view_basket():
    print(session.get('basket', 'Basket is empty'))  # Debug: print basket contents
    basket = session.get('basket', [])
    total_price = sum(item['price'] for item in basket)
    return render_template('basket.html',total_price=total_price, basket=session.get('basket', []))

@app.route('/remove_from_basket/<int:product_id>')
def remove_from_basket(product_id):
    if 'basket' in session:
        # We need to create a new list to ensure Flask sees this as a modification
        new_basket = [item for item in session['basket'] if item['id'] != int(product_id)]
        session['basket'] = new_basket
        session.modiied = True
    return redirect(url_for('view_basket'))


@app.route('/products')
def list_products():
    products = Product.query.all()
    return render_template('list_products.html', products=products)



@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/process_checkout', methods=['POST'])
def process_checkout():
    card_number = request.form.get('card_number')
    card_holder = request.form.get('card_holder')
    expiry_date = request.form.get('expiry_date')
    cvv = request.form.get('cvv')
    
    # Simple validation: Check if the card number is 16 digits
    if not (card_number.replace('-', '').replace(' ', '').isdigit() and len(card_number.replace('-', '').replace(' ', '')) == 16):
        flash('Invalid card number, please enter a 16-digit card number.')
        return redirect(url_for('checkout'))

    # Redirect to a success page or similar
    flash('Checkout successful. Thank you for your purchase!')
    return redirect(url_for('checkout_success'))

@app.route('/checkout_success')
def checkout_success():
    return render_template('checkout_success.html')

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.description = request.form['description']
        product.price = float(request.form['price'])
        db.session.commit()
        return redirect(url_for('front_page'))
    return render_template('edit_product.html', product=product)


if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0')
