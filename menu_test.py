__author__ = 'pavlomv'
from grab import Grab
from lxml import html
from lxml.html import clean
import json

db = None
g = Grab()
g.go('http://www.privet-bufet.ru/article/menyu-na-segodnya')
request = g.doc.select('//div[@class="panda-article"]/table[2]').html()
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

date = table.pop(0)[0]
menu = []
menu_complex = []
for i in table:
    # print(i[0])
    if i[0] == 'Комплекс':
        for j in table[table.index(i):]:
            if j[2] != '':
                # menu_complex_price = j[2].split('-')[0]
                menu_complex = dict(category=j[0], content=[], price=j[2].split('-')[0])
                continue
            menu_complex['content'].append(j[0])
        break
    if (i[1] and i[2]) == '' and i[0] != '':
        category = i[0]
        menu.append(dict(category=category, content=[]))
        continue
    elif i[0] == '':
        continue
    menu[-1]['content'].append({'name': i[0], 'weight': i[1], 'price': i[2].split('-')[0]})
with open('file.json', 'w') as file:
    file.write(json.dumps(dict(date=date, menu=menu, menu_complex=menu_complex), sort_keys=True))


