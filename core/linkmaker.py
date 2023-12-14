import webbrowser


class multi_search:
    def __init__(self, nameArr):
        self.nameArr = nameArr
        self.opgg()
        self.ugg()
        # self.deeplolgg()


    def open_link(self, link):
        webbrowser.open(link)

    # Websites for multi search
        # op.gg
        # u.gg
        # deeplol.gg

   # The thematics of the links
        # op.gg
        # ' ' = +
        # ',' = %2C
        # '#' = %23

        # u.gg
        # ' ' = %20
        # ',' can stay
        # '#' = '-'

        # deeplol.gg
        # ' ' = %20
        # ',' = %2C
        # '#' = %23

   # TODO: Implement the multi search
    
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

    # PH seems to be broken
    # def deeplolgg(self):
    #     link = 'https://www.deeplol.gg/multi/PH/'
    #     for i in self.nameArr:
    #         link += i.replace(' ', '%20').replace(',', '%2C').replace('#', '%23')
    #         link += '%2C'
    #     self.deeplolgg = link




if __name__ == '__main__':
    nameArr = ['KaiserV#GOW', 'Mikado#khan',
               'AustinReaves15#AR15', 'Aim and Miss#BOBO', 'Daryl #Ligo']
    test = multi_search(nameArr)
    print(test.deeplolgg)