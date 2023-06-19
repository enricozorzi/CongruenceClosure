from pysmt.smtlib.parser import SmtLibParser
from pysmt.rewritings import CNFizer
from cc_dag import CC_DAG
from parse import *

def main():
    cc_dag = CC_DAG()
    smt_parser = SmtLibParser()
    script = smt_parser.get_script_fname("Test/test4.smt2")  # Change test1,test2,test3,test4 to change the smt2 file

    #Dont Use f as a variable name in the formula
    formula1 = "f(a, b) = a and f(f(a, b), b) != a"  #UNSAT
    formula2 = "f(a, b) = a and f(f(d, b), b) != a"  #SAT
    formula3 = "f(f(f(a))) = a and f(f(f(f(f(a))))) = a and f(a) != a"  #UNSAT
    formula4 = "f(f(f(a))) = f(a) and f(f(a)) = a and f(a) != a"   #SAT
    formula5 = translate_string(str(script.get_strict_formula().serialize()))
    formula6 = "f(x) = f(y) and x != y" #SAT
    formula7 = "f(f(a))=f(b)&f(f(a))!=f(b)" #UNSAT
 

    new_formula = formula6.replace("f", "")  # Change s to s1, s2, s3, s4 to test
    print("formula:", new_formula)

    list_of_nodes, cc_dag = parse_formula(new_formula, cc_dag)
    list_of_nodes = sorted(list_of_nodes, key=len, reverse=True)
    print("list of nodes:", list_of_nodes)

    create_graph(cc_dag, list_of_nodes)
    # print("\n------------------")
    # for node_id in cc_dag.nodes:
    #     print("id:", node_id)
    #     for node_value in cc_dag.nodes[node_id]:
    #         print(node_value, ":", cc_dag.nodes[node_id][node_value])
    #     print("\n------------------")

    cc_dag.equalities, cc_dag.inequalities = update_eq_ineq(cc_dag.equalities, cc_dag.inequalities, list_of_nodes)
    print("eq_nodes:", cc_dag.equalities)
    print("ineq_nodes:", cc_dag.inequalities)
    print("------------------\n")
    # visualize_dag(cc_dag)

    print(cc_dag.solve())
    
    # print("\n------------------")
    # for node_id in cc_dag.nodes:
    #     print("id:", node_id)
    #     for node_value in cc_dag.nodes[node_id]:
    #         print(node_value, ":", cc_dag.nodes[node_id][node_value])
    #     print("\n------------------")
    # visualize_dag(cc_dag)


if __name__ == "__main__":
    main()
