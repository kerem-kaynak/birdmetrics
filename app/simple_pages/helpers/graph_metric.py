from sqlalchemy import values
from app.authentication.models import Metric
import plotly.graph_objects as go
import plotly
from markupsafe import Markup

def graph_metric(metric, user_id):
    metrics = Metric.query.filter_by(metric_name=metric, company_id=user_id).order_by(Metric.month).all()
    dates = [record.month for record in metrics]
    values = [record.value for record in metrics]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=values, fill='tozeroy', line_color = '#6DB661'))
    fig.update_xaxes(dtick="M1", tickformat="%b\n%Y")
    fig.update_layout(plot_bgcolor = 'rgba(0,0,0,0)')
    graph =  plotly.io.to_html(fig)
    return Markup(graph)