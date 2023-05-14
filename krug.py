class Krug():
    
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def stampaj(self):
        print("(" + str(self.x) + "," + str(self.y)+ ")")

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

x = Krug(2, 3)
x.stampaj()