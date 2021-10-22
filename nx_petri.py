import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.layout import bipartite_layout
import random

# B is our bipartite graph,
# since we are always working on this graph and nothing else we make it global, easier with classes
global B
B = nx.DiGraph()

class Food():
    def __init__(self):
        self.quality = 20
        if random.randint(1,10) <= 2:
            self.quality = -40

    def get_quality(self):
        return self.quality

class Worker():
    def __init__(self):
        self.hp = 100

    def eat(self, food):
        self.hp += food.get_quality()

        if self.hp > 100:
            self.hp = 100

    def change_hp(self, delta):
        self.hp += delta
        if self.hp > 100:
            self.hp == 100

    def get_hp(self):
        return self.hp

class Product():
    def __init__(self):
        self.quality = 50
    
class Farm():
    def __init__(self, V_name):
        self.V_name = V_name
        self.accident_scale = random.randint(20,40)

    def hard_trigger(self):
        E = B.in_edges( self.V_name )
        p_test = []


        for e in E:

            if len ( B.nodes[ e[0] ]["holdings"] ) > 0:
                p_test.append(True)
            else:
                p_test.append(False)

        if len(p_test) > 0:
            return all(p_test)
        else:
            return False
    
    def fire(self):
        
        if self.hard_trigger():
            print(f"{self.V_name} fired")
            E = B.in_edges( self.V_name )
            
            transfer = {"W_x": None, "F_x": Food()}

            for e in E:
                resource = B.nodes[ e[0] ]["holdings"][0]
                if isinstance(resource, Worker):
                    transfer["W_x"] = resource
                    B.nodes[ e[0] ]["holdings"] = B.nodes[ e[0] ]["holdings"][1:]
                
            

            E_out = B.out_edges( self.V_name )
            if random.randint(1, 12) <= 3:
                transfer["W_x"].change_hp(-self.accident_scale)

            for i in E_out:

                if B.nodes[ i[1] ]["color"] == "Road" and transfer["W_x"].get_hp() > 0:
                    B.nodes[ i[1] ]["holdings"].append(transfer["W_x"])

                elif B.nodes[ i[1] ]["color"] == "Barn":
                    B.nodes[ i[1] ]["holdings"].append(transfer["F_x"])
                
        else:
            print(f"{self.V_name} fizzled")

class Diner():
    def __init__(self, V_name):
        self.V_name = V_name

    def hard_trigger(self):
        E = B.in_edges( self.V_name )
        p_test = []

        for e in E:
            #print(e, B.nodes[ e[0] ]["holdings"])
            if len ( B.nodes[ e[0] ]["holdings"] ) > 0:
                p_test.append(True)
            else:
                p_test.append(False)

        if len(p_test) > 0:
            return all(p_test)
        else:
            return False
    
    def fire(self):
        
        if self.hard_trigger():
            print(f"{self.V_name} fired")
            E = B.in_edges( self.V_name )
            
            #transfer is a temporary storage of tokens,
            #W_x stores Workers, and F_x stores Food
            transfer = {"W_x": None, "F_x": None}

            # iterates over edges (e) that points to this instance,
            # e[0] is the source Node we are retrieving Worker or Food from.
            for e in E:

                #by using the method hard_trigger, we know theres atleast 1 element in holdings.
                resource = B.nodes[ e[0] ]["holdings"][0]

                #color attribute dictates if its a Worker or Food, 
                #allows nodes to store different classes of people or nutrition, not just Workers() and Food()

                if B.nodes[ e[0] ]["color"] == "Road":
                    transfer["W_x"] = resource

                elif B.nodes[ e[0] ]["color"] == "Barn":
                    transfer["F_x"] = resource

                #pops the resource from the source Node at index 0, Barn and Road both use Que
                B.nodes[ e[0] ]["holdings"] = B.nodes[ e[0] ]["holdings"][1:]
            
            transfer["W_x"].eat(transfer["F_x"])


            E_out = B.out_edges( self.V_name )

            for e in E_out:
                
                if B.nodes[ e[1] ]["color"] == "Road":

                    #check road functionality
                    #this returns the length of the que on the outgoing road
                    wait_val = -len( B.nodes[ e[1] ]["holdings"] )
                    transfer["W_x"].change_hp( wait_val )
                    if transfer["W_x"].get_hp() > 0:
                        B.nodes[ e[1] ]["holdings"].append(transfer["W_x"])
                
        else:
            print(f"{self.V_name} fizzled")

