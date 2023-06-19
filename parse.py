import re
import random
import networkx as nx
from matplotlib import pyplot as plt
from cc_dag import *

def parse_formula(formula, dag):
    nodes = []
    for sub_formula in re.split("and|&", formula):
        sub_formula = sub_formula.replace(" ", "")
        if "!=" in sub_formula:
            dag.inequalities.append(sub_formula.split("!="))
        else:
            dag.equalities.append(sub_formula.split("="))
    
    for eq in dag.equalities:
        for node in eq:
            if node not in nodes:
                visit(node, nodes)
                recursive_visit(node, nodes)
    
    for ineq in dag.inequalities:
        for node in ineq:
            if node not in nodes:
                visit(node, nodes)
                recursive_visit(node, nodes)
    
    return nodes, dag

def visit(node, nodes):
    if node not in nodes:
        nodes.append(node)
    return nodes




def recursive_visit(node, nodes):
    if re.search('^(\w*\d*\()', node) and node.endswith(")"):
        node = node[node.index("(") + 1:-1]
        temp = node.replace(" ", "")
        functions = re.findall(r'\w*\([^()]+\)', node)
        for function in functions:
            escaped_sub_string = re.escape(function)
            pattern = re.compile(escaped_sub_string + ',?')
            node = re.sub(pattern, "", node)

        if re.search('^(\w*\d*\()', node) and node.endswith(")"):
            visit(temp, nodes)
            return recursive_visit(temp, nodes)

        new_list = functions + [ele.strip() for ele in node.split(",") if ele != '' and ele != ' ']
        if len(new_list) > 1:
            while ','.join(new_list) != temp:
                random.shuffle(new_list)
        
        for i in new_list:
            visit(i, nodes)
            recursive_visit(i, nodes)
        else:
            return new_list
    
    return nodes

def sub_visit(node, nodes):
    if re.search('^(\w*\d*\()', node) and node.endswith(")"):
        node = node[node.index("(") + 1:-1]
        temp = node.replace(" ", "")
        functions = re.findall('\w*\(*[^()]+\)+', node)
        for function in functions:
            escaped_sub_string = re.escape(function)
            pattern = re.compile(escaped_sub_string + ',?')
            node = re.sub(pattern, "", node)

        if re.search('^(\w*\d*\()', node) and node.endswith(")"):
            visit(temp, nodes)
            return recursive_visit(temp, nodes)

        new_list = functions + [ele.strip() for ele in node.split(",") if ele != '' and ele != ' ']
        if len(new_list) > 1:
            while ','.join(new_list) != temp:
                random.shuffle(new_list)
    return new_list


def create_graph(dag, nodes):
    nodes = sorted(nodes, key=len, reverse=True)
    ccpar_set = set()
    for node in nodes:
        args = []
        if re.search('^(\w*\d*\()', node) and node.endswith(")"):
            sub_nodes = []
            sub_nodes = sub_visit(node, sub_nodes)

            for sub_node in sub_nodes:
                args.append(nodes.index(sub_node) + 1)
            
            dag.add_node(nodes.index(node) + 1, node, args, nodes.index(node) + 1, set())
    
    for node in nodes:
        ccpar_set = set()
        if not re.search('^(\w*\d*\()', node) and not node.endswith(")"):
            for n in dag.nodes:
                if nodes.index(node) + 1 in dag.nodes[n]["args"]:
                    ccpar_set.add(n)
            dag.add_node(nodes.index(node) + 1, node, [], nodes.index(node) + 1, ccpar_set)

    for node in nodes:
        ccpar_set = set()
        for n in dag.nodes:
            if nodes.index(node) + 1 in dag.nodes[n]["args"]:
                ccpar_set.add(n)
        dag.add_node(nodes.index(node) + 1, node,dag.nodes[nodes.index(node) + 1]['args'] , dag.nodes[nodes.index(node) + 1]['find'], ccpar_set)
    
    return nodes, dag

def update_eq_ineq(equalities, inequalities, nodes):
    nodes = sorted(nodes, key=len, reverse=True)
    for i in range(len(equalities)):
        for node in range(len(equalities[i])):
            equalities[i][node] = nodes.index(equalities[i][node]) + 1
    
    for i in range(len(inequalities)):
        for node in range(len(inequalities[i])):
            inequalities[i][node] = nodes.index(inequalities[i][node]) + 1
    return equalities, inequalities

def translate_string(formula):
    if formula.startswith("(") and formula.endswith(")"):
        formula = formula[1:-1]
    formula = formula.replace("&", "and")
    for sub_formula in re.split(" and ", formula):
        temp = sub_formula
        if sub_formula.startswith("(") and sub_formula.endswith(")"):
            sub_formula = sub_formula[1:-1]
            if "!" in sub_formula:
                sub_formula = sub_formula[3:-1]
                sub_formula = sub_formula.replace("=", "!=")
            formula = formula.replace(temp, sub_formula)
    return formula

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

