from src import db


class Union(db.Model):
    __tablename__ = "unions"

    unionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unionName = db.Column(db.String(255), nullable=False)
    cityID = db.Column(db.Integer, db.ForeignKey("city.cityID"), nullable=False)
    status = db.Column(db.String(20), default="yes")

    panchayats = db.relationship("Panchayat", backref="union", lazy=True, cascade="all, delete-orphan")
    centres = db.relationship("ChildcareCentre", backref="union", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "unionID": self.unionID,
            "unionName": self.unionName,
            "cityID": self.cityID,
            "cityName": self.city.cityName if self.city else "",
            "status": self.status,
        }
