from src import db


class Cluster(db.Model):
    __tablename__ = "cluster"

    clusterID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clusterName = db.Column(db.String(255), nullable=False)
    centreID = db.Column(db.Integer, db.ForeignKey("childcarecentre.centreID"), nullable=True)
    status = db.Column(db.String(20), default="yes")

    employees = db.relationship("Employee", backref="cluster_ref", lazy=True, cascade="all, delete-orphan", foreign_keys="[Employee.clusterID]")

    def to_dict(self):
        return {
            "clusterID": self.clusterID,
            "clusterName": self.clusterName,
            "centreID": self.centreID,
            "centreName": self.centre.centreName if self.centre else "",
            "status": self.status,
        }
