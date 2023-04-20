from app import app
from models import db, Cupcake

db.drop_all()
db.create_all()

c1 = Cupcake(
    flavor="cherry",
    size="large",
    rating=5,
)
c2 = Cupcake(
    flavor="vanilla",
    size="small",
    rating=5,
)
c3 = Cupcake(
    flavor="berry berry",
    size="large",
    rating=5,
)

c4 = Cupcake(
    flavor="chocolate",
    size="small",
    rating=9,
    image="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
)


db.session.add_all([c1, c2, c3, c4])
db.session.commit()