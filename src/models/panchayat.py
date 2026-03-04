from src import db


class Panchayat(db.Model):
    __tablename__ = "panchayat"

    panchayatID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    panchayatName = db.Column(db.String(255), nullable=False)
    unionID = db.Column(db.Integer, db.ForeignKey("unions.unionID"), nullable=False)
    cityID = db.Column(db.Integer, db.ForeignKey("city.cityID"), nullable=False)
    status = db.Column(db.String(20), default="yes")

    centres = db.relationship("ChildcareCentre", backref="panchayat", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "panchayatID": self.panchayatID,
            "panchayatName": self.panchayatName,
            "unionID": self.unionID,
            "unionName": self.union.unionName if self.union else "",
            "cityID": self.cityID,
            "cityName": self.city.cityName if self.city else "",
            "status": self.status,
        }
