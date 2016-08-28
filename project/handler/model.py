# -*- coding: utf-8 -*-
import time
import datetime

class Model:

    def __init__(self):
        pass

    def setArticlesEllement(self, r, data):
        try:
            id = self.translit(data['theme']) + '+' + self.translit(data['autor']) + str(int(time.time()))
            r.lpush('link_id', id)
            if r.hmset(id, {'theme': data['theme'],
                            'comment': data['comment'],
                            'autor': data['autor'],
                            'date': str(datetime.datetime.now())}):
                return id
            else:
                return False
        except:
            return False



    def getArticlesList(self, r):
        try:
            listing = r.lrange('link_id',0, -1)
            newlisting = []
            for k in listing:
                metadata = self.getArticlesContent(r, k)
                mydict = {'link': k,
                          'autor': metadata['autor'].decode('utf-8'),
                          'theme': metadata['theme'].decode('utf-8')}
                newlisting.append(mydict)
            return newlisting
        except:
            return False



    def getArticlesContent(self, r, id):
        try:
            id = id.replace(" ", "+")
            article = r.hgetall (id)
            return article
        except:
            return False



    def translit(self, string):
        """ This function works just fine """
        capital_letters = {
            u'А': u'A', u'Б': u'B', u'В': u'V', u'Г': u'G', u'Д': u'D', u'Е': u'E', u'Ё': u'E', u'Ж': u'Zh',
            u'З': u'Z', u'И': u'I', u'Й': u'Y', u'К': u'K', u'Л': u'L', u'М': u'M', u'Н': u'N', u'О': u'O',
            u'П': u'P', u'Р': u'R', u'С': u'S', u'Т': u'T', u'У': u'U', u'Ф': u'F', u'Х': u'H', u'Ц': u'Ts',
            u'Ч': u'Ch', u'Ш': u'Sh', u'Щ': u'Sch', u'Ъ': u'', u'Ы': u'Y', u'Ь': u'', u'Э': u'E', u'Ю': u'Yu',
            u'Я': u'Ya', u' ': u'+'
        }

        lower_case_letters = {
            u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd', u'е': u'e', u'ё': u'e', u'ж': u'zh',
            u'з': u'z', u'и': u'i', u'й': u'y', u'к': u'k', u'л': u'l', u'м': u'm', u'н': u'n', u'о': u'o',
            u'п': u'p', u'р': u'r', u'с': u's', u'т': u't', u'у': u'u', u'ф': u'f', u'х': u'h', u'ц': u'ts',
            u'ч': u'ch', u'ш': u'sh', u'щ': u'sch', u'ъ': u'', u'ы': u'y', u'ь': u'', u'э': u'e', u'ю': u'yu',
            u'я': u'ya'
        }

        translit_string = ""

        for index, char in enumerate(string):
            if char in lower_case_letters.keys():
                char = lower_case_letters[char]
            elif char in capital_letters.keys():
                char = capital_letters[char]
                if len(string) > index+1:
                    if string[index+1] not in lower_case_letters.keys():
                        char = char.upper()
                else:
                    char = char.upper()
            translit_string += char

        return translit_string
