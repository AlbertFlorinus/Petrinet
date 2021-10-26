import networkx as nx
import random

from nx_petri import Farm, bipart_plot

B = nx.DiGraph()
class Worker():
    def __init__(self):
        self.hp = 100

class Food():
    def __init__(self):
        self.quality = random.randint(3,40)

class Product():
    def __init__(self):
        self.quality = 50

def Lifo():
    pass

def Stack():
    pass

"""
Förklaring till programmet och varför jag använde networkx.

Places, dvs Road, Storage och Barn är ej instanser av klasser jag själv har skapat.
Däremot lagras dom som noder i en instans av nx.DiGraph, vilket är en graf med riktade kanter.
När Pnet.add_road("r1", start_workers = 2) så sker följande... 
get och add definieras inte här, men är funktioner för Lifo och stack.
"""

#Pnet.add_road("r1", start_workers = 2) ->

B.add_node("r1", holdings = [Worker() for i in range(2)], color = "Road", get = Lifo, bipartite = 0)

#Pnet.add_barn("b1", start_food = 1) ->

B.add_node("b1", holdings =[Food()], color = "Barn",  get = Lifo, bipartite = 0)

#Pnet.add_storage("s1", start_products = 1) ->

B.add_node("s1", holdings = [Product()], color = "Storage", get = Stack, bipartite = 0)

"""
Road, Barn och Storage skiljer sig alltså åt i attributet color som används i transitions för att veta
vad för Place det är. get funktionen samt vilka resurser de eventuellt initieras med.

Dock är alla Places Noder i DiGraph instansen, viktigt!

Pnet.add_farm, Pnet.add_diner etc lägger också till dem som noder, med andra attribut. Varav ett
attribut (trans) är en lista som består av klassinstansen för den transitionen vi valde att skapa.
När det körs så sker följande.
"""
#Pnet.add_farm(farm_1) ->
B.add_node("farm_1", trans = [Farm("farm_1")], color = "Transition", bipartite = 1)

"""
set_inroad, set_outroad, set_outstorage etc används alla med Pnet.create_edge(u, v)

Våran graf B är riktad, så (u, v) innebär att noden u -> v

farm_1.set_inroad(r1) <-> Pnet.create_edge("r1", "farm_1")
farm_1.set_outroad(r1) <-> Pnet.create_edge("farm_1", "r1")
farm_1.set_outbarn(b1) <-> Pnet.create_edge("farm_1", "b1") 
osv...

Vad Pnet.create_edge(u, v) faktiskt gör är:
"""

B.add_edge("r1", "farm_1")
"""
grafen B har alltså information om alla kanter, användbart.
Nu lite exempel.
"""

B.add_edge("farm_1", "b1")
B.add_edge("farm_1", "r1")

places_in = B.in_degree("farm_1") #   -> 1
places_out = B.out_degree("farm_1") # -> 2

places_total = B.degree("farm_1") #   -> 3

#antal places + antal transitions = N
N = len(B)

#alla places, här använder vi attributet bipartite. alla places hade ju värdet 0.
places = {n for n, d in B.nodes(data=True) if d["bipartite"] == 0}

transitions = set(B) - places
#vilket är samma som
transitions = {n for n, d in B.nodes(data=True) if d["bipartite"] == 1}

"""
Observera att elementen i dessa set endast är vad vi valde att ha för namn när vi skapade noden.
det kan vara ett tal, eller i vårat ex en str som "r1" t.ex.
attributen är direkt funna i grafen B och nås ej enbart genom namnet för noden.
"""

#neighbors ger alla grannar
grannar = list(nx.neighbors(B, "farm_1"))

#denna lista har alltså stringen "s1", vi skapade ju aldrig en edge emellan dom!
ickegrannar = list(nx.non_neighbors(B, "farm_1"))

"""
för att få antal arbetare i vägen "r1" används:
len( B.nodes["r1"]["holdings"] )

Detta använder vi för att skapa triggers. se exempel nedan för hard_trigger()

"""

def hard_trigger(B, transition_name):
    in_places = B.in_edges(transition_name)
    for edge in in_places:
        #in_roads är [(u, "farm_1"), (u1, "farm_1")...]
        #edge[0] ger alltså vilken place som går in till farm_1
        if len( B.nodes[edge[0]]["holdings"] ) < 1:
            # En väg utan arbetare, vi kan inte använda transitionen
            return False
    return True

#Vi kan få grannmatriser, incident matriser och mycket mer.
A = nx.adjacency_matrix(B).todense()

"""
Andra Fördelar är att networkx har funktioner för att plotta graferna man skapar, och är lätt att integrera
med numpy, pandas, matplotlib och andra användbara moduler. Blir lättare att vidareutveckla tänkte jag.
"""