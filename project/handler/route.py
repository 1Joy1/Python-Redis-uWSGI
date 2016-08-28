# -*- coding: utf-8 -*-

from handler import Handler
from myerror import MyError

class Router(object):


    def __init__(self, environ):

        self.path = environ.get('PATH_INFO').lstrip('/')
        self.state = '200 OK'
        self.view = Handler(environ)
        self.urlMap = {'': self.view.home,
                       '/': self.view.home,
                       'get/': self.view.get,
                       'blog/': self.view.blog,
                       'items/': self.view.items,
                       'post/': self.view.post,
                       'hello/post/': self.view.hello_post,
                       'other/': self.view.contact,
                       'send/post/': self.view.send_post,
                       'topic/': self.view.topic
                       }




    def getPage(self, path, environ):

        if (self.urlMap.get(path) is None):
            self.state = '404'
            return MyError('404 Not Found', 'Generated from application').err
        if (path == 'hello/post/' or path == 'send/post/') and environ.get('REQUEST_METHOD') != "POST":
            self.state = '405 Method Not Allowed'
            return MyError('405 Method Not Allowed', 'Generated from application').err

        response = self.urlMap.get(path)(environ)
        if not response:
            self.state = '500 Error'
            return MyError('500 Server Error', 'Generated from application').err

        return response