class Factory():
    def __init__(self, V_name):
        self.V_name = V_name
        self.accident_scale = random.randint(60, 100)

    def hard_trigger(self):
        E = B.in_edges( self.V_name )
        p_test = []

        for e in E:

            if len ( B.nodes[ e[0] ]["holdings"] ) > 0:
                p_test.append(True)
            else:
                p_test.append(False)

        if len(p_test) > 0:
            return all(p_test)
        else:
            return False
    
    def fire(self):
        
        if self.hard_trigger():
            print(f"{self.V_name} fired")
            E = B.in_edges( self.V_name )
            
            transfer = {"W_x": None, "P_x": Product()}

            for e in E:
                
                resource = B.nodes[ e[0] ]["holdings"][0]
                if B.nodes[ e[0] ]["color"] == "Road":
                    transfer["W_x"] = resource
                
                B.nodes[ e[0] ]["holdings"] = B.nodes[ e[0] ]["holdings"][1:]
            

            E_out = B.out_edges( self.V_name )

            if random.randint(1,12) <= 3:
                transfer["W_x"].change_hp(-self.accident_scale)

            for i in E_out:
                    #check road functionality
                    #this returns the length of the que on the outgoing road

                if B.nodes[ i[1] ]["color"] == "Road" and transfer["W_x"].get_hp() > 0:
                    #check road functionality
                    #this returns the length of the que on the outgoing road
                    wait_val = -len( B.nodes[ i[1] ]["holdings"] )
                    transfer["W_x"].change_hp(wait_val)
                    if transfer["W_x"].get_hp() > 0:
                        B.nodes[ i[1] ]["holdings"].append(transfer["W_x"])

                elif B.nodes[ i[1] ]["color"] == "Storage":
                    B.nodes[ i[1] ]["holdings"].append(transfer["P_x"])
                
        else:
            print(f"{self.V_name} fizzled")

