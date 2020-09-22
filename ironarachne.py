import requests
from lxml import html

heraldryRoot = f'https://ironarachne.com/heraldry/'

def getHeraldryLink(seed=None, id=None):
    uri = f'{heraldryRoot}{seed}-{id}'
    page = requests.get(uri, allow_redirects=True)
    tree = html.fromstring(page.content)
    if len(tree.xpath('//div[@class="heraldry-large"]/img/@src')) > 0:
        return tree.xpath('//div[@class="heraldry-large"]/img/@src')[0]
    return None