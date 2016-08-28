# -*- coding: utf-8 -*-
from cgi import parse_qs, escape
from jinja2 import Environment, FileSystemLoader
import os
import redis
from model import Model

class Handler:

    def __init__(self, environ):
        self.state = '200 OK'
        self.counter = self.getCounter(environ)




    def blog(self, environ, counter=0):
        try:
            template = self.get_file_template('mainboot.html')
            inclData = { 'title': 'Blog',
                         'title2': u'Блог - Форма отправки',
                         'counter': self.counter }
            inclContent = { 'params': inclData }
            return template.render(inclContent).encode('utf-8')
        except:
            return False




    def items(self, environ, counter=0):
        try:
            template = self.get_file_template('mainboot.html')

            articlesList = Model().getArticlesList(redis.StrictRedis(host='localhost', port=6379, db=0))


            inclData = {'title': 'Items',
                        'title2': u'Статьи',
                        'host': environ['HTTP_HOST'],
                        'articlesList': articlesList,
                        'textlink': '/topic/?id=',
                        'counter': self.counter
                        }
            inclContent = { 'params': inclData }
            #return str(articlesList)
            return template.render(inclContent).encode('utf-8')
        except:
            return False





    def send_post(self, environ, counter=0):
        try:
            template = self.get_file_template('mainboot.html')

            try:
                request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            except (ValueError):
                request_body_size = 0
            request_body = environ['wsgi.input'].read(request_body_size)
            query = parse_qs(request_body)

            for key in query:
                query[key] = ', '.join(query[key]).decode('utf-8')

            savedEll = Model().setArticlesEllement(redis.StrictRedis(host='localhost', port=6379, db=0), query)

            if savedEll:
                inclData = {'title': 'Successfully',
                            'title2': u'Статья сохранена',
                            'counter': self.counter,
                            'link': '/../topic/?id=' + savedEll,
                            'textlink': environ['HTTP_HOST'] + '/topic/?id=' + savedEll
                            }
            else:
                inclData = {'title': 'Fail',
                            'title2': u'Ошибка, статья не сохранена',
                            'css': '../../static/form.css',
                            'counter': self.counter
                            }

            inclContent = { 'params': inclData }
            return template.render(inclContent).encode('utf-8')
        except:
            return False




    def topic(self, environ, counter=0):
        try:
            template = self.get_file_template('mainboot.html')
            query =  parse_qs(environ['QUERY_STRING'])
            for key in query:
                query[key] = ', '.join(query[key]).decode('utf-8')

            article = Model().getArticlesContent(redis.StrictRedis(host='localhost', port=6379, db=0), query['id'])

            inclData = {'title': 'Article',
                        'title2': article['theme'].decode('utf-8'),
                        'comment': article['comment'].decode('utf-8'),
                        'autor': article['autor'].decode('utf-8'),
                        'date': article['date'].split('.')[0].decode('utf-8'),
                        'counter': self.counter
                        }

            inclContent = { 'params': inclData }
            return template.render(inclContent).encode('utf-8')
        except:
            return False




#****************Часть предыдущего задания с исправленными замечаниями***********************
#********************************************************************************************

    def getCounter(self, environ):
        try:
            r = redis.StrictRedis(host='localhost', port=6379, db=0)
        except:
            return False
        counter = r.get('counter')
        if not counter:
            counter = r.set('counter', 1)
        if not counter:
            return "No Avalable"
        if environ.get('HTTP_COOKIE') != 'Check=MyUniqueCookie':
            counter = int(counter) + 1
            r.set('counter', counter)
        return int(counter)




    def home(self, environ, counter=0):
        try:
            template = self.get_file_template('mainboot.html')

            for key in environ:
                environ[key] = escape(str(environ[key]))

            inclData = {'title': 'Main',
                        'title2': u'Главная',
                        'table': environ,
                        'counter': self.counter
                        }
            inclContent = { 'params': inclData }
            return template.render(inclContent).encode('utf-8')
        except:
            return False




    def get(self, environ, counter=0):
        try:
            template = self.get_file_template('mainboot.html')
            query =  parse_qs(environ['QUERY_STRING'])

            for key in query:
                query[key] = ', '.join(query[key]).decode('utf-8')

            inclData = {'title': 'GET req',
                        'title2': u'GET запрос с параметрами',
                        'table': query,
                        'counter': self.counter
                        }
            inclContent = { 'params': inclData }
            return template.render(inclContent).encode('utf-8')
        except:
            return False




    def post(self, environ, counter=0):
        try:
            template = self.get_file_template('mainboot.html')
            inclData = { 'title': 'Form',
                         'title2': u'Форма POST запроса',
                         'counter': self.counter }
            inclContent = { 'params': inclData }
            return template.render(inclContent).encode('utf-8')
        except:
            return False




    def hello_post(self, environ, counter=0):
        try:
            template = self.get_file_template('mainboot.html')
            try:
                request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            except (ValueError):
                request_body_size = 0
            request_body = environ['wsgi.input'].read(request_body_size)
            query = parse_qs(request_body)

            for key in query:
                query[key] = ', '.join(query[key]).decode('utf-8')

            inclData = {'title': 'POST req',
                        'title2': u'POST ответ',
                        'table': query,
                        'counter': self.counter
                        }
            inclContent = { 'params': inclData }
            return template.render(inclContent).encode('utf-8')
        except:
            return False




    def contact(self, environ, counter=0):
        try:
            template = self.get_file_template('mainboot.html')

            table =  "'\n'.join(result)"
            inclData = {'title': 'Other',
                        'title2': u'Разное (переменные окружения ОС сервера)',
                        'text': str(dict(os.environ.items())),
                        'counter': self.counter
                        }

            inclContent = { 'params': inclData }
            #return str(dict(os.environ.items()))
            return template.render(inclContent).encode('utf-8')
        except:
            return False




    def get_file_template(self, file_template):
        #template_dir = '{}/templates'.format(os.path.dirname(os.path.abspath(__file__)))
        template_dir = '{}/templates'.format(os.path.abspath(os.curdir))
        env = Environment(loader=FileSystemLoader(template_dir))
        return env.get_template(file_template)