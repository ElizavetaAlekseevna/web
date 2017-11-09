from wsgiref import simple_server, validate

includes = [
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
	    
class WsgiTopBottomMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):       
    
            css = ""
            js = ""
            for i in includes:
                if(i.split('.')[1] == 'css'):
                    css += '<link rel="stylesheet" href="/_static/' + i + '"/>\n'
                else:
                    js += '<script src="/_static/' + i + '"></script>\n'
	    
            response = self.app(environ, start_response).decode() 
            if response.find('<head>') > -1:
                data, headend = response.split('</head>')
                response = data + css + '</head>' + headend
            if response.find('<body>') > -1:
                data, htmlend = response.split('</body>')
                response = data + js +'</body>' + htmlend
            return (response).encode()  
	    

def app(environ, start_response):
    addr = environ['PATH_INFO']
    path = '.' + addr  
    file = open(path, 'r')
    fileread = file.read()
    file.close()

    response_code = '200 OK'
    response_type = ('Content-Type', 'text/HTML')
    start_response(response_code, [response_type])
    return fileread

# Оборачиваем WSGI приложение в middleware
app = WsgiTopBottomMiddleware(app)


# Запускаем сервер
from wsgirev serve(app, host='localhost', port=8000)