class House():
    def __init__(self, V_name):
        self.V_name = V_name

    def soft_trigger(self):
        E = B.in_edges( self.V_name )
        worker_check = []
        p_test = []

        if len(B.in_edges( self.V_name) ) == 2:
            for e in E:
                if B.nodes[ e[0] ]["color"] == "Road":

                    for i in B.nodes[ e[0] ]["holdings"]:
                        worker_check.append(True)
                
                elif B.nodes[ e[0] ]["color"] == "Storage":
                    if len( B.nodes[ e[0] ]["holdings"] ) > 0:
                        p_test.append(True)
                    else:
                        p_test.append(False)

        if len(B.in_edges( self.V_name) ) > 2:
            for e in E:
                if B.nodes[ e[0] ]["color"] == "Road":

                    if len ( B.nodes[ e[0] ]["holdings"] ) > 0:
                        for i in range( len ( B.nodes[ e[0] ]["holdings"] ) ):

                            worker_check.append(True)
                            
                    else:
                        worker_check.append(False)


                elif B.nodes[ e[0] ]["color"] == "Storage":

                    if len ( B.nodes[ e[0] ]["holdings"] ) > 0:
                        p_test.append(True)
                    else:
                        p_test.append(False)

        if sum(p_test) == 0:
            return False
        
        elif sum(worker_check) == 1 and sum(p_test) > 0:
            return True

        elif sum(worker_check) > 1 and sum(p_test) > 0:
            return sum(worker_check)

        else:
            return False
    
    def fire(self):

        #when only one worker is available and product exists
        if self.soft_trigger() == True:
            print(f"{self.V_name} fired with 1 worker")
            E = B.in_edges( self.V_name )
            
            #transfer is a temporary storage of tokens,
            #W_x stores Workers, and F_x stores Food
            transfer = {"W_x": None, "P_x": None}

            # iterates over edges (e) that points to this instance,
            # e[0] is the source Node we are retrieving Worker or Food from.
            for e in E:

                if len(B.nodes[ e[0 ] ]["holdings"]) > 0:
                    resource = B.nodes[ e[0] ]["holdings"][0]

                    #color attribute dictates if its a Worker or Food, 
                    #allows nodes to store different classes of people or nutrition, not just Workers() and Food()

                    if B.nodes[ e[0] ]["color"] == "Road":
                        transfer["W_x"] = resource

                    elif B.nodes[ e[0] ]["color"] == "Storage":
                        transfer["P_x"] = resource

                    #pops the resource from the source Node at index 0, Barn and Road both use Que
                    B.nodes[ e[0] ]["holdings"] = B.nodes[ e[0] ]["holdings"][1:]
            
            #increase hp or worker by 20
            transfer["W_x"].change_hp(20)


            E_out = B.out_edges( self.V_name )

            for e in E_out:
                
                if B.nodes[ e[1] ]["color"] == "Road":

                    B.nodes[ e[1] ]["holdings"].append(transfer["W_x"])

        #When there are more than 1 worker available
        elif self.soft_trigger() == False:
            print(f"{self.V_name} fizzled")
        

        #self.soft_trigger() > True
        else:

            assert self.soft_trigger() > True
            
            print(f"{self.V_name} fired with 2 workers")
            E = B.in_edges( self.V_name )
            
            #transfer is a temporary storage of tokens,
            #W_x stores Workers, and F_x stores Food
            transfer = {"W_x": [], "P_x": None}

            #helper code to check whethers theres 2 roads as source_nodes to the house or only 1
            single_road = 0
            for e in E:
                if B.nodes[ e[0] ]["color"] == "Road":
                    single_road += 1
            
            if single_road == 1:
                for e in E:

                    if B.nodes[ e[0] ]["color"] == "Road":
                        transfer["W_x"] = [ B.nodes[ e[0] ]["holdings"][0], B.nodes[ e[0] ]["holdings"][1] ]
                        B.nodes[ e[0] ]["holdings"] = B.nodes[ e[0] ]["holdings"][2:]

                    elif B.nodes[ e[0] ]["color"] == "Storage":
                        transfer["P_x"] = B.nodes[ e[0] ]["holdings"][-1]
                        #take the product from storage as a stack, ie last element
                        B.nodes[ e[0] ]["holdings"] = B.nodes[ e[0] ]["holdings"][:-1]
            
            elif single_road != 1:
                for e in E:
                    if B.nodes[ e[0] ]["color"] == "Road":

                        if len ( B.nodes[ e[0] ]["holdings"] ) > 0:
                            transfer["W_x"].append( B.nodes[ e[0] ]["holdings"][0] )

                            B.nodes[ e[0] ]["holdings"] = B.nodes[ e[0] ]["holdings"][1:]

                    elif B.nodes[ e[0] ]["color"] == "Storage":
                        transfer["P_x"] = B.nodes[ e[0] ]["holdings"][-1]
                        B.nodes[ e[0] ]["holdings"] = B.nodes[ e[0] ]["holdings"][:-1]

            
            #a new worker is created in the house
            transfer["W_x"].append(Worker())

            E_out = B.out_edges( self.V_name )


            for e in E_out:
                
                if B.nodes[ e[1] ]["color"] == "Road":
                    for worker in transfer["W_x"]:
                        B.nodes[ e[1] ]["holdings"].append(worker)

