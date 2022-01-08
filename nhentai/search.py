from nhentai.parser import SearchPage, Book, init_tags

class SearchSettings:
    def __init__(self):
        self.hard_tags = dict()
        self.soft_tags = dict()
        self.restrict_tags = dict()
        self.max_pages_range = [1]
        self.popular = 'recent'

        init_tags(self.soft_tags)
        init_tags(self.soft_tags)
        init_tags(self.soft_tags)

    def gather_tags_from_book(book):
        for t in book.tags:
            self.soft_tags[t].extend(book.tags[t])

class Node:
    def __init__(self, tag, value):
        self.children = dict()
        self.tag = tag
        self.value = value

class SearchTree:
    def __init__(self, settings):
        self.root_node = Node(None, None)
        self.settings = settings
