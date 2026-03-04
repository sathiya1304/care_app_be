from src import db


class EvaluationMonth(db.Model):
    __tablename__ = "evaluationmonth"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    evaluationMonthEnd = db.Column(db.Date, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "evaluationMonthEnd": str(self.evaluationMonthEnd) if self.evaluationMonthEnd else None,
        }
