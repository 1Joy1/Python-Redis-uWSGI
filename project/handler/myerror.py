class MyError(Exception):
    def __init__(self, text, text2):
        MyError.txt = text

        self.err = ('<html><head><title>' + text + '</title></head>'
                   '<body bgcolor="white">'
                   '<center><h1>' + text + '</h1></center><hr><center>'+ text2 +'</center>'
                   '</body></html>')