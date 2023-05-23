from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from server import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(7000 , address='192.168.1.6')
IOLoop.instance().start()