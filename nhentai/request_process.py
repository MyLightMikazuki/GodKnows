import os, requests
from nhentai.http_transfer import get_bookhttp
from nhentai.parser import Book

# 漫畫的檔案樹，用以管理下載過的檔案
class DirectoriesTree:
    def __init__(self, root_name):
        self.root_name = root_name
        self.children = dict()

        if self.root_name == None:
            self.root_name = '.'
        elif not os.path.isdir(self.root_name):
            os.mkdir(self.root_name)

        self.status_name = os.path.join(self.root_name, 'nhentai_status.txt')

        if os.path.isfile(self.status_name):
            with open(self.status_name, 'r') as f:
                while True:
                    readline = f.readline()
                    if readline == '\n':
                        continue
                    elif len(readline) == 0:
                        break
                    # 依照 'nhentai_status' 加入以下載過的漫畫
                    self.children[int(readline.strip())] = Book()

    def make_child(self, identity, text):
        if identity in self.children:
            return
        book = Book(identity)
        book.parse(text)
        if book.valid():
            # 網頁被成功解析，才加入 self.children 裡
            self.children[identity] = book

    def store_status(self, translate):
        for identity in self.children:
            book = self.children[identity]
            if not book.valid():
                continue
            book_name = '{i}'. format(i=book.identity)
            if translate:
                book_name = '{b} {p} {a}'. format(b=book.title['before'], p=book.title['pretty'], a=book.title['after'])

            dir_name = os.path.join(self.root_name, book_name)
            if not os.path.isdir(dir_name): 
                os.mkdir(dir_name)

            # 依照儲存的 http 網址下載圖片
            book.load_img(dir_name)
            book.identity = None

        with open(os.path.join(self.status_name), 'w') as f:
            for identity in self.children:
                f.write('{}\n'.format(identity))

class RequestProcess():
    def __init__(self, *args, **kwargs):
        # 建立檔案樹
        self.dir_tree = DirectoriesTree(kwargs.get('root_directory', None))

        self.start_requests(kwargs.get('identities', []))

        # 下載並紀錄檔案樹
        self.dir_tree.store_status(kwargs.get('translate', False))


    def start_requests(self, identities):
        for identity in identities:
            url=get_bookhttp(identity)
            try:
                r = requests.get(url=url)
                self.save_response(r)
            except requests.exceptions.HTTPError as e:
                print('Can not connect with {}, Error: {}'.format(url, e))

    def save_response(self, response):
        self.dir_tree.make_child(int(response.url.split('/')[-2]), response.text)
