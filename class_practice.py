class Item:
    def __init__(self, id, name, praice, purchase_praice):
        self.id = id
        self.name = name
        self.praice = praice
        self.purchase_praice =purchase_praice
    
    def cost_rate(self) :
        rate = self.purchase_praice / self.praice
        return rate
    


item_1 = Item("A0001", "半袖クールTシャツ", 5000, 2250)
rate = item_1.cost_rate()
print(rate)