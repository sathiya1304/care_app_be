from src import db


class Evaluate(db.Model):
    __tablename__ = "evaluate"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mobile = db.Column(db.String(15), nullable=False, index=True)
    childName = db.Column(db.String(255), nullable=False)
    centreName = db.Column(db.String(255), nullable=True)
    dateofBirth = db.Column(db.Date, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    termStatus = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default="yes")

    # Term score columns (comma-separated score strings)
    term1 = db.Column(db.Text, nullable=True)
    term2 = db.Column(db.Text, nullable=True)
    term3 = db.Column(db.Text, nullable=True)
    term4 = db.Column(db.Text, nullable=True)
    term5 = db.Column(db.Text, nullable=True)
    term6 = db.Column(db.Text, nullable=True)
    term7 = db.Column(db.Text, nullable=True)
    term8 = db.Column(db.Text, nullable=True)
    term9 = db.Column(db.Text, nullable=True)
    term10 = db.Column(db.Text, nullable=True)
    term11 = db.Column(db.Text, nullable=True)
    term12 = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "mobile": self.mobile,
            "childName": self.childName,
            "centreName": self.centreName,
            "dateofBirth": str(self.dateofBirth) if self.dateofBirth else None,
            "age": self.age,
            "termStatus": self.termStatus,
            "status": self.status,
            **{f"term{i}": getattr(self, f"term{i}") for i in range(1, 13)},
        }
