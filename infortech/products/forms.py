from wtforms import IntegerField, StringField, BooleanField, TextAreaField, Form, validators


class RegisterProduct(Form):
    name = StringField('Nome', [validators.DataRequired()])
    max_stock = IntegerField('Stock máximo', [validators.DataRequired()])
    stock = IntegerField('Stock disponível', [validators.DataRequired()])
    sector = IntegerField('Sector', [validators.DataRequired()])
    supplier_discount = IntegerField('Desconto', [validators.DataRequired()])
    base_price = IntegerField('Preço base', [validators.DataRequired()])
    product_IVA = IntegerField('IVA', [validators.DataRequired()])
    total_order = IntegerField('Pedido', [validators.DataRequired()])


class RegisterSupplier(Form):
    name = StringField('Nome', [validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=6, max=50), validators.Email()])
    address = StringField('Morada', [validators.DataRequired()])
    NIF = IntegerField('NIF', [validators.DataRequired()])


class AddCategory(Form):
    name = StringField('Categoria', [validators.DataRequired()])
