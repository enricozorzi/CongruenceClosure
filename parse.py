import re
from cc_dag import *
from itertools import product
import random
from matplotlib import pyplot as plt
from pysmt.smtlib.parser import SmtLibParser
from pysmt.rewritings import CNFizer 
import re
from itertools import product
import networkx as nx


def parsing(F,a):
    list_node=[]
    for i in re.split(" and ",F):
        if "!=" in i:
            a.inequalities.append(i.split(" != "))
        else:
            a.equalities.append(i.split(" = "))
            
    for eq in a.equalities:
        for node in eq:
            if node not in list_node:
                visit(node,list_node)
                rec(node,list_node)

    for ineq in a.inequalities:
        for node in ineq:
            if node not in list_node:
                visit(node,list_node)
                rec(node,list_node)
    return list_node,a


def visit(node,list_node):
    if node not in list_node:
        list_node.append(node)
        return list_node
    return list_node

def rec(node, list_node):
    if re.search('^(\w*\d*\()', node) and node.endswith(")"):
        node = node[node.index("(") + 1:-1]
        temp = node.replace(" ", "")
        functions = re.findall(r'\w*\([^()]+\)', node)
        for function in functions:
            escaped_sub_string = re.escape(function)
            pattern = re.compile(escaped_sub_string + ',?')
            node = re.sub(pattern, "", node)

        if re.search('^(\w*\d*\()', node) and node.endswith(")"):
            visit(temp, list_node)
            return rec(temp, list_node)

        new_list = functions + [ele.strip() for ele in node.split(",") if ele != ''and ele != ' ']
        if len(new_list) > 1:
            while ','.join(new_list) != temp:
                random.shuffle(new_list)
        for i in new_list:
            visit(i, list_node)
            rec(i, list_node)
    return list_node


def create_graph(a,list_node):
    list_node = sorted(list_node, key=len,  reverse=True)
    ccpar= set()
    for i in list_node:
        args=[]
        if re.search('^(\w*\d*\()', i) and i.endswith(")"):
            list = []
            list = rec(i,list)

            for node in list:
                args.append(list_node.index(node)+1)
            a.add_node(list_node.index(i)+1, i, args,list_node.index(list[0])+1 , set())

    for i in list_node:
        ccpar= set()
        if not re.search('^(\w*\d*\()', i) and not i.endswith(")"):
            for n in a.nodes:
                if list_node.index(i)+1 in a.nodes[n]["args"]:
                    ccpar.add(n)
            a.add_node(list_node.index(i)+1, i, [], list_node.index(i)+1, ccpar)
            
    return list_node,a
    
def update_eq_ineq(eq,ineq,list_node):
    list_node = sorted(list_node, key=len,  reverse=True)
    for i in range(len(eq)):
        for node in range(len(eq[i])):
            eq[i][node]=list_node.index(eq[i][node])+1
    for i in range(len(ineq)):
        for node in range(len(ineq[i])):
            ineq[i][node]=list_node.index(ineq[i][node])+1
    return eq,ineq


def traduceString(F):
    if F.startswith("(") and F.endswith(")"):
        F = F[1:-1]
    F=F.replace("&","and")
    for i in re.split(" and ",F):
        temp = i
        if i.startswith("(") and i.endswith(")"): i = i[1:-1]
        if "!" in i:
            i = i[3:-1]
            i= i.replace("=","!=")
        F = F.replace(temp,i)
    return F

def visualize_dag(dag):
        G = nx.DiGraph()

        # Add nodes to the graph
        for node in dag.nodes:
            G.add_node(node)

        # Add edges to the graph
        for node in dag.nodes:
            for child_id in dag.nodes[node]["ccpar"]:
                G.add_edge(child_id, node)

        # Create a dictionary to store node labels
        labels = {node: f"{dag.nodes[node]['fn']} (ID: {node})" for node in dag.nodes}

        # Draw the graph
        pos = nx.circular_layout(G)
        nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue', node_size=500, font_size=10, arrows=True)
        plt.show()