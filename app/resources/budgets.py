import re

from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required

from app.models import Budget, Transaction
from app.response_templates.utils import get_base_response, BaseResponseStatus


class BudgetsResource(Resource):

    def __init__(self):
        self.req_parse = reqparse.RequestParser()
        self.req_parse.add_argument('category', type=str, required=True, help='No category provided', location='json')
        self.req_parse.add_argument('description', type=str, required=False, help='No task provided', location='json', default='No description.')
        self.req_parse.add_argument('amount', type=float, required=True, help='No amount provided', location='json')
        super(BudgetsResource, self).__init__()

    @staticmethod
    @jwt_required()
    def get(looking_category: str = None):
        response = get_base_response()

        if looking_category is None:
            response['data'] = Budget.get_all()
            code = 200

        elif looking_category.lower() == 'categories':
            response['data'] = Budget.get_category_names()
            code = 200

        elif looking_category and Budget.exists(looking_category):
            response['data'] = Budget.get(looking_category).to_dict()
            code = 200

        else:
            response['status'] = BaseResponseStatus.ERROR
            response['message'] = f'Category "{looking_category}" was not found.'
            code = 404

        return response, code

    @staticmethod
    @jwt_required()
    def get_categories():
        response = get_base_response()
        response['data'] = Budget.get_category_names()
        code = 200
        return response, code

    @jwt_required()
    def post(self, looking_category: str = None, response: dict = None):
        if response is None:
            response = get_base_response()

        forbidden_names = ['categories']
        errors = []
        required_fields = {"category", "description", "amount"}
        args = self.req_parse.parse_args()

        if not required_fields.issubset(args.keys()):
            missing_fields = required_fields - args.keys()
            response['status'] = BaseResponseStatus.ERROR
            response['message'] = f"Missing fields: {', '.join(missing_fields)}"
            return response, 400

        category = args['category']

        if category is None or category == '':
            errors.append(f'Category name cannot be empty.')

        elif category.lower() in forbidden_names:
            errors.append("You can't use the name \"{}\" because it is in the list of reserved words.".format(category))

        else:
            non_matching_symbols = ''.join(set(re.findall(r'[^a-zA-Zа-яА-Я0-9\s]', category)))

            if non_matching_symbols:
                errors.append(f'Invalid symbols found in category name: "{non_matching_symbols}".')

        if looking_category is None:
            if not category:
                errors.append(f'Invalid category name, example: "food".')
            elif Budget.exists(category):
                errors.append(f'Category "{category}" is already exists.')

        description = args['description'] if args['description'] else "No description."

        try:
            args['amount'] = float(args['amount'])
        except (ValueError, TypeError) as e:
            errors.append(f'Amount value is incorrect, example: "100.0".')

        if errors:
            response['status'] = BaseResponseStatus.ERROR
            response['message'] = '\n- ' + '\n\n- '.join(errors)
            return response, 400

        if looking_category is not None:
            budget = Budget.edit(looking_category, category, args['amount'], description)
            transactions_count = Transaction.edit_category(looking_category, category)
            response['data'] = budget.to_dict()
            response['data'].update(dict(transactions=transactions_count))
            response['message'] = f'Budget edited.'

        else:
            budget = Budget.add(category=category, description=description, amount=args['amount'])
            response['data'] = budget.to_dict()
            response['message'] = f'Budget created.'

        return response, 200

    @jwt_required()
    def put(self, looking_category: str = None):
        response = get_base_response()

        if looking_category is None:
            response['status'] = BaseResponseStatus.ERROR
            response['message'] = 'Invalid category name. Example: "food". '
            return response, 400

        if Budget.exists(looking_category) is False:
            response['status'] = BaseResponseStatus.ERROR
            response['message'] = f'Category "{looking_category}" was not found.'
            return response, 404

        return self.post(looking_category, response)

    @staticmethod
    @jwt_required()
    def delete(looking_category: str):
        response = get_base_response()

        if Budget.exists(looking_category) is False:
            response['status'] = BaseResponseStatus.ERROR
            response['message'] = f'Budget "{looking_category}" not found.'
            return response, 404

        transactions_by_bg = Transaction.find(looking_category)

        if transactions_by_bg:
            response['status'] = BaseResponseStatus.ERROR
            response['message'] = f'Impossible to delete the budget "{looking_category}" ' \
                                  f'as there are transactions in the budget: {len(transactions_by_bg)}.\n' \
                                  f'Delete or modify the transactions before deleting the budget.'
            return response, 409

        Budget.delete_by_category(looking_category)

        response['message'] = f'Budget "{looking_category}" deleted.'

        return response, 200
