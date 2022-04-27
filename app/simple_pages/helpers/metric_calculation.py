import json
from unittest import skip
from flask_login import current_user
import pandas as pd
import numpy as np
from app.authentication.models import Metric, Heatmap
from app.extensions.database import db
import plotly
from sqlalchemy import true
import plotly.express as px
from markupsafe import Markup




dummy = {'time':['2021-01-01','2021-02-01','2021-03-01','2021-04-01','2021-05-01','2021-06-01',],
'acc1':[1000,800,900,1000,1000,1400],
'acc2':[400,800,800,800,800,1000],
'acc3':[500,600,0,0,0,0],
'acc4':[0,0,0,3000,3000,3500]
}

def json_to_df(data):
    df = pd.DataFrame.from_dict(data, orient='index', columns=data['time'])
    df.drop(['time'], inplace = True)

    return df

# MRR

def mrr_calc(df):
    mrr = df.sum()
    for i in range(len(mrr)):
        new_log = Metric(company_id = current_user.id, metric_name = 'mrr', month = mrr.index[i], value = mrr[i])
        new_log.save()

    return None

def arr_calc(df):
    mrr = 12 * df.sum()
    for i in range(len(mrr)):
        new_log = Metric(company_id = current_user.id, metric_name = 'arr', month = mrr.index[i], value = mrr[i])
        new_log.save()

    return None

def new_mrr_calc(df):
    temp = df.copy()
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if ((df.iloc[i,j] != 0) & (df.iloc[i,j-1] == 0)):
                next
            else:
                temp.iloc[i,j] = 0
    new_mrr = temp.sum()
    for i in range(len(new_mrr)):
        new_log = Metric(company_id = current_user.id, metric_name = 'new_mrr', month = new_mrr.index[i], value = new_mrr[i])
        new_log.save()

    return None

def churned_mrr_calc(df):
    temp = df.copy()
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if ((df.iloc[i,j] == 0) & (df.iloc[i,j-1] != 0)):
                temp.iloc[i,j] = -1 * df.iloc[i,j-1]
            else:
                temp.iloc[i,j] = 0
    churned_mrr = temp.sum()
    churned_mrr[0] = 0
    for i in range(len(churned_mrr)):
        new_log = Metric(company_id = current_user.id, metric_name = 'churned_mrr', month = churned_mrr.index[i], value = churned_mrr[i])
        new_log.save()

    return None

def expansion_mrr_calc(df):
    temp = df.copy()
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if (df.iloc[i,j] > df.iloc[i,j-1]) & (df.iloc[i,j-1] != 0):
                temp.iloc[i,j] = df.iloc[i,j] - df.iloc[i,j-1]
            else:
                temp.iloc[i,j] = 0
    expansion_mrr = temp.sum()
    expansion_mrr[0] = 0
    for i in range(len(expansion_mrr)):
        new_log = Metric(company_id = current_user.id, metric_name='expansion_mrr', month=expansion_mrr.index[i], value = expansion_mrr[i])
        new_log.save()

    return None

def contraction_mrr_calc(df):
    temp = df.copy()
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if (df.iloc[i,j] < df.iloc[i,j-1]) & (df.iloc[i,j-1] != 0) & (df.iloc[i,j] != 0):
                temp.iloc[i,j] = df.iloc[i,j] - df.iloc[i,j-1]
            else:
                temp.iloc[i,j] = 0
    contraction_mrr = temp.sum()
    contraction_mrr[0] = 0
    for i in range(len(contraction_mrr)):
        new_log = Metric(company_id = current_user.id, metric_name='contraction_mrr', month=contraction_mrr.index[i], value = contraction_mrr[i])
        new_log.save()

    return None

def run_metrics(data):
    df = json_to_df(data)
    wipe_user_data()
    mrr_calc(df)
    arr_calc(df)
    new_mrr_calc(df)
    churned_mrr_calc(df)
    expansion_mrr_calc(df)
    contraction_mrr_calc(df)
    customers_calc(df)
    new_customers_calc(df)
    churned_customers_calc(df)
    logo_retention_calc(df)
    logo_churn_rate_calc(df)
    customer_lifetime_calc(df)
    arpa_calc(df)
    lifetime_value_calc(df)
    ndr_calc(df)
    monthly_gross_churn_calc(df)
    net_mrr_churn_calc(df)
    quick_ratio_calc(df)
    retention_heatmap(df)

    return None

