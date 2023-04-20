from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)


# ? GET / RETURN HTML STATIC PAGE WITH EMPTY LIST FOR CUPCAKES AND FORM TO ADD CUPCAKE
@app.route("/")
def show_base():
    return render_template("base.html")

# ? GET api/cupcakes RETURN JSON LIST OF ALL CUPCAKES
@app.route("/api/cupcakes")
def show_all():
    """Return serialized JSON list of all Cupcakes"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

# ? GET api/cupcakes/<id> RETURN JSON SINGLE CUPCAKE
@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    """Return serialized JSON of a single cupcake"""
    cupcake = Cupcake.query.get_or_404(id)

    return jsonify(cupcake=cupcake.serialize())

# ? POST api/cupcakes CREATE NEW CUPCAKE 
@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Create a new cupcake, add to db and then return serialized JSON of a single cupcake"""
    #* CREATE CUPCAKE FROM JSON RECEIVED
    cupcake = Cupcake(
        flavor=request.json['flavor'],
        size=request.json['size'],
        rating= request.json['rating'],
        image= request.json['image']
    )
    # *ADD TO DB
    db.session.add(cupcake)
    db.session.commit()
    # *SERIALIZE JSON RESPONSE
    response_json = jsonify(cupcake = cupcake.serialize())
    # * RETURN RESPONSE, STATUS CODE TUPLE
    return (response_json, 201)

# ? PATCH api/cupcakes UPDATE EXISTING CUPCAKE, LEAVE NON PATCHED VARIABLES AS IS 
@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    """Create then update cupcake in db and return serialized JSON of cupcake"""
    # * CREATE
    cupcake = Cupcake.query.get_or_404(id)
    # * THEN UPDATE
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.image = request.json.get('image', cupcake.image)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    # * TO DB
    db.session.commit()
    # * SERIALIZE
    json_response = cupcake.serialize()
    # * JSON OF CUPCAKE
    return  jsonify(cupcake=json_response)

# ? DELETE api/cupcakes DELETE EXISTING CUPCAKE, RETURN MSG
@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    """Delete cupcake from db by ID and return JSON msg"""
    # * GET CUPCAKE BY ID
    cupcake = Cupcake.query.get_or_404(id)
    # * ADD FOR DELETE
    db.session.delete(cupcake)
    # * MAKE THE COMMITMENT
    db.session.commit()
    # * JSON MSG
    return  jsonify(message = "Deleted")