class Pnet():

    @classmethod
    def add_road(cls, node_name, start_workers = 0):
        if start_workers == 0:
            B.add_node(node_name, holdings = [], color = "Road", COLOR = 1.0, bipartite = 0)

        else:
            B.add_node(node_name, holdings = [Worker() for i in range(start_workers)], color = "Road", COLOR = 1.0, bipartite = 0)
    
    @classmethod
    def add_barn(cls, node_name, start_food = 0):
        if start_food == 0:
            B.add_node(node_name, holdings = [], color = "Barn", COLOR = 0.6, bipartite = 0)
        else:
            B.add_node(node_name, holdings = [Food() for i in range(start_food)], color = "Barn", COLOR = 0.6, bipartite = 0)

    @classmethod
    def add_storage(cls, node_name, start_products = 0):
        if start_products == 0:
            B.add_node(node_name, holdings = [], color = "Storage", COLOR = 0.4, bipartite = 0)
        else:
            B.add_node(node_name, holdings = [Product() for i in range(start_products)], color = "Storage", COLOR = 0.4, bipartite = 0)

    @classmethod
    def add_farm(cls, node_name):
        B.add_node(node_name, trans = [Farm(node_name)], color = "Transition", COLOR = 0.1, bipartite = 1)

    @classmethod
    def add_diner(cls, node_name):
        B.add_node(node_name, trans = [Diner(node_name)], color = "Transition", COLOR = 0.3, bipartite = 1)

    @classmethod
    def add_factory(cls, node_name):
        B.add_node(node_name, trans = [Factory(node_name)], color = "Transition", COLOR = 0.5,  bipartite = 1)
    
    @classmethod
    def add_house(cls, node_name):
        B.add_node(node_name, trans = [House(node_name)], color = "Transition", COLOR = 0.9,  bipartite = 1)

    @classmethod
    def create_edge(cls, u, v):
        #adds a directed edge (u, v).
        #u goes to v, not the other way around
        #u and v are existing nodes
        B.add_edge(u, v)

def simsims_ex():
    Pnet.add_road("r1", start_workers=3)
    Pnet.add_road("r2", start_workers=4)
    Pnet.add_barn("l1", start_food=5)
    Pnet.add_barn("l2", start_food=3)
    Pnet.add_storage("s1", start_products=4)

    Pnet.add_farm("farm_1")
    Pnet.create_edge("r1", "farm_1")
    Pnet.create_edge("farm_1", "l1")
    Pnet.create_edge("farm_1", "r1")

    Pnet.add_diner("diner_1")
    Pnet.create_edge("r1", "diner_1")
    Pnet.create_edge("l1", "diner_1")
    Pnet.create_edge("diner_1", "r1")

    Pnet.add_diner("diner_2")
    Pnet.create_edge("r2", "diner_2")
    Pnet.create_edge("l2", "diner_2")
    Pnet.create_edge("diner_2", "r1")

    Pnet.add_diner("diner_3")
    Pnet.create_edge("r1", "diner_3")
    Pnet.create_edge("l2", "diner_3")
    Pnet.create_edge("diner_3", "r2")

    Pnet.add_farm("farm_2")
    Pnet.create_edge("r2", "farm_2")
    Pnet.create_edge("farm_2", "l2")
    Pnet.create_edge("farm_2", "r2")

    Pnet.add_factory("factory_1")
    Pnet.create_edge("r1", "factory_1")
    Pnet.create_edge("factory_1", "s1")
    Pnet.create_edge("factory_1", "r1")

    Pnet.add_factory("factory_2")
    Pnet.create_edge("r2", "factory_2")
    Pnet.create_edge("factory_2", "s1")
    Pnet.create_edge("factory_2", "r2")

    Pnet.add_house("house_1")
    Pnet.create_edge("r1", "house_1")
    Pnet.create_edge("house_1", "r2")
    Pnet.create_edge("s1", "house_1")

    Pnet.add_house("house_2")
    Pnet.create_edge("r2", "house_2")
    Pnet.create_edge("house_2", "r1")
    Pnet.create_edge("s1", "house_2")

    Pnet.add_house("house_3")
    Pnet.create_edge("r1", "house_3")
    Pnet.create_edge("house_3", "r1")
    Pnet.create_edge("s1", "house_3")

    Pnet.add_house("house_4")
    Pnet.create_edge("r2", "house_4")
    Pnet.create_edge("house_4", "r2")
    Pnet.create_edge("s1", "house_4")

