from abc import ABC, abstractmethod

# 1. SRP
class ReportBuilder:
    def build(self): return "Report Data"

class ReportSaver:
    def save(self, data): print(f"Saved: {data}")

class ReportEmailer:
    def send(self, data): print(f"Emailed: {data}")

# 2. OCP
class Shape(ABC):
    @abstractmethod
    def area(self): pass

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14 * self.r ** 2

class Square(Shape):
    def __init__(self, s): self.s = s
    def area(self): return self.s ** 2

# 3. Singleton
class AppSettings:
    _instance = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.currency = "ETB"
        return cls._instance

# 4. Factory
class Triangle(Shape):
    def __init__(self, b=3, h=4): self.b, self.h = b, h
    def area(self): return 0.5 * self.b * self.h

class ShapeFactory:
    @staticmethod
    def create(kind):
        shapes = {"circle": Circle(3), "square": Square(3), "triangle": Triangle(3, 4)}
        return shapes[kind]

# 5. Observer
class NewsAgency:
    def __init__(self): self.subs = []
    def subscribe(self, sub): self.subs.append(sub)
    def notify(self, msg): 
        for s in self.subs: s.update(msg)

class Sub1:
    def update(self, msg): print("Sub 1 received:", msg)

class Sub2:
    def update(self, msg): print("Sub 2 received:", msg)

# Execution Tests
if __name__ == "__main__":
    # 1. SRP
    r = ReportBuilder().build()
    ReportSaver().save(r)
    ReportEmailer().send(r)

    # 2. OCP
    print("Circle area:", Circle(5).area())

    # 3. Singleton
    s1, s2 = AppSettings(), AppSettings()
    print("Same instance?", s1 is s2, f"({s1.currency})")

    # 4. Factory
    shape = ShapeFactory.create("triangle")
    print("Factory created triangle area:", shape.area())

    # 5. Observer
    agency = NewsAgency()
    agency.subscribe(Sub1())
    agency.subscribe(Sub2())
    agency.notify("Breaking News!")