def customers_calc(df):
    temp = df.copy()
    customers = (temp!=0).sum()
    for i in range(len(customers)):
        new_log = Metric(company_id = current_user.id, metric_name = 'customers', month=customers.index[i], value=customers[i])
        new_log.save()
    return None

def new_customers_calc(df):
    temp = df.copy()
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if ((df.iloc[i,j] != 0) & (df.iloc[i,j-1] == 0)):
                temp.iloc[i,j] = 1
            else:
                temp.iloc[i,j] = 0
    new_customers = (temp!=0).sum()
    for i in range(len(new_customers)):
        new_log = Metric(company_id = current_user.id, metric_name = 'new_customers', month = new_customers.index[i], value = new_customers[i])
        new_log.save()

    return None

def churned_customers_calc(df):
    temp = df.copy()
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if ((df.iloc[i,j] == 0) & (df.iloc[i,j-1] != 0)):
                temp.iloc[i,j] = -1 * df.iloc[i,j-1]
            else:
                temp.iloc[i,j] = 0
    churned_customers = (temp!=0).sum()
    churned_customers[0] = 0
    for i in range(len(churned_customers)):
        new_log = Metric(company_id = current_user.id, metric_name = 'churned_customers', month = churned_customers.index[i], value = churned_customers[i])
        new_log.save()

    return None

def logo_retention_calc(df):
    for j in range(1,len(df.columns)):
        prev_customers = 0
        retained_customers = 0
        for i in range(len(df)):
            if df.iloc[i,j-1] != 0:
                prev_customers += 1
                if df.iloc[i,j] != 0:
                    retained_customers += 1
        rate = retained_customers / prev_customers
        new_log = Metric(company_id = current_user.id, metric_name = 'logo_retention', month = df.columns[j], value = rate)
        new_log.save()
    
    return None

def logo_churn_rate_calc(df):
    for j in range(1,len(df.columns)):
        prev_customers = 0
        churned_customers = 0
        for i in range(len(df)):
            if df.iloc[i,j-1] != 0:
                prev_customers += 1
                if df.iloc[i,j] == 0:
                    churned_customers += 1
        rate = churned_customers / prev_customers
        new_log = Metric(company_id = current_user.id, metric_name = 'logo_churn_rate', month = df.columns[j], value = rate)
        new_log.save()
    
    return None

def customer_lifetime_calc(df):
    for j in range(1,len(df.columns)):
        prev_customers = 0
        churned_customers = 0
        for i in range(len(df)):
            if df.iloc[i,j-1] != 0:
                prev_customers += 1
                if df.iloc[i,j] == 0:
                    churned_customers += 1
        rate = churned_customers / prev_customers
        if rate == 0:
            new_log = Metric(company_id = current_user.id, metric_name = 'customer_lifetime', month = df.columns[j], value = 0)
            new_log.save()
        else:
            new_log = Metric(company_id = current_user.id, metric_name = 'customer_lifetime', month = df.columns[j], value = 1/rate)
            new_log.save()
    
    return None

def arpa_calc(df):
    mrr = df.sum()
    customers = (df!=0).sum()
    arpa = mrr/customers
    for i in range(len(arpa)):
        new_log = Metric(company_id = current_user.id, metric_name = 'arpa', month = arpa.index[i], value = arpa[i])
        new_log.save()

    return None

def lifetime_value_calc(df):
    temp_arpa = df.copy()
    temp_arpa.drop(temp_arpa.columns[0], axis = 1, inplace = True)
    mrr = temp_arpa.sum()
    customers = (temp_arpa!=0).sum()
    arpa = mrr/customers
    for j in range(1,len(df.columns)):
        prev_customers = 0
        churned_customers = 0
        for i in range(len(df)):
            if df.iloc[i,j-1] != 0:
                prev_customers += 1
                if df.iloc[i,j] == 0:
                    churned_customers += 1
        rate = churned_customers / prev_customers
        if rate == 0:
            new_log = Metric(company_id = current_user.id, metric_name = 'lifetime_value', month = df.columns[j], value = 0)
            new_log.save()
        else:
            new_log = Metric(company_id = current_user.id, metric_name = 'lifetime_value', month = df.columns[j], value = arpa[j-1]*(1/rate))
            new_log.save()

    return None

