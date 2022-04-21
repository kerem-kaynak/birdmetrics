from app.app import create_app
from app.simple_pages.helpers.graph_metric import graph_metric

app = create_app()

app.add_template_global(graph_metric, name='graph_metric')

if __name__ == '__main__':
  app.run(debug=True)