from datetime import datetime
from typing import Dict, List

from sqlalchemy import func, extract

from app import db


class Transaction(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)

    def __str__(self):
        return f"Date:\t{self.date}\n" \
               f"Category:\t{self.category}\n" \
               f"Description:\t{self.description}\n" \
               f"Amount:\t{self.amount}"

    def __repr__(self):
        return str(self)

    def to_dict(self) -> dict:
        data = dict()

        if self.id is not None:
            data.update(dict(id=self.id))

        data.update(
            dict(
                date=self.date.strftime('%d.%m.%y %H:%M'),
                category=self.category,
                amount=self.amount,
                description=self.description
            )
        )

        return data

    @staticmethod
    def get(transaction_id: int) -> 'Transaction':
        return Transaction.query.filter_by(id=transaction_id).first()

    @staticmethod
    def exists(transaction_id: int) -> bool:
        return Transaction.query.filter_by(id=transaction_id).first() is not None

    @staticmethod
    def add(date, category: str, description: str, amount: float) -> 'Transaction':
        new_tr = Transaction(date=date, category=category, description=description, amount=amount)
        db.session.add(new_tr)
        db.session.commit()
        return new_tr

    @staticmethod
    def edit_category(looking_category: str, new_category: str) -> int:
        transactions_by_bg = Transaction.find(looking_category)
        for tbg in transactions_by_bg:
            tbg.category = new_category
        db.session.commit()
        return len(transactions_by_bg)

    @staticmethod
    def edit_transaction(transaction_id: int, date: datetime, category: str, amount: float, description: str) -> 'Transaction':
        tr = Transaction.get(transaction_id)
        tr.date = date
        tr.category = category
        tr.amount = amount
        tr.description = description
        db.session.commit()
        return tr

    @staticmethod
    def delete_by_id(transaction_id: int):
        tr = Transaction.get(transaction_id)
        db.session.delete(tr)
        db.session.commit()

    @staticmethod
    def get_all() -> List[Dict]:
        return [i.to_dict() for i in Transaction.query.all()]

    @staticmethod
    def find(looking_category: str) -> List['Transaction']:
        return Transaction.query.filter_by(category=looking_category).all()

    @staticmethod
    def summarize(year, month) -> Dict:
        result = (
            db.session.query(
                Transaction.category,
                func.sum(Transaction.amount)
            )
                .filter(extract('year', Transaction.date) == year)
                .filter(extract('month', Transaction.date) == month)
                .group_by(Transaction.category)
                .all()
        )
        return {i[0]: i[1] for i in result}

    @staticmethod
    def total(year, month) -> float:
        return (
            db.session.query(
                func.sum(Transaction.amount)
            ).filter(extract('year', Transaction.date) == year)
            .filter(extract('month', Transaction.date) == month)
            .all()
        )[0][0]
