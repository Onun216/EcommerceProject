from flask import request, flash, redirect, url_for, render_template, session

from infortech import app, db, search
from infortech.products.models import Product, Supplier, Category
from infortech.products.forms import RegisterProduct, RegisterSupplier, AddCategory

import secrets


@app.route('/register-supplier', methods=['GET', 'POST'])
def register_supplier():
    if 'username' not in session:
        flash(f'Login necessário para continuar', 'danger')
        return redirect(url_for('login_admin'))

    form = RegisterSupplier(request.form)
    if request.method == 'POST':
        name = form.name.data
        email = form.email.data
        address = form.address.data
        NIF = form.NIF.data

        reg_sup = Supplier(name=name, email=email, address=address, NIF=NIF)
        db.session.add(reg_sup)
        flash(f'O fornecedor {name} foi registado com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('register_supplier'))
    return render_template('products/register_supplier.html', form=form)


@app.route('/edit-supplier/<int:id>', methods=['GET', 'POST'])
def edit_supplier(id):
    if 'username' not in session:
        flash(f'Login necessário para continuar', 'danger')
        return redirect(url_for('login_admin'))

    form = RegisterSupplier(request.form)
    supplier = Supplier.query.get_or_404(id)

    if request.method == 'POST':
        supplier.name = form.name.data
        supplier.email = form.email.data
        supplier.address = form.address.data
        supplier.NIF = form.NIF.data

        flash(f'O fornecedor foi editado com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('view_suppliers'))

    form.name.data = supplier.name
    form.email.data = supplier.email
    form.address.data = supplier.address
    form.NIF.data = supplier.NIF

    return render_template('products/edit_supplier.html', form=form, supplier=supplier)


@app.route('/add-category', methods=['GET', 'POST'])
def addCategory():
    if 'username' not in session:
        flash(f'Login necessário para continuar', 'danger')
        return redirect(url_for('login_admin'))

    form = AddCategory(request.form)
    if request.method == 'POST':
        new_category = form.name.data

        category = Category(name=new_category)
        db.session.add(category)
        flash(f'A categoria {new_category} foi adicionada com sucesso à base de dados.', 'success')
        db.session.commit()
        return redirect(url_for('addCategory'))
    return render_template('products/add_category.html', form=form)


@app.route('/register-product', methods=['GET', 'POST'])
def register_product():
    if 'username' not in session:
        flash(f'Login necessário para continuar', 'danger')
        return redirect(url_for('login_admin'))

    suppliers = Supplier.query.all()
    categories = Category.query.all()
    form = RegisterProduct(request.form)
    if request.method == 'POST':
        name = form.name.data
        max_stock = form.max_stock.data
        stock = form.stock.data
        sector = form.sector.data
        supplier_discount = form.supplier_discount.data
        base_price = form.base_price.data
        product_IVA = form.product_IVA.data
        total_order = form.total_order.data

        supplier = request.form.get('supplier')
        category = request.form.get('category')

        reg_prod = Product(name=name, max_stock=max_stock,
                           stock=stock, sector=sector,
                           supplier_discount=supplier_discount,
                           base_price=base_price, product_IVA=product_IVA, total_order=total_order,
                           supplier_id=supplier, category_id=category)
        db.session.add(reg_prod)
        flash(f'O producto {name} foi registado com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('register_product'))
    return render_template('products/register_product.html', form=form, suppliers=suppliers, categories=categories)


low_stock = (Product.max_stock - (Product.max_stock * 0.9))


@app.route('/warehouse-result')
def warehouse_result():
    try:
        searchword = request.args.get('q')
        products = Product.query.msearch(searchword, fields=['name'], limit=6)
        return render_template('products/search_warehouse.html', products=products)
    except Exception as e:
        print(e)
    return render_template('admin/home.html')


@app.route('/warehouse')
def warehouse():
    if 'username' not in session:
        flash(f'Login necessário para continuar', 'danger')
        return redirect(url_for('login_admin'))

    products = Product.query.order_by(Product.sector)
    suppliers = Supplier.query.all()
    categories = Category.query.all()

    return render_template('products/warehouse.html', products=products, suppliers=suppliers, categories=categories)


@app.route('/add-stock', methods=['POST'])
def add():
    product_alerts = Product.query.filter(Product.stock <= low_stock)
    if request.method == 'POST':
        try:
            for product in product_alerts:
                quantity = request.form.get('quantity')
                updated_prod = Product.query.filter_by(id=product.id).first().addToStock(quantity=int(quantity))
                return redirect(url_for('warehouse'))
        except Exception as e:
            print(e)
        finally:
            return redirect(url_for('warehouse'))

    return redirect(url_for('warehouse'))


@app.route('/edit-product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    if 'username' not in session:
        flash(f'Login necessário para continuar', 'danger')
        return redirect(url_for('login_admin'))

    form = RegisterProduct(request.form)
    product = Product.query.get_or_404(id)
    suppliers = Supplier.query.all()
    categories = Category.query.all()
    category = request.form.get('category')
    supplier = request.form.get('supplier')

    if request.method == 'POST':
        product.name = form.name.data
        product.max_stock = form.max_stock.data
        product.stock = form.stock.data
        product.sector = form.sector.data
        product.supplier_discount = form.supplier_discount.data
        product.base_price = form.base_price.data
        product.product_IVA = form.product_IVA.data
        product.total_order = form.total_order.data

        flash(f'O produto foi editado com sucesso', 'success')
        db.session.commit()
        return redirect(url_for('warehouse'))

    form.name.data = product.name
    form.max_stock.data = product.max_stock
    form.stock.data = product.stock
    form.sector.data = product.sector
    form.supplier_discount.data = product.supplier_discount
    form.base_price.data = product.base_price
    form.product_IVA.data = product.product_IVA
    form.total_order.data = product.total_order
    category = product.category.name

    return render_template('products/edit_product.html', form=form, suppliers=suppliers,
                           categories=categories, product=product)
