import matplotlib
import numpy as np

from flask import render_template, session, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from matplotlib import pyplot as plt

from infortech import app, db, bcrypt
from infortech.admin.forms import RegistrationForm, LoginForm
from infortech.admin.models import Admin
from infortech.products.models import Product, Supplier
from infortech.users.models import User, UserOrder
from infortech.products.routes import low_stock

matplotlib.use('Agg')


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('admin/home.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    products = Product.query.all()

    if 'username' not in session:
        flash(f'Login necessário para continuar', 'danger')
        return redirect(url_for('login_admin'))

    return render_template('admin/admin_page.html', products=products)



#@app.route('/register-admin', methods=['GET', 'POST'])
#def register_admin():
    #form = RegistrationForm(request.form)
    #if request.method == 'POST' and form.validate():
        #hash_password = bcrypt.generate_password_hash(form.password.data)
        #user_admin = Admin(username=form.username.data,
                           #password=hash_password)
        #db.session.add(user_admin)
        #db.session.commit()
        #flash('Admin registado com sucesso', 'success')
        #return redirect(url_for('home'))
    #return render_template('admin/register.html', form=form)


@app.route('/login-admin', methods=['GET', 'POST'])
def login_admin():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user_admin = Admin.query.filter_by(username=form.username.data).first()
        if user_admin and bcrypt.check_password_hash(user_admin.password, form.password.data):
            session['username'] = form.username.data
            flash(f'Benvindo {form.username.data}', 'success')
            return redirect(request.args.get('next') or url_for('admin_page'))
        else:
            flash('Password incorrecta! Tente novamente.', 'danger')

    return render_template('admin/login_admin.html', form=form)


@app.route('/view-users', methods=['GET', 'POST'])
def view_users():
    if 'username' not in session:
        flash(f'Login necessário para continuar', 'danger')
        return redirect(url_for('login_admin'))

    users = User.query.order_by(User.name).all()
    return render_template('admin/view_users.html', users=users)


@app.route('/view-suppliers', methods=['GET', 'POST'])
def view_suppliers():
    if 'username' not in session:
        flash(f'Login necessário para continuar', 'danger')
        return redirect(url_for('login_admin'))

    suppliers = Supplier.query.order_by(Supplier.name).all()
    return render_template('admin/view_suppliers.html', suppliers=suppliers)


@app.route('/view-orders/<int:id>', methods=['GET', 'POST'])
def view_orders(id):
    if 'username' not in session:
        flash(f'Login necessário para continuar', 'danger')
        return redirect(url_for('login_admin'))

    products = Product.query.all()
    user = User.query.filter_by(id=id)
    orders = UserOrder.query.filter_by(customer_id=id)

    return render_template('admin/view_orders.html', user=user, orders=orders, products=products)


@app.route('/user-result')
def users_result():
    if 'username' not in session:
        flash(f'Login necessário para continuar', 'danger')
        return redirect(url_for('login_admin'))

    searchword = request.args.get('q')
    users = User.query.msearch(searchword, fields=['name'], limit=6)
    return render_template('admin/search_users.html', users=users)


@app.route('/supplier-result')
def suppliers_result():
    if 'username' not in session:
        flash(f'Login necessário para continuar', 'danger')
        return redirect(url_for('login_admin'))

    searchword = request.args.get('q')
    suppliers = Supplier.query.msearch(searchword, fields=['name'], limit=6)
    return render_template('admin/search_suppliers.html', suppliers=suppliers)


@app.route('/sales-graphs', methods=['GET', 'POST'])
def sales_graphs():
    if 'username' not in session:
        flash(f'Login necessário para continuar', 'danger')
        return redirect(url_for('login_admin'))

    suppliers = Supplier.query.all()
    products = Product.query.all()
    return render_template('admin/view_sales.html', suppliers=suppliers, products=products)


@app.route('/graph/<int:id>', methods=['GET', 'POST'])
def graph(id):
    if 'username' not in session:
        flash(f'Login necessário para continuar', 'danger')
        return redirect(url_for('login_admin'))

    supplier = Supplier.query.filter_by(id=id).first()
    products = Product.query.filter_by(supplier_id=supplier.id)

    species = ([product.name for product in products])
    details = {
        'Vendas a clientes': ([int((product.total_order - product.stock)) for product in products]),
        'Encomendas': ([product.total_order for product in products])
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

    ax.set_facecolor(color="None")
    ax.set_ylabel('Total vendido (unidades)')
    ax.set_title('Vendas (detalhe)')
    ax.set_xticks(x + width, species)
    ax.legend(loc='upper left', ncols=2)

    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(15, 10, forward=True)
    plt.savefig('infortech/static/admin_graph.png')
    return render_template('admin/sale_graph.html', products=products, supplier=supplier,
                           plot_url="static/admin_sale_graph.png", x=x, species=species, details=details)


@app.route('/logout-admin')
def logout_admin():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('home'))
