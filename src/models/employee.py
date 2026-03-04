from src import db


class Employee(db.Model):
    __tablename__ = "employee"

    employeeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cityID = db.Column(db.Integer, db.ForeignKey("city.cityID"), nullable=True)
    clusterID = db.Column(db.Integer, db.ForeignKey("cluster.clusterID"), nullable=True)
    userName = db.Column(db.String(255), nullable=False)
    userPassword = db.Column(db.String(255), nullable=False)
    otherInfo = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="yes")


    def to_dict(self):
        return {
            "employeeID": self.employeeID,
            "cityID": self.cityID,
            "cityName": self.city.cityName if self.city else "",
            "clusterID": self.clusterID,
            "clusterName": self.cluster_ref.clusterName if self.cluster_ref else "",
            "userName": self.userName,
            "userPassword": self.userPassword,
            "otherInfo": self.otherInfo,
            "status": self.status,
        }
