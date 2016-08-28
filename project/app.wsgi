# -*- coding: utf-8 -*-
from handler.route import Router

def application(environ, start_response):
    routing = Router(environ)
    response = routing.getPage(routing.path, environ)
    start_response(routing.state, [('Content-Type', 'text/html; charset=UTF-8'),
                                   ('Set-Cookie', 'Check=MyUniqueCookie; path=/')])
    return [response]