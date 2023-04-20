import calendar
import datetime

from flask_jwt_extended import jwt_required
from flask_restful import reqparse, Resource

from app.models import Budget, Transaction
from app.response_templates.utils import get_base_response, BaseResponseStatus


class TransactionsResource(Resource):

    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.req_parse.add_argument('date', type=str, required=True, help='No date provided', location='json')
        self.req_parse.add_argument('category', type=str, required=True, help='No category provided', location='json')
        self.req_parse.add_argument('description', type=str, required=False, help='No task provided', location='json', default='No description.')
        self.req_parse.add_argument('amount', type=float, required=True, help='No amount provided', location='json')
        super(TransactionsResource, self).__init__()

    @staticmethod
    @jwt_required()
    def get(transaction_id: int = None, year: int = None, month: int = None):
        response = get_base_response()

        if transaction_id is not None:
            transaction = Transaction.get(transaction_id)
            if transaction is None:
                response['status'] = BaseResponseStatus.ERROR
                response['message'] = f'Transaction ID:{transaction_id} not found.'
                return response, 404
            response['message'] = f'Transaction ID:{transaction_id} found.'
            response['data'] = transaction.to_dict()
            return response, 200

        if year is None and month is None:
            response['data'] = Transaction.get_all()
            return response, 200

        else:
            summarized_transactions = Transaction.summarize(year, month)

            if not summarized_transactions:
                response['status'] = BaseResponseStatus.ERROR
                response['message'] = f"No transactions were found. Please add at least one transaction and try again."
                return response, 404

            budgets = Budget.get_budget_amounts()

            expenses = [
                dict(
                    category=category,
                    value=value,
                    budget=budgets[category],
                    diff=round(budgets[category] - value, 2),
                    transactions=len(Transaction.find(category))
                ) for category, value in summarized_transactions.items()
            ]

            budget_total = Budget.total()
            expenses_total = Transaction.total(year, month)
            total = dict(
                budget=budget_total,
                expenses=expenses_total,
                diff=round(budget_total - expenses_total, 2),
                transactions=len(Transaction.get_all())
            )

            response['data'] = {
                "date": f"{calendar.month_name[month]} {year}",
                "expenses": expenses,
                "total": total
            }

            return response, 200

    @jwt_required()
    def post(self, transaction_id: int = None, response: dict = None):
        if response is None:
            response = get_base_response()

        errors = []

        args = self.req_parse.parse_args()

        response['message'] = args

        required_fields = {"date", "category", "description", "amount"}

        if not required_fields.issubset(args.keys()):
            missing_fields = required_fields - args.keys()
            response['status'] = BaseResponseStatus.ERROR
            response['message'] = f"Missing fields: {', '.join(missing_fields)}"
            return response, 400

        try:
            args['date'] = datetime.datetime.strptime(args['date'], "%d.%m.%Y %H:%M")
        except (ValueError, TypeError):
            errors.append(f'Invalid date, example: "01.01.2023 18:00", got: "%s".' % str(args))

        category = args['category']
        categories = Budget.get_category_names()
        if not category:
            errors.append(f'Invalid category name, example: "food".')
        elif category not in categories:
            errors.append(f'Given category "{category}" not found.')

        description = args['description'] if args['description'] else "No description."

        try:
            args['amount'] = float(args['amount'])
        except (ValueError, TypeError):
            errors.append(f'Amount value is incorrect, example: "100.0".')

        if errors:
            response['status'] = BaseResponseStatus.ERROR
            response['message'] = '\n'.join(errors)
            return response, 400

        if transaction_id is not None:
            transaction = Transaction.edit_transaction(
                transaction_id=transaction_id,
                date=args['date'],
                category=category,
                amount=args['amount'],
                description=description
            )
            message, code = 'Transaction edited.', 200

        else:
            transaction = Transaction.add(
                date=args['date'],
                category=category,
                description=description,
                amount=args['amount']
            )
            message, code = 'Transaction created.', 201

        response['data'] = transaction.to_dict()
        response['message'] = message

        return response, code

    @jwt_required()
    def put(self, transaction_id: int):
        response = get_base_response()

        if Transaction.exists(transaction_id) is False:
            response['status'] = BaseResponseStatus.ERROR
            response['message'] = f"Transaction ID:{transaction_id} not found."
            return response, 404

        return self.post(transaction_id, response)

    @staticmethod
    @jwt_required()
    def delete(transaction_id: int):
        response = get_base_response()

        if Transaction.exists(transaction_id) is False:
            response['status'] = BaseResponseStatus.ERROR
            response['message'] = f"Transaction ID:{transaction_id} not found."
            return response, 404

        Transaction.delete_by_id(transaction_id)
        response['message'] = f'Transaction ID:{transaction_id} deleted.'

        return response, 200
