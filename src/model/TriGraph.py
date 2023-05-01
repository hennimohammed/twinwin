import queue
from collections import namedtuple


ContractionResult = \
    namedtuple("ContractionResult", ('removed_black_neighbors', 'new_red_neighbors'))

class Node:
    def __init__(self, id) -> None:
        self.id = id 
        self.black_neighbors = set() 
        self.red_neighbors = set()
        self.is_deleted = False
        self.contraction_history : queue.LifoQueue[ContractionResult] = queue.LifoQueue() 

    def add_black_neighbor(self, neighbor):
        self.black_neighbors.add(neighbor)

    def add_red_neighbor(self, neighbor):
        self.red_neighbors.add(neighbor)

    def remove_black_neighbor(self, neighbor):
        self.black_neighbors.remove(neighbor)

    def remove_red_neighbor(self, neighbor):
        self.red_neighbors.remove(neighbor)
    
    def get_black_neighbors(self, deleted_nodes={}):
        return self.black_neighbors - deleted_nodes
    
    def get_red_neighbors(self, deleted_nodes={}):
        return self.red_neighbors - deleted_nodes
    
    def save_contraction_history(self, contraction_result: ContractionResult):
        self.contraction_history.put(contraction_result)

    def get_contraction_history(self):
        self.contraction_history.get()

class TriGraph: 

    def __init__(self, nodes: list[Node]):
        self.nodes = nodes 
        self.contractions = queue.LifoQueue(maxsize=len(nodes))
        self.deleted_nodes = set()

    def get_nodes(self):
        return [node for node in self.nodes if not node.is_deleted]

    def get_contraction_result(self, node1_id, node2_id):
        ''' 
        Calculates the result of contracting node2 into node1, 
        and returns ContractionResult(remove_black_neighbors, new_red_neighbors)
        '''

        node1_BN = self.nodes[node1_id].get_black_neighbors(self.deleted_nodes)
        node2_BN = self.nodes[node2_id].get_black_neighbors(self.deleted_nodes)

    
        remove_black_neighbors = node1_BN - node2_BN
        new_red_neighbors = remove_black_neighbors.copy()

        node1_RN = self.nodes[node1_id].get_red_neighbors(self.deleted_nodes)
        node2_RN = self.nodes[node2_id].get_red_neighbors(self.deleted_nodes)

        node2_all_neighbors = node2_BN | node2_RN
        node1_all_neighbors = node1_BN | node1_RN

        new_red_neighbors.update(node2_all_neighbors - node1_all_neighbors)

        return ContractionResult(remove_black_neighbors, new_red_neighbors)

        

    def contract_nodes(self, node1_id, node2_id):
        if node2_id < node1_id:
            node1_id, node2_id = node2_id, node1_id

        #calculate contraction result
        contraction_result = self.get_contraction_result(node1_id, node2_id)

        #deletes node2
        self.deleted_nodes.add(node2_id)

        #remove black edges from contracted node1 and neighbors
        for black_neighbor in contraction_result.removed_black_neighbors:
            self.nodes[node1_id].remove_black_neighbor(black_neighbor)
            self.nodes[black_neighbor].remove_black_neighbor(node1_id)

        #add red edges to contracted node1 and neighbors 
        for red_neighbor in contraction_result.new_red_neighbors:
            self.nodes[node1_id].add_red_neighbor(red_neighbor)
            self.nodes[red_neighbor].add_red_neighbor[node1_id]

        #save contraction_result in node1
        self.nodes[node1_id].save_contraction_history(contraction_result)
        #save contraction in queue
        self.contractions.put((node1_id, node2_id))

    def undo_contraction(self):
        #pop latest contraction from queue
        node1_id, node2_id = self.contractions.get() 

        #restore node2
        self.deleted_nodes.remove(node2_id)

        #restore contraction result
        contraction_result = self.nodes[node1_id].get_contraction_history()

        #restore removed black edges from node1 and neighbors 
        for black_neighbor in contraction_result.removed_black_neighbors:
            self.nodes[node1_id].add_black_neighbor(black_neighbor)
            self.nodes[black_neighbor].add_black_neighbor(node1_id)

        #remove red edges created in this contraction from node1 and neighbors
        for red_neighbor in contraction_result.new_red_neighbors:
            self.nodes[node1_id].remove_red_neighbor(red_neighbor)
            self.nodes[red_neighbor].remove_red_neighbor(node1_id)

        


