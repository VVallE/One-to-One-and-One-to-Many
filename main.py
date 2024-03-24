from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ships.db"
db = SQLAlchemy(app)


class Ship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    sailors = db.relationship("Sailor", backref="ship", lazy=True)


class Sailor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ship_id = db.Column(db.Integer, db.ForeignKey("ship.id"))
    certificate = db.relationship("Certificate", uselist=False, back_populates="sailor")


class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    sailor_id = db.Column(db.Integer, db.ForeignKey("sailor.id"))
    sailor = db.relationship("Sailor", back_populates="certificate")


@app.route("/")
def index():
    return "/get_certificate/Pylyp /get_crew/Victoria"


@app.route("/get_crew/<ship_name>", methods=["GET"])
def get_crew(ship_name):
    ship = Ship.query.filter_by(name=ship_name).first()
    if ship:
        crew = [sailor.name for sailor in ship.sailors]
        return crew
    return "Ship not found"


@app.route("/get_certificate/<sailor_name>", methods=["GET"])
def get_certificate(sailor_name):
    sailor = Sailor.query.filter_by(name=sailor_name).first()
    if not sailor:
        return "Sailor not found"
    if not sailor.certificate:
        return "Sailor has no certificate"
    return sailor.certificate.date


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
