"""
Python
from email.message import EmailMessage

def order_quantity(prod):
    quantity = prod.max_stock - prod.stock
    return quantity


@app.route('/mail-to-supplier', methods=['POST'])
def mailToSupplier():
    product_alerts = Product.query.filter(Product.stock <= low_stock)
    if request.method == 'POST':
        # AttributeError
        try:
            for product in product_alerts:
                supplier_alert = Supplier.query.filter_by(id=product.supplier_id).first()
                #email = supplier_alert.email
                mail_supplier(product, order_quantity(product))
                #product.addToWarehouse(order_quantity(product))
                continue
                #return redirect(url_for('warehouse'))
        except AttributeError as e:
            print(e)
        finally:
            return redirect(url_for('warehouse'))

    return redirect(url_for('warehouse'))

@app.route('/complete-stock', methods=['POST'])
def complete_stock():
    product_alerts = Product.query.filter(Product.stock <= low_stock)
    if request.method == 'POST':
        # AttributeError
        try:
            for product in product_alerts:
                product.addToStock(order_quantity(product))
                return redirect(url_for('warehouse'))
        except AttributeError as e:
            print(e)
        finally:
            return redirect(url_for('warehouse'))

    return redirect(url_for('warehouse'))

"""

"""
<td> <a href="{{url_for('edit_users', id=user.id)}}" class="btn btn-outline-primary">Editar</a> </td>

HTML

<td>
    <form action="/complete-stock" method="post">
        <button class="btn btn-outline-primary">Actualizar</button>
    </form>
</td>

{% extends "layout.html" %}

{% block content %}

<div class="container text-center">

  <a href="/admin">
        <button type="button" class="btn btn-outline-primary">Voltar</button>
    </a>
    {% include '_messages.html' %}
    {% from "_formhelpers.html" import render_field %}
  <table class="table">
  <thead>
      <th scope="col">Produto</th>
      <th scope="col">Stock</th>
      <th scope="col">Sector</th>
      <th scope="col">Alerta</th>
      <th scope="col"></th>
  </thead>

  <tbody>
  {% for product in products %}
  {% if product.stock > 0 %}
  {% set low_stock = product.max_stock|int - (product.max_stock * 0.8)|int  %}
    <tr>
      <td>{{product.name}}</td>
      <td>{{product.stock}}</td>
      <td>{{product.sector}}</td>


      {% if product.stock <= low_stock %}
        <td>
      <form action="/mail-to-supplier" method="post">

          <button class="btn btn-primary">Enviar email</button>
      </form>
      </td>

        <td>
        <form action="/add-stock" method="post">
          <button class="btn btn-outline-primary">Actualizar stock</button>

        </form>

      </td>
         {% endif %}


    </tr>
  {% endif %}
  {% endfor %}
  </tbody>
</table>

</div>

{% endblock content %}
"""
