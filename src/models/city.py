from src import db


class City(db.Model):
    __tablename__ = "city"

    cityID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cityName = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default="yes")

    unions = db.relationship("Union", backref="city", lazy=True, cascade="all, delete-orphan")
    panchayats = db.relationship("Panchayat", backref="city", lazy=True, cascade="all, delete-orphan")
    centres = db.relationship("ChildcareCentre", backref="city", lazy=True, cascade="all, delete-orphan")
    employees = db.relationship("Employee", backref="city", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "cityID": self.cityID,
            "cityName": self.cityName,
            "status": self.status,
        }
