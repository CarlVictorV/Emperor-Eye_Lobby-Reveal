import webbrowser


class multi_search:
    def __init__(self, nameArr):
        self.nameArr = nameArr
        self.opgg()
        self.ugg()

    def open_link(self, link):
        webbrowser.open(link)
    
    def opgg(self):
        link = 'https://www.op.gg/multisearch/ph?summoners='
        for i in self.nameArr:
            link += i.replace(' ', '+').replace(',', '%2C').replace('#', '%23')
            link += '%2C'
        self.opgg = link

    def ugg(self):
        link = 'https://u.gg/multisearch?summoners='
        for i in self.nameArr:
            link += i.replace(' ', '%20').replace('#', '-')
            link += ','
        link += '&region=ph2'
        self.ugg = link


if __name__ == '__main__':
    nameArr = []
    test = multi_search(nameArr)