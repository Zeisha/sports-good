from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SportsGoodInventory(db.Model):
    __tablename__ = 'sports_goods'

    good_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Integer())
    sport = db.Column(db.String(80))

    def __init__(self, good_id, name, price, sport):
        self.good_id = good_id
        self.name = name
        self.price = price
        self.sport = sport

    def __repr__(self):
        return f"{self.name}:{self.good_id}"
