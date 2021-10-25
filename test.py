from networkx.algorithms.dag import topological_sort


class Con():
    lifo = lambda x: [i[0] for i in x]
    lifo_del = lambda x: x.holdings[1:]

    @classmethod
    def update_road(cls, r):
       r.holdings = cls.lifo_del(r) 
    
    @classmethod
    def move_res(cls, r):
        
class Road():
    def __init__(self):
        self.holdings = ["pehder", "abbe", "emma"]
        self.take = Con.update_road
    

class Transition():

    def __init__(self, V_name, road):
        self.V_name = V_name
        self.road = road
    
    def get(self):
        self.road.take(self.road)


#r1 = Road()
#Con.update_road(r1)
r1 = Road()
farm = Transition("f1", r1)
farm.get()
farm.get()
print(r1.holdings)
