from flask import Flask, render_template, request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random 


'''

Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)



class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random",methods=["GET"])
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe={
    "id": random_cafe.id,
    "name": random_cafe.name,
    "map_url": random_cafe.map_url,
    "img_url": random_cafe.img_url,
    "location": random_cafe.location,
    "seats": random_cafe.seats,
    "has_toilet": random_cafe.has_toilet,
     "has_wifi": random_cafe.has_wifi,
    "has_sockets": random_cafe.has_sockets,
    "can_take_calls": random_cafe.can_take_calls,
    "coffee_price": random_cafe.coffee_price,
    })


@app.route("/all",methods=["GET"])
def get_all_cafes():
    cafes = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = cafes.scalars().all()
    cafe_list = []
    for cafe in all_cafes:
        cafe_json = {
            "id": cafe.id,
            "name": cafe.name,
            "map_url": cafe.map_url,
            "img_url": cafe.img_url,
            "location": cafe.location,
            "has_sockets": cafe.has_sockets,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "can_take_calls": cafe.can_take_calls,
            "seats": cafe.seats,
            "coffee_price": cafe.coffee_price,
        }
        cafe_list.append(cafe_json)
    return jsonify(cafes=cafe_list)
    
@app.route("/search", methods=["GET"])
def cafes_location():
    query_location = request.args.get("loc")
    cafe = db.session.execute(db.select(Cafe).where(Cafe.location==query_location))
    cafes = cafe.scalars().all()

    list_of_cafes = []
    if cafes:
        for cafe in cafes:
            cafe_in_json={
            "name": cafe.name,
            "map_url": cafe.map_url,
            "img_url": cafe.img_url,
            "location": cafe.location,
            "seats": cafe.seats,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "has_sockets": cafe.has_sockets,
            "can_take_calls": cafe.can_take_calls,
            "coffee_price": cafe.coffee_price
            }
            list_of_cafes.append(cafe_in_json)
        return jsonify(list_of_cafes)

    else:
        return jsonify({
            "error": {
            "Not Found": "Sorry we don't have a cafe at that location."
            }
            })
        
    
                                  
    

# HTTP POST - Create Record
@app.route("/add", methods = ["POST"])
def add_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),


    )
    # db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
