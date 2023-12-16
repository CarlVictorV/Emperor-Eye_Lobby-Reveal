import webbrowser


class multi_search:
    def __init__(self, nameArr):
        self.nameArr = nameArr
        self.opgg()
        self.ugg()

    def open_link(self, link):
        webbrowser.open(link)

    # Websites for multi search
    # op.gg
    # u.gg

   # The thematics of the links
        # op.gg
        # link = 'https://www.op.gg/multisearch/ph?summoners='
        # ' ' = +
        # ',' = %2C
        # '#' = %23

        # u.gg
        # link = 'https://u.gg/multisearch?summoners='
        # ' ' = %20
        # ',' can stay
        # '#' = '-'

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


class single_search:
    def __init__(self, nameArr):
        self.nameArr = nameArr

    def open_link(self, link):
        webbrowser.open(link)

    # Websites for single search
    # 'OP.GG', 'U.GG', 'TRACKER.GG', 'LEAGUE OF GRAPHS', 'LOLALYTICS', 'PORO.GG'
   # The thematics of the links
        # op.gg
        # link = 'https://www.op.gg/summoners/ph/'
        # ' ' = +
        # '#' = %23 or '-'

        # u.gg
        # link = 'https://u.gg/lol/profile/ph2/'
        # ' ' = %2
        # '#' = '-'

        # tracker.gg
        # link = 'tracker.gg/lol/profile/riot/PH/'
        # ' ' = %20
        # '#' = %23 only

        # leagueofgraphs
        # link = 'https://www.leagueofgraphs.com/summoner/ph/'
        # ' ' = +
        # '#' = %23 or '-'

        # lolalytics
        # link = 'https://xdx.gg/'
        # ' ' = +
        # '#' = -

        # Poro.gg
        # link = 'https://poro.gg/summoner/ph/'
        # ' ' = %20
        # '#' = '-'

        # porofessor.gg
        # link = 'https://porofessor.gg/live/ph/'
        # ' ' = +
        # '#' = %23 or '-'

    def opgg(self):

        self.opgg = []
        for i in self.nameArr:
            link = 'https://www.op.gg/summoners/ph/'
            link += i.replace(' ', '+').replace('#', '-')
            self.opgg.append(link)

    def ugg(self):

        self.ugg = []
        for i in self.nameArr:
            link = 'https://u.gg/lol/profile/ph2/'
            link += i.replace(' ', '%20').replace('#', '-')
            self.ugg.append(link)

    def tracker(self):

        self.tracker = []
        for i in self.nameArr:
            link = 'https://tracker.gg/lol/profile/riot/PH/'
            link += i.replace(' ', '%20').replace('#', '%23')
            self.tracker.append(link)

    def leagueofgraphs(self):

        self.leagueofgraphs = []
        for i in self.nameArr:
            link = 'https://www.leagueofgraphs.com/summoner/ph/'
            link += i.replace(' ', '+').replace('#', '-')
            self.leagueofgraphs.append(link)


    def lolalytics(self):
            
        self.lolalytics = []
        for i in self.nameArr:
            link = 'https://xdx.gg/'
            link += i.replace(' ', '+').replace('#', '-')
            self.lolalytics.append(link)

    def porogg(self):
    
        self.porogg = []
        for i in self.nameArr:
            link = 'https://poro.gg/summoner/ph/'
            link += i.replace(' ', '%20').replace('#', '-')
            self.porogg.append(link)

    


if __name__ == '__main__':
    nameArr = ['KaiserV#GOW', 'Mikado#khan',
               'AustinReaves15#AR15', 'Aim and Miss#BOBO', 'Daryl #Ligo']
    # test = multi_search(nameArr)
    # print(test.deeplolgg)

    # test = single_search(nameArr)
    # test.lolalytics()
    # print(test.lolalytics)
