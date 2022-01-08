import os, requests
from html.parser import HTMLParser
from nhentai.http_transfer import temp_to_galleries_http

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.content = list()
        self.https = set()
        self.tags = list()
        self.not_found = False
    
    def handle_starttag(self, tag, attrs):
        out = '<start> {}'.format(tag)
        for attr in attrs:
            for val in attr:
                if val == None:
                    continue
                out += ' {}'.format(val)
                if val.find('https') >= 0:
                    self.https.add(val)

                if val.find('/parody/') == 0:
                    self.tags.append(val)
                elif val.find('/character/') == 0:
                    self.tags.append(val)
                elif val.find('/tag/') == 0:
                    self.tags.append(val)
                elif val.find('/artist/') == 0:
                    self.tags.append(val)
                elif val.find('/group/') == 0:
                    self.tags.append(val)
                elif val.find('/language/') == 0:
                    self.tags.append(val)
                elif val.find('/category/') == 0:
                    self.tags.append(val)
        self.content.append(out)
    
    def handle_endtag(self, tag):
        self.content.append('<end>')

    def handle_data(self, data):
        self.content.append(data)
        if data.find('https') >= 0:
            self.https.add(data)
        elif data.find('404 – Not Found') >= 0:
            self.not_found = True

def init_tags(tags):
    tags['parody'] = list() 
    tags['character'] = list() 
    tags['tag'] = list() 
    tags['artist'] = list() 
    tags['group'] = list() 
    tags['language'] = list() 
    tags['category'] = list()  

# 漫畫書的基本資料
class Book:
    def __init__(self, identity=None):
        self.en_title = dict()
        self.title = dict()
        self.identity = identity
        self.image_list = list()
        self.record = set()
        self.tags = dict()

        init_tags(self.tags)

    def valid(self):
        return self.identity != None

    def load_img(self, filename):
        print('Download the images to {}'.format(filename))
        for n, h, _ in self.image_list:
            with open(os.path.join(filename, n) , 'wb') as f:
                print('Download the image from {}'.format(h))
                f.write(requests.get(h).content)

    def parse(self, text):
        p = PageParser()
        p.feed(text)

        if p.not_found:
            self.identity = None
            return

        # 取得圖片的 http 鏈接
        for raw_http in p.https:
            if raw_http.find('https://t.nhentai.net/galleries/') >= 0:
                h, n, itype = temp_to_galleries_http(raw_http)
                if h != None:
                    self.image_list.append((str(n) + '.' + itype, h, n))

        self.image_list = sorted(self.image_list, key=lambda misc: int(misc[2]))

        # 取得漫畫的名稱
        idx = 0
        while idx < len(p.content):
            c = p.content[idx]
            if c == '<start> span class before':
               if not 'before' in self.en_title:
                   self.en_title['before'] = p.content[idx+1]
               else:
                   self.title['before'] = p.content[idx+1]
            elif c == '<start> span class pretty':
               if not 'pretty' in self.en_title:
                   self.en_title['pretty'] = p.content[idx+1]
               else:
                   self.title['pretty'] = p.content[idx+1]
            elif c == '<start> span class after':
               if not 'after' in self.en_title:
                   self.en_title['after'] = p.content[idx+1]
               else:
                   self.title['after'] = p.content[idx+1]
            idx += 1

        # 取得漫畫的 tags
        for tag in p.tags:
            res = tag.split('/')
            self.tags[res[1]].append(res[2])
        p.close()

class SearchPage:
    def __init__(self):
        self.curr_page = None
        self.pages = set()
        self.galleries = set()

    def parse(self, text):
        p = PageParser()
        p.feed(text)

        idx = 0
        while idx < len(p.content):
            c = p.content[idx]
            if c.find('<start> a href') == 0 and \
                   c.find('class page') >= 0:
                self.pages.add(int(p.content[idx+1]))

            if c.find('<start> a href') == 0 and \
                   c.find('class page current') >= 0:
                self.curr_page = int(p.content[idx+1])

            if c.find('<start> a href /g/') == 0:
                for t in c.split():
                    if t.find('/g/') == 0:
                        identity = int(t[3:-1])
                        self.galleries.add(identity)
            idx += 1
        p.close()
