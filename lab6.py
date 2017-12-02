from pyramid.config import Configurator
from pyramid.response import Response
from wsgiref.simple_server import make_server
from webob import Request, Response
from jinja2 import Environment, FileSystemLoader

assets = [
    'app.js',
    'react.js',
    'leaflet.js',
    'D3.js',
    'moment.js',
    'math.js',
    'main.css',
    'bootstrap.css',
    'normalize.css',
    ]
js = []
css = []

for item in assets:
        itemspl = item.split('.')
        if itemspl[1] == 'js':
            js.append(item)
        elif itemspl[1] == 'css':
            css.append(item)
           
class WsgiTopBottomMiddleware(object):
  def __init__(self, app):
    self.app = app
    
def __call__(self, environ, start_response):
      response = self.app(environ, start_response).decode() 
      if response.find('<head>' and '<body>') > -1:
              start, head = response.split('<head>')
              data1, body1 = head.split('</head>')
              end, body2 = body1.split('<body>')
              data2, htmlend = body2.split('</body>')
                       
      yield (start + data + htmlend).encode() 
   else:
      yield (response).encode() 

def index(request):
  env = Environment(loader=FileSystemLoader('.'))
  template = env.get_template('/index.html')
  return Response(template.render(javascripts=js, styles=css))

def about(request):
  env = Environment(loader=FileSystemLoader('.'))
  template = env.get_template('/about/aboutme.html')
  return Response(template.render(javascripts=js, styles=css))

if __name__ == '__main__':
  config = Configurator() 
  config.add_route('index', '/')
  config.add_view(index, route_name='index')
  config.add_route('about', '/about')
  config.add_view(about, route_name='about')
  app = config.make_wsgi_app()
  httpd=make_server('0.0.0.0', 8000, app)
  httpd.serve_forever()
