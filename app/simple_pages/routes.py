from crypt import methods
from datetime import date
from distutils.command.upload import upload
from os import name
from flask import Blueprint, redirect, render_template, url_for, request, flash
from flask_login import current_user, login_required
from flask.helpers import get_flashed_messages
import json
import datetime
from app.simple_pages.helpers.graph_metric import graph_metric
from app.authentication.helpers.forms import LoginForm
from app.simple_pages.helpers.metric_calculation import *

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

@blueprint.route('/revenue')
@login_required
def revenue():
    user_id = current_user.id
    page_name = 'Revenue Metrics'
    metrics = ['arr','mrr','new_mrr','expansion_mrr','contraction_mrr','churned_mrr']
    return render_template('simple_pages/metric_page.html', page_name=page_name, metrics=metrics, user_id=user_id, metric_dict=metric_dict)

@blueprint.route('/customers')
@login_required
def customers():
    user_id = current_user.id
    page_name = 'Customer Metrics'
    metrics = ['customers','new_customers','churned_customers']
    return render_template('simple_pages/metric_page.html', page_name=page_name, metrics=metrics, user_id=user_id, metric_dict=metric_dict)

@blueprint.route('/retention')
@login_required
def retention():
    user_id = current_user.id
    page_name = 'Retention Metrics'
    metrics = ['logo_retention','logo_churn_rate','customer_lifetime']
    return render_template('simple_pages/metric_page.html', page_name=page_name, metrics=metrics, user_id=user_id, metric_dict=metric_dict)

@blueprint.route('/profitability')
@login_required
def profitability():
    user_id = current_user.id
    page_name = 'Profitability Metrics'
    metrics = ['arpa','lifetime_value']
    return render_template('simple_pages/metric_page.html', page_name=page_name, metrics=metrics, user_id=user_id, metric_dict=metric_dict)

@blueprint.route('/unit_economics')
@login_required
def unit_economics():
    user_id = current_user.id
    page_name = 'Unit Economics'
    metrics = ['ndr','monthly_gross_churn','net_mrr_churn', 'quick_ratio']
    return render_template('simple_pages/metric_page.html', page_name=page_name, metrics=metrics, user_id=user_id, metric_dict=metric_dict)
    
@blueprint.route('/upload')
@login_required
def upload_file():
    return render_template('simple_pages/upload_page.html')

@blueprint.route('/')
def index():
    return redirect(url_for('simple_pages.revenue'))

@blueprint.route('/fileupload', methods=['POST'])
@login_required
def file_upload():
    upload_data = request.form.get("data", False)
    upload_data = json.loads(upload_data)
    for i in upload_data.keys():
        if i != 'time':
            for j in range(len(upload_data[i])):
                upload_data[i][j] = float(upload_data[i][j])
        else:
            for j in range(len(upload_data[i])):
                upload_data[i][j] = datetime.datetime.strptime(upload_data[i][j], '%Y-%m-%d').date()
    run_metrics(upload_data)
    return redirect(url_for('simple_pages.revenue'))

@blueprint.route('/retention_heatmap')
@login_required
def retention_heatmap():
    user_id = current_user.id
    page_name = 'Cohort Retention Heatmap'
    tmp = Heatmap.query.filter_by(company_id = user_id).all()
    if len(tmp) < 1:
        return render_template('simple_pages/heatmap.html', graph = 'Upload data to view your heatmap.', page_name = page_name)
    graph = Markup(tmp[0].graph_markup)
    return render_template('simple_pages/heatmap.html', graph = graph, page_name=page_name)