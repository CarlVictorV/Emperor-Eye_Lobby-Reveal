import webbrowser


class multi_search:
    def __init__(self, nameArr):
        self.nameArr = nameArr

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


if __name__ == '__main__':
    nameArr = ['KaiserV#GOW', 'Mikado#khan',
               'AustinReaves15#AR15', 'Aim and Miss#BOBO']
    multi_search(nameArr)
