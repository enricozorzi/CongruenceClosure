from itertools import product


class CC_DAG:
    def __init__(self):
        self.nodes = {}
        self.equalities = []
        self.inequalities = []

    def add_node(self, id, fn, args, find, ccpar):
        self.nodes[id] = {
            "fn": fn,
            "args": args,
            "find": find,
            "ccpar": ccpar,
        }

    def NODE(self, node_id):
        return self.nodes[node_id]

    def find(self, id):
        if self.NODE(id)["find"] == id:
            return id
        else:
            return self.find(self.NODE(id)["find"])

    def union(self, id1, id2):
        n1 = self.NODE(self.find(id1))
        n2 = self.NODE(self.find(id2))
        n1["find"] = n2["find"]
        n2["ccpar"].update(n1["ccpar"])
        n1["ccpar"] = set()

    def ccpar(self, id):
        result = self.NODE(self.find(id))
        return result["ccpar"]

    def congruent(self, id1, id2):
        n1 = self.NODE(id1)
        n2 = self.NODE(id2)
        if (n1["fn"] is not n2["fn"]) or (len(n1["args"]) != len(n2["args"])):
            return False
        for i in range(len(n1["args"])):
            val1 = self.find(n1["args"][i])
            val2 = self.find(n2["args"][i])
            if val1 != val2:
                return False
        return True

    def merge(self, id1, id2):
        a1 = self.find(id1)
        a2 = self.find(id2)
        if a1 != a2:
            pi1 = self.ccpar(id1)
            pi2 = self.ccpar(id2)
            self.union(id1, id2)
            for t1, t2 in product(pi1, pi2):
                if self.find(t1) != self.find(t2) and self.congruent(t1, t2):
                    node1 = self.NODE(t1)
                    node2 = self.NODE(t2)
                    self.merge(node1, node2)
            return True
        else:
            return False

    def solve(self):
        forbiddenMerges = set()

        for pair in self.inequalities:
            firstId, secondId = pair
            forbiddenMerges.add((firstId, secondId))

        for pair in self.equalities:
            firstId, secondId = pair
            if (firstId, secondId) in forbiddenMerges:
                return "UNSAT"
            self.merge(firstId, secondId)
    
        for pair in self.inequalities:
            firstId, secondId = pair
            forbiddenMerges.add((firstId, secondId))
            if self.find(firstId) == self.find(secondId):
                return "UNSAT"
            
        return "SAT"
        
