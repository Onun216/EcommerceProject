from infortech import db

from datetime import datetime


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(80), nullable=False)
    max_stock = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    sector = db.Column(db.Integer, nullable=False)
    supplier_discount = db.Column(db.Integer, nullable=False)
    base_price = db.Column(db.Float, nullable=False)
    price_paid = db.Column(db.Float, nullable=False)
    product_IVA = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    total_order = db.Column(db.Integer, nullable=False)

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'),
                            nullable=False)
    supplier = db.relationship('Supplier',
                               backref=db.backref('products', lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)
    category = db.relationship('Category',
                               backref=db.backref('categories', lazy=True))

    def __init__(self, *args, **kwargs):
        kwargs['price_paid'] = ((float(kwargs['base_price']) - (float(kwargs['base_price'])
                                                                * (float(kwargs['supplier_discount']) / 100)))
                                * ((float(kwargs['product_IVA']) / 100) + 1))

        kwargs['price'] = float(kwargs['price_paid']) * ((float(kwargs['product_IVA']) / 100) + 1)

        super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<Product %r>' % self.name

    def update_stock(self, quantity):
        self.stock -= quantity
        db.session.commit()

    def addToStock(self, quantity):
        self.stock += quantity
        self.total_order += quantity
        db.session.commit()

    def grossProfit(self):
        result = self.price - self.price_paid
        gross_p = result * (self.total_order - self.stock)
        return gross_p


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    address = db.Column(db.String(200), nullable=False)
    NIF = db.Column(db.Integer, nullable=False, unique=True)

    def __repr__(self):
        return '<Supplier %r>' % self.name


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name
