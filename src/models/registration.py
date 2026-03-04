from src import db


class Registration(db.Model):
    __tablename__ = "registration"

    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mobile = db.Column(db.String(15), nullable=False, index=True)
    childName = db.Column(db.String(255), nullable=False)
    fatherName = db.Column(db.String(255), nullable=True)
    motherName = db.Column(db.String(255), nullable=True)
    dateofRegistration = db.Column(db.Date, nullable=True)
    dateofBirth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    city = db.Column(db.String(255), nullable=True)
    myunion = db.Column(db.String(255), nullable=True)
    panchayat = db.Column(db.String(255), nullable=True)
    centreName = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default="yes")

    def to_dict(self):
        return {
            "sno": self.sno,
            "mobile": self.mobile,
            "childName": self.childName,
            "fatherName": self.fatherName,
            "motherName": self.motherName,
            "dateofRegistration": str(self.dateofRegistration) if self.dateofRegistration else None,
            "dateofBirth": str(self.dateofBirth) if self.dateofBirth else None,
            "gender": self.gender,
            "age": self.age,
            "city": self.city,
            "myunion": self.myunion,
            "panchayat": self.panchayat,
            "centreName": self.centreName,
            "status": self.status,
        }
