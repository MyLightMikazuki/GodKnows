def get_taghttp(tag, value, popular='recent', num_page=1):
    page = str()
    if num_page != 1:
        page = '?page={}'.format(num_page)

    mode = str()

    if popular == 'recent':
        popular = ''
    elif popular == 'today' or  popular == 'week':
        popular = 'popular-' + popular

    return 'https://nhentai.net/{t}/{v}/{pop}{p}'.format(t=tag, v=value, pop=popular, p=page)

def get_bookhttp(identity):
    return 'https://nhentai.net/g/{i}/'.format(i=identity)

# 轉換 https://t.nhentai.net/galleries/000000/0.jpg -> https://i.nhentai.net/galleries/000000/0.jpg
def temp_to_galleries_http(h):
    num_type = h.split('/')[-1]
    number = num_type.split('.')[0]

    # cover 是封面，和漫畫第一頁相同，thumb 是其它漫畫的捷徑
    if number == 'cover' or number == 'thumb':
        return None, None, None

    itype = num_type.split('.')[-1]

    size = len(number)
    number = int(number[0:0+size-1])

    idx = h.split('/')[-2]
    return 'https://i.nhentai.net/galleries/{i}/{n}.{t}'.format(i=idx, n=number, t=itype), number, itype
