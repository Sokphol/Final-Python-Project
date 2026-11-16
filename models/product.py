from extensions import db

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(500), nullable=True)
    stock = db.Column(db.Integer, nullable=False, default=10)
    status = db.Column(db.String(20), nullable=False, default='Active')
    rating = db.Column(db.Float, nullable=True, default=5.0)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('category.id'),
        nullable=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=True
    )

    category = db.relationship('Category', backref=db.backref('products', lazy=True))
    user = db.relationship('User', backref=db.backref('products', lazy=True))

    @property
    def is_in_stock(self):
        return self.stock > 0 and self.status == 'Active'
