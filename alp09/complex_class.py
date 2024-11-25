class Complex:
    def __init__ (self, r, i):
        self.r = r
        self.i = i
    def print(self):
        print(self.r, self.i, "j")
    def add(self, c):
        self.r += c.r
        self.i += c.i

c = Complex(30, 6)
d = Complex(5, -1)
c.add(d)
c.print()
