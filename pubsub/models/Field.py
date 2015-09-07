__author__ = 'fritz'
class Field():
    def __init__(self, size, name, rtl, order, font, sticky):
        self.size = int(size)
        self.name = str(name)
        self.rtl = bool(rtl)
        self.order = int(order)
        self.font = str(font)
        self.sticky = bool(sticky)