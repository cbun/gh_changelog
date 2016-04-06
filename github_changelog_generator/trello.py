import trolly
import re

class TrelloScraper():
    def __init__(self, key, secret, boards=None):
        self.client = trolly.client.Client(key, secret)
        self.cards = []
        for board in boards:
            self.cards += self.client.get_board(board).get_cards()
        self.tag_urls = _get_tag_urls(self.cards)

def _find_tag(name):
    m = re.search(r'\[(.*?)\]', name)
    if m:
        return m.group(0)

def get_tag_urls(cards):
    urls = {}
    for card in cards:
        info = card.data
        tag = _find_tag(info['name'])
        if tag and not urls.get(tag): # Don't overwrite
            urls[tag] = info['shortUrl']
    return urls

# TODO move to yaml
master_board = '55add76bc1f0878b7c30fc9a'
