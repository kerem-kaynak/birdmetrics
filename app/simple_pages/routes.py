from os import name
from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user

from app.simple_pages.helpers.graph_metric import graph_metric
from app.authentication.helpers.forms import LoginForm

blueprint = Blueprint('simple_pages', __name__)

metric_dict = {
    'arr': 'ARR',
    'mrr': 'MRR',
    'new_mrr': 'New MRR',
    'expansion_mrr': 'Expansion MRR',
    'contraction_mrr': 'Contraction MRR',
    'churned_mrr': 'Churned MRR',
    'customers': 'Customers',
    'new_customers': 'New Customers',
    'churned_customers': 'Churned Customers',
    'arpa': 'ARPA',
    'logo_churn_rate': 'Logo Churn Rate',
    'customer_lifetime': 'Average Customer Lifetime',
    'lifetime_value': 'Customer Lifetime Value',
    'net_mrr_churn': 'Net MRR Churn',
    'quick_ratio': 'Quick Ratio',
    'logo_retention': 'Logo Retention',
    'ndr': 'Net Dollar Retention',
    'monthly_gross_churn': 'Gross MRR Churn'
}

@blueprint.route('/')
def index():
    user_id = current_user.id
    page_name = 'Dashboard'
    return render_template('simple_pages/homepage.html', page_name=page_name, metrics=['arr'], user_id=user_id, metric_dict=metric_dict)
    
