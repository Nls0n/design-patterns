from abc import ABC, abstractmethod
import heapq

class State(ABC):
    @abstractmethod
    def next(self, order): pass

class ReadyState(State):
    def next(self, order): pass

class CookingState(State):
    def next(self, order): order.state = ReadyState()

class PendingState(State):
    def next(self, order): order.state = CookingState()

class OrderContext:
    def __init__(self):
        self.state = PendingState()
    
    def advance(self):
        self.state.next(self)

class Strategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float: pass

class NormalPricing(Strategy):
    def calculate(self, amount: float) -> float: 
        return amount

class DiscountPricing(Strategy):
    def calculate(self, amount: float) -> float: 
        return amount * 0.9

class PizzaFactory(ABC):
    @abstractmethod
    def create_dough(self): pass
    
    @abstractmethod
    def create_sauce(self): pass

class ItalianPizzaFactory(PizzaFactory):
    def create_dough(self): 
        return "Thin"
    
    def create_sauce(self): 
        return "Marinara"

class PizzaComponent(ABC):
    @abstractmethod
    def cost(self) -> float: pass

class BasePizza(PizzaComponent):
    def cost(self) -> float: 
        return 10.0

class PizzaDecorator(PizzaComponent):
    def __init__(self, pizza: PizzaComponent):
        self.pizza = pizza
        
    def cost(self) -> float: 
        return self.pizza.cost()

class CheeseDecorator(PizzaDecorator):
    def cost(self) -> float: 
        return self.pizza.cost() + 2.0

class OrderProcessor(ABC):
    def process(self):
        self.validate()
        self.pay()
        return self.generate_element()
        
    def validate(self): pass
    
    @abstractmethod
    def pay(self): pass
    
    @abstractmethod
    def generate_element(self): pass

class OnlineOrderProcessor(OrderProcessor):
    def pay(self): pass
    
    def generate_element(self): 
        return "OnlineReceipt"

class LegacyPayment:
    def make_payment(self, cents: int): 
        return True

class PaymentAdapter:
    def __init__(self, legacy: LegacyPayment):
        self.legacy = legacy
        
    def pay(self, dollars: float):
        return self.legacy.make_payment(int(dollars * 100))

class Observer(ABC):
    @abstractmethod
    def update(self, message: str): pass

class Subject:
    def __init__(self):
        self.observers = []
        
    def attach(self, obs: Observer):
        self.observers.append(obs)
        
    def notify(self, message: str):
        for obs in self.observers:
            obs.update(message)

class Command(ABC):
    @abstractmethod
    def execute(self): pass

class CookCommand(Command):
    def execute(self): 
        return "Cooking"

class MenuComponent(ABC):
    @abstractmethod
    def get_name(self): pass

class MenuItem(MenuComponent):
    def __init__(self, name):
        self.name = name
        
    def get_name(self): 
        return self.name

class MenuIterator:
    def __init__(self, items):
        self.items = items
        self.index = 0
        
    def __next__(self):
        if self.index < len(self.items):
            res = self.items[self.index]
            self.index += 1
            return res
        raise StopIteration
        
    def __iter__(self): 
        return self

class MenuCategory(MenuComponent):
    def __init__(self, name):
        self.name = name
        self.children = []
        
    def add(self, child):
        self.children.append(child)
        
    def get_name(self): 
        return self.name
        
    def __iter__(self): 
        return MenuIterator(self.children)

class RealApp:
    def render(self): 
        return "<h1>Pizzeria Client UI</h1>"

class AppProxy:
    def __init__(self):
        self.app = RealApp()
        
    def render(self, access: bool):
        if access: 
            return self.app.render()
        return "<h1>403 Forbidden</h1>"

def a_star(graph, start, goal, h):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = h.get(start, 0)
    
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
            
        for neighbor, cost in graph.get(current, {}).items():
            tentative_g = g_score[current] + cost
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + h.get(neighbor, 0)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return []