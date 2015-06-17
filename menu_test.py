__author__ = 'pavlomv'
from grab import Grab
from lxml import html
from lxml.html import clean
from lxml.html import builder as E
import re

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
for item in table:
    print(item)
    # for element in item:
        # print(' '.join(element.split()))

