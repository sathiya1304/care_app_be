from src import db


class ChildcareCentre(db.Model):
    __tablename__ = "childcarecentre"

    centreID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    centreName = db.Column(db.String(255), nullable=False)
    panchayatID = db.Column(db.Integer, db.ForeignKey("panchayat.panchayatID"), nullable=False)
    cityID = db.Column(db.Integer, db.ForeignKey("city.cityID"), nullable=False)
    unionID = db.Column(db.Integer, db.ForeignKey("unions.unionID"), nullable=False)
    status = db.Column(db.String(20), default="yes")

    clusters = db.relationship("Cluster", backref="centre", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "centreID": self.centreID,
            "centreName": self.centreName,
            "panchayatID": self.panchayatID,
            "panchayatName": self.panchayat.panchayatName if self.panchayat else "",
            "unionID": self.unionID,
            "unionName": self.union.unionName if self.union else "",
            "cityID": self.cityID,
            "cityName": self.city.cityName if self.city else "",
            "status": self.status,
        }