def ndr_calc(df):
    mrr = df.sum()

    temp_exp = df.copy()
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if (df.iloc[i,j] > df.iloc[i,j-1]) & (df.iloc[i,j-1] != 0):
                temp_exp.iloc[i,j] = df.iloc[i,j] - df.iloc[i,j-1]
            else:
                temp_exp.iloc[i,j] = 0
    expansion_mrr = temp_exp.sum()
    expansion_mrr[0] = 0

    temp_churn = df.copy()
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if ((df.iloc[i,j] == 0) & (df.iloc[i,j-1] != 0)):
                temp_churn.iloc[i,j] = -1 * df.iloc[i,j-1]
            else:
                temp_churn.iloc[i,j] = 0
    churned_mrr = temp_churn.sum()
    churned_mrr[0] = 0

    temp_con = df.copy()
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if (df.iloc[i,j] < df.iloc[i,j-1]) & (df.iloc[i,j-1] != 0) & (df.iloc[i,j] != 0):
                temp_con.iloc[i,j] = df.iloc[i,j] - df.iloc[i,j-1]
            else:
                temp_con.iloc[i,j] = 0
    contraction_mrr = temp_con.sum()
    contraction_mrr[0] = 0

    temp_ndr = mrr.copy()
    temp_ndr[0] = 0

    for i in range(1,len(mrr)):
        temp_ndr[i] = 1 + ((expansion_mrr[i] + churned_mrr[i] + contraction_mrr[i]) / mrr[i-1])

    for i in range(len(temp_ndr)):
        new_log = Metric(company_id = current_user.id, metric_name = 'ndr', month = temp_ndr.index[i], value = temp_ndr[i])
        new_log.save()

    return None

def monthly_gross_churn_calc(df):
    temp_churn = df.copy()
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if ((df.iloc[i,j] == 0) & (df.iloc[i,j-1] != 0)):
                temp_churn.iloc[i,j] = -1 * df.iloc[i,j-1]
            else:
                temp_churn.iloc[i,j] = 0
    churned_mrr = temp_churn.sum()
    churned_mrr[0] = 0

    temp_con = df.copy()
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if (df.iloc[i,j] < df.iloc[i,j-1]) & (df.iloc[i,j-1] != 0) & (df.iloc[i,j] != 0):
                temp_con.iloc[i,j] = df.iloc[i,j] - df.iloc[i,j-1]
            else:
                temp_con.iloc[i,j] = 0
    contraction_mrr = temp_con.sum()
    contraction_mrr[0] = 0

    mrr = df.sum()

    monthly_gross_churn = -1 * (churned_mrr + contraction_mrr) / mrr

    for i in range(len(monthly_gross_churn)):
        new_log = Metric(company_id = current_user.id, metric_name = 'monthly_gross_churn', month = monthly_gross_churn.index[i], value = monthly_gross_churn[i])
        new_log.save()

    return None

def net_mrr_churn_calc(df):
    temp_exp = df.copy()
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if (df.iloc[i,j] > df.iloc[i,j-1]) & (df.iloc[i,j-1] != 0):
                temp_exp.iloc[i,j] = df.iloc[i,j] - df.iloc[i,j-1]
            else:
                temp_exp.iloc[i,j] = 0
    expansion_mrr = temp_exp.sum()
    expansion_mrr[0] = 0

    temp_churn = df.copy()
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if ((df.iloc[i,j] == 0) & (df.iloc[i,j-1] != 0)):
                temp_churn.iloc[i,j] = -1 * df.iloc[i,j-1]
            else:
                temp_churn.iloc[i,j] = 0
    churned_mrr = temp_churn.sum()
    churned_mrr[0] = 0

    temp_con = df.copy()
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if (df.iloc[i,j] < df.iloc[i,j-1]) & (df.iloc[i,j-1] != 0) & (df.iloc[i,j] != 0):
                temp_con.iloc[i,j] = df.iloc[i,j] - df.iloc[i,j-1]
            else:
                temp_con.iloc[i,j] = 0
    contraction_mrr = temp_con.sum()
    contraction_mrr[0] = 0

    mrr = df.sum()

    net_mrr_churn = (-1 * (contraction_mrr + churned_mrr) - expansion_mrr) / mrr

    for i in range(len(net_mrr_churn)):
        new_log = Metric(company_id = current_user.id, metric_name = 'net_mrr_churn', month = net_mrr_churn.index[i], value = net_mrr_churn[i])
        new_log.save()

    return None

