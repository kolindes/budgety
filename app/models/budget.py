from typing import List, Dict

from sqlalchemy import func

from app import db


class Budget(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)

    def __str__(self):
        return f"Category:\t{self.category}\n" \
               f"Description:\t{self.description}\n" \
               f"Amount:\t{self.amount}"

    def __repr__(self):
        return str(self)

    def to_dict(self) -> Dict:
        return dict(
            category=self.category,
            amount=self.amount,
            description=self.description
        )

    @staticmethod
    def get(category: str) -> 'Budget':
        return Budget.query.filter_by(category=category).first()

    @staticmethod
    def add(category: str, description: str, amount: float) -> 'Budget':
        new_bg = Budget(category=category, description=description, amount=amount)
        db.session.add(
            new_bg
        )
        db.session.commit()
        return new_bg

    @staticmethod
    def edit(looking_category: str, new_category: str, amount: float, description: str) -> 'Budget':
        budget = Budget.get(looking_category)
        budget.category = new_category
        budget.description = description
        budget.amount = amount
        db.session.commit()
        return budget

    @staticmethod
    def delete_by_category(looking_category: str):
        db.session.delete(
            Budget.get(looking_category)
        )
        db.session.commit()

    @staticmethod
    def exists(category: str) -> bool:
        return Budget.query.filter_by(category=category).first() is not None

    @staticmethod
    def get_category_names() -> List[str]:
        return [i[0] for i in db.session.query(Budget.category).all()]

    @staticmethod
    def get_all() -> List['Budget']:
        return [i.to_dict() for i in Budget.query.all()]

    @staticmethod
    def get_budget_amounts() -> Dict:
        result = (
            db.session.query(
                Budget.category,
                Budget.amount
            )
                .all()
        )
        return {i[0]: i[1] for i in result}

    @staticmethod
    def total() -> float:
        return (
            db.session.query(
                func.sum(Budget.amount)
            ).all()
        )[0][0]
