from flask import Blueprint

from app.resources.transactions import TransactionsResource

transactions_bp = Blueprint('transactions', __name__)

transactions_resource = TransactionsResource.as_view('transactions_resource')

# Main Budgets GET (get total stats), POST (writes new Transaction)
transactions_bp.add_url_rule(
    '/api/transactions',
    view_func=transactions_resource,
    methods=[
        'GET',
        'POST'
    ]
)

# Working with certain Budget by ID: GET (get Transaction), PUT (modifying Transaction), DELETE (deletes a Transaction)
transactions_bp.add_url_rule(
    '/api/transactions/<int:transaction_id>',
    view_func=transactions_resource,
    methods=[
        'GET',
        'PUT',
        'DELETE'
    ]
)

# getExpenses by year/month
transactions_bp.add_url_rule(
    '/api/transactions/<int:year>/<int:month>',
    view_func=transactions_resource,
    methods=[
        'GET',
    ]
)
