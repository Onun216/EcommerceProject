from flask import request, session, redirect, render_template, url_for, flash
from infortech import app
from infortech.products.models import Product


def MergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@app.route('/add-to-cart', methods=['POST'])
def addToCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        product = Product.query.filter_by(id=product_id).first()
        if product_id and quantity and request.method == 'POST':
            DictItems = {product_id: {'name': product.name, 'price': float(product.price),
                                      'quantity': int(quantity), 'IVA': float(product.product_IVA)}}

            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    print('O produto já está no carrinho')
                else:
                    session['Shoppingcart'] = MergeDicts(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/view-cart')
def cart():

    if 'Shoppingcart' not in session:
        return redirect(url_for('store'))

    if len(session['Shoppingcart']) == 0:
        return redirect(url_for('store'))

    subtotal = 0
    order_total = 0
    for key, product_id in session['Shoppingcart'].items():
        subtotal += float(product_id['price']) * int(product_id['quantity'])
        order_total = float('%.2f' % subtotal)

    return render_template('users/cart.html', order_total=order_total, subtotal=subtotal)


@app.route('/update-cart/<int:code>', methods=['POST'])
def update_cart(code):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('store'))
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    flash('Item actualizado!')
                    return redirect(url_for('cart'))
        except Exception as e:
            print(e)
            return redirect(url_for('cart'))


@app.route('/delete-cart-item/<int:id>')
def delete_item(id):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('store'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            session['Shoppingcart'].pop(key, None)
            return redirect(url_for('cart'))
    except Exception as e:
        print(e)
        return redirect(url_for('cart'))