def colab_plot_detail():
    #fore plotting colab/jupyter etc
    places = {n for n, d in B.nodes(data=True) if d["bipartite"] == 0}
    transitions = set(B) - places

    val3_map = {node: float(B.nodes[node]["COLOR"]) for node in places}
    values3 = [val3_map.get(node, 0.25) for node in places]

    nx.draw_networkx_nodes(B, pos = nx.kamada_kawai_layout(B), nodelist = list(places), cmap=plt.get_cmap("viridis"), node_color=values3)

    val4_map = {node: float(B.nodes[node]["COLOR"]) for node in transitions}
    values4 = [val4_map.get(node, 0.25) for node in transitions]

    nx.draw_networkx_nodes(B, pos = nx.kamada_kawai_layout(B), nodelist = list(transitions), cmap=plt.get_cmap("viridis"), node_color=values4, node_shape="s", node_size=80)

    leaver_edges = set(list(B.in_edges(places)))
    comer_edges = set(list(B.in_edges(transitions)))

        
    flipped = set( (i[1],i[0]) for i in leaver_edges )

    common = flipped.intersection(comer_edges)
    common = common.union(set( ( i[1], i[0] ) for i in common))


    leaver_edges = leaver_edges.difference(common)
    comer_edges = comer_edges.difference(common)

    nx.draw_networkx_labels(B, pos = nx.kamada_kawai_layout(B), font_size=8)

    nx.draw_networkx_edges(B, pos = nx.kamada_kawai_layout(B), edgelist = common, edge_color="g" ,arrowsize=12)
    nx.draw_networkx_edges(B, pos = nx.kamada_kawai_layout(B), edgelist = leaver_edges, edge_color="b", arrowsize=8)
    nx.draw_networkx_edges(B, pos = nx.kamada_kawai_layout(B), edgelist = comer_edges, edge_color="r", arrowsize=8)

def deterministic(order):

    #helper code to determine whether to end the simulation
    places = {n for n, d in B.nodes(data=True) if d["bipartite"] == 0}

    roads_places = {i for i in places if B.nodes(data = True)[i]["color"] == "Road"}
    c0 = 0

    for i in order:
        c0 += 1
        p0 = [len( B.nodes[i]["holdings"] ) for i in roads_places]
        #if 0 in p0:
        if all(v == 0 for v in p0):
            #all(v == 0 for v in values)
            print(p0)
            print(B.nodes(data=True))
            print(f"simulation ended at {c0} iterations. ")
            break

        
        B.nodes[i]["trans"][0].fire()

def stochastic_iteration(n):
    #of n iterations
    orig_state = list(f"{n}: {len(d['holdings'])} " for n, d in B.nodes(data=True) if d["bipartite"] == 0)
    #takes only the transition nodes, ie bipartite = 1
    transit_lst = [t for t in B.nodes if B.nodes[t]["bipartite"] == 1]
    sequence = [random.choice(transit_lst) for i in range(n)]
    #calls the "deterministic funtion, whats random here is merely the sequence to simulate"
    deterministic(sequence)

    new_state = list(f"{n}: {len(d['holdings'])} " for n, d in B.nodes(data=True) if d["bipartite"] == 0)
    print("\n \n --------")
    print(f"name: amount of tokens")

    for i, j in zip(orig_state, new_state):
        print(i, "-->", j)

def colab_simple():
    val_map ={node: float(B.nodes[node]["COLOR"]) for node in B.nodes() }
    values = [val_map.get(node, 0.25) for node in B.nodes()]
    nx.draw(B,pos = nx.kamada_kawai_layout(B), arrows=True,cmap=plt.get_cmap("viridis"), node_color = values, with_labels = True)

def bipart_plot():
    places = {n for n, d in B.nodes(data=True) if d["bipartite"] == 0}
    val_map ={node: float(B.nodes[node]["COLOR"]) for node in B.nodes() }    
    values = [val_map.get(node, 0.25) for node in B.nodes()]
    nx.draw_networkx(B, pos = bipartite_layout(B, places), node_color = values, width = 1)
