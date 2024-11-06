from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="postgresql+psycopg2://ecommerce_dev:123456@localhost:5432/jul_ecommerce"
# creating instance app is the parameter
db = SQLAlchemy(app)

# Model - Table,  model is the class from sqlalchemy
class Products(db.Model):
    # define the tablename
    __tablename__ = "products"
    # define primary key
    id = db.Column(db.Integer, primary_key=True)
    # define more attributes
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100))
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)

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
    product1 = Products(
        name="Product1",
        description="Product 1 description",
        price=12.99,
        stock=15
    )
    # another way to seed table
    product2 = Products()
    product2.name = "Product 2"
    product2.price = 149.99
    product2.stock = 25
    
    #add to session 
    db.session.add(product1)
    db.session.add(product2)
    # commit
    db.session.commit()
    print("Tables seeded")