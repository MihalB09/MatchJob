class Cart:

    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

if __name__ == "__main__":
    c = Cart()
    c.add('Strawberry')
    print(c.items)