def quick_ratio_calc(df):
    temp_exp = df.copy()
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if (df.iloc[i,j] > df.iloc[i,j-1]) & (df.iloc[i,j-1] != 0):
                temp_exp.iloc[i,j] = df.iloc[i,j] - df.iloc[i,j-1]
            else:
                temp_exp.iloc[i,j] = 0
    expansion_mrr = temp_exp.sum()
    expansion_mrr[0] = 0

    temp_churn = df.copy()
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if ((df.iloc[i,j] == 0) & (df.iloc[i,j-1] != 0)):
                temp_churn.iloc[i,j] = -1 * df.iloc[i,j-1]
            else:
                temp_churn.iloc[i,j] = 0
    churned_mrr = temp_churn.sum()
    churned_mrr[0] = 0

    temp_con = df.copy()
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if (df.iloc[i,j] < df.iloc[i,j-1]) & (df.iloc[i,j-1] != 0) & (df.iloc[i,j] != 0):
                temp_con.iloc[i,j] = df.iloc[i,j] - df.iloc[i,j-1]
            else:
                temp_con.iloc[i,j] = 0
    contraction_mrr = temp_con.sum()
    contraction_mrr[0] = 0

    temp_new = df.copy()
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if ((df.iloc[i,j] != 0) & (df.iloc[i,j-1] == 0)):
                next
            else:
                temp_new.iloc[i,j] = 0
    new_mrr = temp_new.sum()
    new_mrr[0] = 0

    quick_ratio = new_mrr.copy()

    for i in range(len(new_mrr)):
        if (contraction_mrr[i] + churned_mrr[i]) == 0:
            quick_ratio[i] = 0
        else:
            quick_ratio[i] = (new_mrr[i] + expansion_mrr[i]) / (-1 * (contraction_mrr[i] + churned_mrr[i]))
    for i in range(len(quick_ratio)):
        new_log = Metric(company_id = current_user.id, metric_name = 'quick_ratio', month = quick_ratio.index[i], value = quick_ratio[i])
        new_log.save()

    return None

def wipe_user_data():
    user_id = current_user.id
    try:
        Metric.query.filter_by(company_id = user_id).delete()
        Heatmap.query.filter_by(company_id = user_id).delete()
        db.session.commit()
    except:
        db.session.rollback()

def retention_heatmap(df):
    zeros_data = np.zeros(shape=(len(df.columns), len(df.columns)))
    retention_data = pd.DataFrame(zeros_data, columns=list(range(len(df.columns))), index=df.columns)
    for i in range(len(df.columns)):
        retention_col = [0] * (len(df.columns))
        for j in range(i,len(df.columns)):
            for t in range(len(df.index)):
                if ((df.iloc[t,i] != 0) & (df.iloc[t,j] != 0)):
                    retention_col[j-i] += 1
        retention_col = list(np.array(retention_col) / np.array([retention_col[0] for i in range(len(retention_col))]))
        retention_data.iloc[i] = retention_col
    heatmap = px.imshow(retention_data, text_auto = True, color_continuous_scale='rdylgn')
    heatmap.update_xaxes(side="top")
    heatmap.layout.update(xaxis = dict(
        tickmode='linear',
    ))
    heatmap.layout.update(yaxis = dict(
        tickvals=retention_data.index
    ))
    graph =  plotly.io.to_html(heatmap)
    new_log = Heatmap(company_id = current_user.id, graph_markup = Markup(graph))
    new_log.save()
    return None