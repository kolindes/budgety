from flask import Blueprint

from app.resources.budgets import BudgetsResource

budgets_bp = Blueprint('budgets', __name__)

budgets_resource = BudgetsResource.as_view('budgets_resource')


# Main Budgets GET (get all), POST (creates a new Budget)
budgets_bp.add_url_rule(
    '/api/budgets',
    view_func=budgets_resource,
    methods=[
        'GET',
        'POST'
    ]
)

# Working with certain Budget by ID: GET (get Budget), PUT (modifying Budget), DELETE (deletes Budget)
budgets_bp.add_url_rule(
    '/api/budgets/<string:looking_category>',
    view_func=budgets_resource,
    methods=[
        'GET',
        'PUT',
        'DELETE'
    ]
)
