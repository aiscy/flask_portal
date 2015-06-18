__author__ = 'pavlomv'
from grab import Grab
from lxml import html
from lxml.html import clean
from lxml.html import builder as E
import re
import collections
import json

db = None
g = Grab()
g.go('http://www.privet-bufet.ru/article/menyu-na-segodnya')
request = g.doc.select('//div[@class="panda-article"]').html()
doc = html.document_fromstring(request)

cleaner = clean.Cleaner(style=True, remove_tags=['p', 'em'])
doc = cleaner.clean_html(doc)
table = []
for row in doc.cssselect("tr"):
    tds = row.cssselect("td")
    table.append([tds[0].text_content(), tds[1].text_content(), tds[2].text_content()])
for i in table:
    for j in i:
        k = i.index(j)
        i.remove(j)
        i.insert(k, ' '.join(j.split()))
# print(table)

# menu = collections.OrderedDict(category='',
#                 name='',
#                 weight='',
#                 price='')
# menu = collections.OrderedDict()
menu = []
print(menu)
category = None
date = table.pop(0)[0]
for i in table:
    # print(i[0], i[1], i[2])
    if (i[1] and i[2]) == '' and i[0] != '':
        category = i[0]
        menu.append(dict(category=category, content=[]))
        # print(menu)
        continue
        # print(category)
    menu[-1]['content'].append({'name': i[0], 'weight': i[1], 'price': i[2].split('-')[0]})
    print(menu)
    # menu.append(['category'] = {'name': i[0], 'weight': i[1], 'price': i[2].split('-')[0]})
    # menu.append(collections.OrderedDict(category=category,
    #                                     content=[{'name': i[0], 'weight': i[1], 'price': i[2].split('-')[0]}]))
    # menu[category] = [{'name': i[0], 'weight': i[1], 'price': i[2].split('-')[0]}]



# print(menu)


to_json = collections.OrderedDict(
    date=date,
    menu=menu)
# print(to_json)
#
with open('file.json', 'w') as file:
    file.write(json.dumps(to_json, sort_keys=True))



        # element[table.index(item)] = ' '.join(element.split())
        # ' '.join(element.split()
# print(table)

