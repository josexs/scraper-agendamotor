import cfscrape
from bs4 import BeautifulSoup
import json
from unicodedata import normalize
import sys

path = sys.argv[1]
url = 'https://agendamotor.es/organizador/kdds-coches/'

class ScrapperClass(object):
    def __init__(self, name, date, site, street, locality, region, image):
        self.name = name
        self.date = date
        self.site = site
        self.street = street
        self.locality = locality
        self.region = region
        self.image = image
        self.state = False

    def dump(self):
        return {
            'name': normalizeStr(self.name),
            'date': normalizeStr(self.date),
            'site': normalizeStr(self.site),
            'address': {
                'street': normalizeStr(self.street),
                'locality': normalizeStr(self.locality),
                'region': normalizeStr(self.region),
            },
            'image': self.image,
            'state': False
        }


class DateClass(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value


def normalizeStr(str):
    a, b = 'áéíóúüñà', 'aeiouuna'
    trans = str.maketrans(a, b)
    return str.translate(trans)


scraper = cfscrape.create_scraper()
r = scraper.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
html = list(soup.children)[1]
items = soup.find_all('div', class_='type-tribe_events')

itemsArray = []
months = [
    DateClass('enero', 1),
    DateClass('febrero', 2),
    DateClass('marzo', 3),
    DateClass('abril', 4),
    DateClass('mayo', 5),
    DateClass('junio', 6),
    DateClass('julio', 7),
    DateClass('agosto', 8),
    DateClass('septiembre', 9),
    DateClass('octubre', 10),
    DateClass('noviembre', 11),
    DateClass('diciembre', 12),
]


def dateOK(date):
    for m in months:
        if m.name in date:
            dateSplit = date.split(' ')
            if (len(dateSplit) == 4):
                date = "2021-" + str(m.value) + "-" + \
                    str(dateSplit[0] + ' ' + dateSplit[3])
            else:
                date = "2021-" + str(m.value) + "-" + str(dateSplit[0])

    dateSplit = date.split('//')
    if (len(dateSplit) == 2):
        dateOK = dateSplit[0].replace("/", "-")
        dateSplitB = dateOK.split('-')
        dateOK = dateSplitB[2].strip() + '-' + \
            dateSplitB[1] + '-' + dateSplitB[0]
        if (dateOK):
            timeOK = dateSplit[1]
            date = str(dateOK).strip() + timeOK
    return date


for item in items:
    name = item.find('h3').get_text().strip()
    site = item.find(
        'div', class_='tribe-events-venue-details').get_text().strip()
    dateSc = item.find(
        'span', class_='tribe-event-date-start').get_text().strip()
    streetSc = item.find(
        'span', class_='tribe-street-address')
    localitySc = item.find(
        'span', class_='tribe-locality')
    regionSc = item.find(
        'span', class_='tribe-region')
    imageSc = item.find(
        'div', class_='tribe-events-event-image')

    date = dateOK(dateSc)
    street = ''
    locality = ''
    region = ''
    image = ''

    if (streetSc):
        street = streetSc.get_text().strip()
    if (localitySc):
        locality = localitySc.get_text().strip()
    if (regionSc):
        region = regionSc.get_text().strip()
    if (imageSc):
        image = imageSc.find('img')['data-lazy-src']
    itemsArray.append(
        ScrapperClass(name, date, site, street, locality, region, image))

with open(path + "scraper-agendamotor.json", "w", encoding='utf8') as outfile:
    jsonOK = json.dump([o.dump() for o in itemsArray], outfile)

a_file = open(path + "scraper-agendamotor.json", "r")
a_json = json.load(a_file)
pretty_json = json.dumps(a_json)
a_file.close()
print(pretty_json)
