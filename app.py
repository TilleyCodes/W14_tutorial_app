from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="postgresql+psycopg2://ecommerce_dev:123456@localhost:5432/jul_ecommerce"

# creating instance app is the parameter
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Model - Table,  model is the class from sqlalchemy
class Product(db.Model):
    # define the tablename
    __tablename__ = "products"
    # define primary key
    id = db.Column(db.Integer, primary_key=True)
    # define more attributes
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)

#  Schema
class ProductSchema(ma.Schema):
    class Meta:
        # define the field to be serialised
        fields = ("id", "name", "description","price", "stock")

#  to handle multiple products
products_schema = ProductSchema(many=True)

#  to handle single product
product_schema = ProductSchema()

#  custom CLI commands to help create the tables
@app.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created")

@app.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped")

@app.cli.command('seed')
def seed_table():
    # create a product object
    product1 = Product(
        name="Product1",
        description="Product 1 description",
        price=12.99,
        stock=15
    )
    # another way to seed table
    product2 = Product()
    product2.name = "Product 2"
    product2.price = 149.99
    product2.stock = 25
    
    #add to session 
    db.session.add(product1)
    db.session.add(product2)
    # commit
    db.session.commit()
    print("Tables seeded")

# Get all products = /products - GET
# get a single product - /products/id - GET
# create a product - /products - POST
# update a product - /products/id - PUT or PATCH
#  delete a product - /products/id - DELETE

# CRUD for products
# Read - Get method, of CRUD
@app.route("/products")
def get_products():
    # stmt stand for statement
    stmt = db.select(Product) # SELECT * FROM products;
    products_list = db.session.scalars(stmt)
    data = products_schema.dump(products_list)
    return data

@app.route("/products/<int:product_id>")
def get_product(product_id):
    # delete a product - /products/id - DELETE# SELECT * FROM products WHERE id+product_id
    stmt = db.select(Product).filter_by(id=product_id)
    product = db.session.scalar(stmt)
    if product:
        data = product_schema.dump(product)
        return data
    else:
        return{"message": f"Product with id {product_id} does not exist"}, 404

# C of CRUD - CREATE - POST 
@app.route("/products", method=["POST"])
def create_product():
    body_data = request.get_json()
    new_product = Product(
    name=body_data.get("name"),
    description=body_data.get("descritpion"),
    price=body_data.get("price"),
    stock=body_data.get("stock")
    )
    db.session.add(new_product)
    db.session.commit()
    return product_schema.dump(new_product), 201

# delete a product - /products/id - DELETE
@app.route("/products/<int:products_id>", method=["DELETE"])
def delete_product(product_id):
    #  find the product with product id from db
    stmt = db.select(Product).where(Product.id==product_id)
    product = db.session.scalar(stmt)
    #  if product exits
    if product:
        #  delete the product
        db.session.delete(product)
        db.session.commit()
        #  repspond with messgae deleted
        return {"message": f"Product '{product.name}' deleted successfully"}
    #  else
    else:
        # repsond messgae with (f-string) that id does not exist
        return {"message": f"Product with id {product_id} does not exist"}, 404
