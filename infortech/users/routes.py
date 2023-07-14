from flask import request, flash, render_template, session, url_for, redirect, make_response
from flask_login import login_user, logout_user, current_user, login_required

from infortech import app, db, bcrypt, login_manager, search
from infortech.users.forms import UserRegistrationForm, UserLoginForm
from infortech.users.models import User, UserOrder
from infortech.products.models import Product, Supplier, Category

import json
import os
import secrets
import pdfkit


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(name=form.name.data,
                        address=form.address.data,
                        NIF=form.NIF.data,
                        email=form.email.data,
                        password=hash_password)
        db.session.add(new_user)
        flash('Novo cliente criado com sucesso!', 'success')
        db.session.commit()
        return redirect(url_for('userLogin'))
    return render_template('users/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def userLogin():
    form = UserLoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email.data).first()
        if attempted_user and bcrypt.check_password_hash(attempted_user.password, form.password.data):
            login_user(attempted_user)
            # session['email'] = form.email.data
            flash(f'Login bem sucedido!', 'success')
            next = request.args.get('next')
            return redirect(next or url_for('store'))
        else:
            flash('Dados incorrectos! Tente novamente', 'danger')

    return render_template('users/login.html', form=form)


@app.route('/edit-user-account/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user_account(id):
    form = UserRegistrationForm()
    user = User.query.filter_by(id=current_user.id).first()

    if request.method == 'POST':
        user.name = form.name.data
        user.address = form.address.data
        user.NIF = form.NIF.data
        user.email = form.email.data

        flash(f'Dados actualizados com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('order_history', id=current_user.id))

    form.password.data = user.password

    return render_template('users/edit_user_account.html', form=form, user=user)


@app.route('/users/logout')
def user_logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/edit-user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    return render_template('users/edit_users.html')


@app.route('/view-store', methods=['GET', 'POST'])
def view_store():
    products = Product.query.filter(Product.stock > 0).order_by(Product.id)
    suppliers = Supplier.query.all()
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()

    return render_template('users/view_store.html', products=products, suppliers=suppliers, categories=categories)


@app.route('/view-store-category/<int:id>')
def get_category_for_view_store(id):
    category = Product.query.filter_by(category_id=id)

    return render_template('users/view_store.html', category=category)


@app.route('/view-store-result')
def view_store_result():
    searchword = request.args.get('q')
    products = Product.query.msearch(searchword, fields=['name'], limit=6)
    return render_template('users/view_store_search.html', products=products)


@app.route('/store', methods=['POST', 'GET'])
@login_required
def store():
    products = Product.query.filter(Product.stock > 0).order_by(Product.id)
    suppliers = Supplier.query.all()
    categories = Category.query.join(Product, (Category.id == Product.category_id)).all()

    return render_template('users/store.html', products=products, suppliers=suppliers, categories=categories)


@app.route('/category/<int:id>')
def get_category(id):
    category = Product.query.filter_by(category_id=id)

    return render_template('users/store.html', category=category)


@app.route('/store-result')
def store_result():
    searchword = request.args.get('q')
    products = Product.query.msearch(searchword, fields=['name'], limit=6)
    return render_template('users/search_store.html', products=products)


@app.route('/product/<int:id>')
def view_product(id):
    product = Product.query.get_or_404(id)
    return render_template('users/view_product.html', product=product)


@app.route('/get-order')
@login_required
def get_order():
    if current_user.is_authenticated:
        total = 0
        subTotal = 0

        # Chave do dict session['Shoppingcart'] é o id do produto cujo stock queremos actualizar
        for key, product in session['Shoppingcart'].items():
            subTotal += float(product['price']) * int(product['quantity'])
            total = float("%.2f" % subTotal)
            purchased_product = Product.query.filter_by(id=int(key)).first() \
                .update_stock(quantity=int(product['quantity']))

        customer_id = current_user.id
        order_NIF = current_user.NIF

        # Cria uma identificação com 10 caractéres para a factura
        invoice = secrets.token_hex(5)
        try:

            order = UserOrder(invoice=invoice, customer_id=customer_id, order_NIF=order_NIF,
                              orders=session['Shoppingcart'], order_total=total)
            db.session.add(order)
            flash(f'O seu pedido foi confirmado. Obrigado!', 'success')
            db.session.commit()
            session.pop('Shoppingcart')
            return redirect(url_for('orders', invoice=invoice))
        except Exception as e:
            print(e)
            flash(f'Ocorreu um erro ao processar o seu pedido. Tente novamente!', 'danger')
            return redirect(url_for('cart'))


@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        total = 0
        subTotal = 0
        IVA = 0
        customer_id = current_user.id
        customer = User.query.filter_by(id=customer_id).first()
        order_NIF = customer.NIF
        orders = UserOrder.query.filter_by(
            customer_id=customer_id).order_by(UserOrder.id.desc()).first()
        for key, product in orders.orders.items():
            subTotal += float(product['price']) * int(product['quantity'])
            total = float("%.2f" % subTotal)
            partial_iva = (float(product['price']) * (int(product['IVA']) / 100)) * int(product['quantity'])
            IVA += float("%.2f" % partial_iva)

    else:
        return redirect(url_for('userLogin'))
    return render_template('users/order.html', invoice=invoice, subTotal=subTotal,
                           total=total, customer=customer, order_NIf=order_NIF, orders=orders, IVA=IVA)


@app.route('/order-history/<int:id>', methods=['GET', 'POST'])
@login_required
def order_history(id):
    if current_user.is_authenticated:
        customer_id = current_user.id
        order_history = UserOrder.query.filter_by(customer_id=current_user.id)

        for order in order_history:
            subTotal = 0
            for key, product in order.orders.items():
                subTotal += float(product['price']) * int(product['quantity'])

        return render_template('users/order_history.html', order_history=order_history)


@app.route('/get_pdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        total = 0
        subTotal = 0
        IVA = 0
        customer_id = current_user.id

        if request.method == 'POST':
            customer = User.query.filter_by(id=customer_id).first()
            order_NIF = customer.NIF
            orders = UserOrder.query.filter_by(
                customer_id=customer_id).order_by(UserOrder.id.desc()).first()
            for key, product in orders.orders.items():
                subTotal += float(product['price']) * int(product['quantity'])
                total = float("%.2f" % subTotal)
                partial_iva = (float(product['price']) * (int(product['IVA']) / 100)) * int(product['quantity'])
                IVA += float("%.2f" % partial_iva)

            rendered = render_template('users/pdf.html', invoice=invoice,
                                       total=total, customer=customer, order_NIF=order_NIF, orders=orders, IVA=IVA)
            pdf = pdfkit.from_string(rendered, False)
            response = make_response(pdf)
            response.headers['content-Type'] = 'application/pdf'
            response.headers['content-Disposition'] = 'attached; inline: filename=' + invoice + '.pdf'
            return response
    return redirect(url_for('orders'))
