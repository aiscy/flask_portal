__author__ = 'pavlomv'
from grab import Grab
from lxml import html
from lxml.html import clean
from lxml.html import builder as E


db = None
g = Grab()
g.go('http://www.privet-bufet.ru/article/menyu-na-segodnya')
request = g.doc.select('//div[@class="panda-article"]').html()
doc = html.document_fromstring(request)
table = []
for row in doc.cssselect("tr"):
    tds = row.cssselect("td")
    for col in tds:
        print(col.text_content())
    print('-----')

# cleaner = clean.Cleaner(style=True, remove_tags=('p', 'em'))
# doc = cleaner.clean_html(doc)
# html_new = html.tostring(E.DIV(E.TABLE(E.CLASS("table table-striped table-hover food_menu"), doc.cssselect('tbody')[-1])),
#                          encoding='unicode')
# # print(html_new)

