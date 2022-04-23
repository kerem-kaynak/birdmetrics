from flask_login import current_user
import pandas as pd
from app.authentication.models import Metric

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
    temp = df
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if (df.iloc[i,j] != 0) & (df.iloc[i,j-1] == 0):
                temp.iloc[i,j] = 0
    new_mrr = temp.sum()
    for i in range(len(new_mrr)):
        new_log = Metric(company_id = current_user.id, metric_name = 'new_mrr', month = new_mrr.index[i], value = new_mrr[i])
        new_log.save()

    return None

def churned_mrr_calc(df):
    temp = df
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if (df.iloc[i,j] == 0) & (df.iloc[i,j-1] != 0):
                temp.iloc[i,j] = 0                
    churned_mrr = temp.sum()
    for i in range(len(churned_mrr)):
        new_log = Metric(company_id = current_user.id, metric_name = 'churned_mrr', month = churned_mrr.index[i], value = churned_mrr[i])
        new_log.save()

    return None

def expansion_mrr_calc(df):
    temp = df
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if (df.iloc[i,j] > df.iloc[i,j-1]) & (df.iloc[i,j-1] != 0):
                temp.iloc[i,j] = df.iloc[i,j] - df.iloc[i,j-1]
            else:
                temp.iloc[i,j] = 0
    expansion_mrr = temp.sum()
    for i in range(len(expansion_mrr)):
        new_log = Metric(company_id = current_user.id, metric_name='expansion_mrr', month=expansion_mrr.index[i], value = expansion_mrr[i])
        new_log.save()

    return None

def contraction_mrr_calc(df):
    temp = df
    for i in range(len(df)):
        for j in range(1,len(df.columns)):
            if (df.iloc[i,j] < df.iloc[i,j-1]) & (df.iloc[i,j-1] != 0) & (df.iloc[i,j] != 0):
                temp.iloc[i,j] = df.iloc[i,j] - df.iloc[i,j-1]
            else:
                temp.iloc[i,j] = 0
    contraction_mrr = temp.sum()
    for i in range(len(contraction_mrr)):
        new_log = Metric(company_id = current_user.id, metric_name='contraction_mrr', month=contraction_mrr.index[i], value = contraction_mrr[i])
        new_log.save()

    return None

def revenue_metrics(data):
    df = json_to_df(data)
    mrr_calc(df)
    arr_calc(df)
    new_mrr_calc(df)
    churned_mrr_calc(df)
    expansion_mrr_calc(df)
    contraction_mrr_calc(df)

    return None

