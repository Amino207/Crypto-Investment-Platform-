# assets.py
class Assets:
    #constructing objects
    def __init__(self, name, current_price):
        #assigning asset name and price attributes
        self.name = name
        self.current_price = float(current_price)

    def __str__(self):
        return f'{self.name}: ${self.current_price}'


    #constructing view_assets method
    def get_name(self):
        return self.name
    def get_current_price(self):
        return self.current_price







