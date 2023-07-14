import base64
import io

from io import BytesIO

from flask import render_template, request, redirect, session, flash, url_for, send_file

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from infortech import app, db, bcrypt
from infortech.suppliers.forms import SupplierAccountRegistrationForm, LoginForm
from infortech.suppliers.models import SupplierAccount

from infortech.products.models import Product, Supplier


@app.route('/supplier', methods=['GET', 'POST'])
def supplier_page():
    if 'username' not in session:
        flash(f'Faça login!', 'danger')
        return redirect(url_for('login_supplierAccount'))

    products = Product.query.all()

    return render_template('suppliers/supplier_page.html', products=products)


@app.route('/supplier-account', methods=['GET', 'POST'])
def register_supplierAccount():
    form = SupplierAccountRegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        supplier_account = SupplierAccount(username=form.username.data,
                                           password=hash_password)
        db.session.add(supplier_account)
        db.session.commit()
        flash('Conta registada com sucesso!', 'success')
        return redirect(url_for('login_supplierAccount'))
    return render_template('suppliers/register.html', form=form)


@app.route('/supplier-account-login', methods=['GET', 'POST'])
def login_supplierAccount():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        attempted_supplier = SupplierAccount.query.filter_by(username=form.username.data).first()
        if attempted_supplier and bcrypt.check_password_hash(attempted_supplier.password, form.password.data):
            session['username'] = form.username.data
            flash(f'Benvindo {form.username.data}', 'success')
            return redirect(request.args.get('next') or url_for('supplier_page'))
        else:
            flash('Password errada, tente novamente.', 'danger')

    return render_template('suppliers/login.html', form=form)


@app.route('/sales', methods=['GET'])
def view_sales():
    if 'username' not in session:
        flash(f'Faça login!', 'danger')
        return redirect(url_for('login_supplierAccount'))

    current_supplier = Supplier.query.filter_by(name=session['username']).first()
    products = Product.query.filter_by(supplier_id=current_supplier.id)

    x = [product.name for product in products]
    y = [product.total_order for product in products]

    fig, ax = plt.subplots()

    ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)
    plt.title('Vendas')
    plt.ylabel('Total vendido (unidades)')

    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(15, 10, forward=True)
    plt.savefig('infortech/static/sale_graph.png')
    return render_template('suppliers/sales.html', products=products, curret_supplier=current_supplier,
                           plot_url="static/sale_graph.png", x=x, y=y)


@app.route('/sales-detail', methods=['GET'])
def view_detail():
    if 'username' not in session:
        flash(f'Faça login!', 'danger')
        return redirect(url_for('login_supplierAccount'))

    current_supplier = Supplier.query.filter_by(name=session['username']).first()
    products = Product.query.filter_by(supplier_id=current_supplier.id)

    species = ([product.name for product in products])
    details = {
        'Vendas a clientes': ([int((product.total_order - product.stock)) for product in products]),
        'Vendas à InforTech': ([product.total_order for product in products])
    }

    x = np.arange(len(species))
    width = 0.25
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for detail, value in details.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, value, width, label=detail)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    ax.set_ylabel('Total vendido (unidades)')
    ax.set_title('Vendas (detalhe)')
    ax.set_xticks(x + width, species)
    ax.legend(loc='upper left', ncols=2)

    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(15, 10, forward=True)
    plt.savefig('infortech/static/detail_sale_graph.png')
    return render_template('suppliers/sales_detail.html', products=products, curret_supplier=current_supplier,
                           plot_url="static/detail_sale_graph.png", x=x, species=species, details=details)


@app.route('/logout-supplier')
def logout_supplier():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('home'))
