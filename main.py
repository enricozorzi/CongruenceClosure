from pysmt.smtlib.parser import SmtLibParser
from colorama import Fore
from pysmt.rewritings import CNFizer
from cc_dag import CC_DAG
from parse import *
import sys
import os

def main():
    # script_name = "Test/test2.smt2"
    script_name = sys.argv[1]
    if ".smt2" in script_name and os.path.exists(script_name):
        smt_parser = SmtLibParser()
        script = smt_parser.get_script_fname(script_name)
        formula = translate_string(str(script.get_strict_formula().serialize()))
        cc_dag = CC_DAG()
        new_formula = formula.replace("f", "")  # Change s to s1, s2, s3, s4 to test
        print('\033[1m' + "Formula:" + '\033[0m', Fore.WHITE + new_formula + Fore.RESET + "\n")
        list_of_nodes, cc_dag = parse_formula(new_formula, cc_dag)
        list_of_nodes = sorted(list_of_nodes, key=len, reverse=True)
        
        create_graph(cc_dag, list_of_nodes)
        

        cc_dag.equalities, cc_dag.inequalities = update_eq_ineq(cc_dag.equalities, cc_dag.inequalities, list_of_nodes)
        print('\033[1m', "EQUALITIES:" , '\033[0m', cc_dag.equalities )
        print('\033[1m' , "INEQUALITIES:"  '\033[0m', cc_dag.inequalities, "\n")
           

        visualize_dag(cc_dag)

        # print('\033[1m' + "List of nodes:" + '\033[0m', list_of_nodes)
        print('\033[1m' + "The Formula is:",Fore.YELLOW + cc_dag.solve() + '\033[0m' )

    elif ".txt" in script_name  and os.path.exists(script_name):
        script = open(script_name, "r").read().splitlines()
        
        for line in script:
            cc_dag = CC_DAG()
            new_formula = line.replace("f", "")  # Change s to s1, s2, s3, s4 to test
            print('\033[1m' + "Formula:" + '\033[0m' , new_formula  )
            list_of_nodes, cc_dag = parse_formula(new_formula, cc_dag)
            list_of_nodes = sorted(list_of_nodes, key=len, reverse=True)
            # print('\033[1m' + "List of nodes:" + '\033[0m', list_of_nodes, "\n")
            create_graph(cc_dag, list_of_nodes)
            
            
            cc_dag.equalities, cc_dag.inequalities = update_eq_ineq(cc_dag.equalities, cc_dag.inequalities, list_of_nodes)
            print('\n\033[1m', "EQUALITIES:" , '\033[0m', cc_dag.equalities )
            print('\033[1m' , "INEQUALITIES:"  '\033[0m', cc_dag.inequalities )
           
            # visualize_dag(cc_dag)

            
            print("\n"+'\033[1m' + "The Formula is:",Fore.YELLOW + cc_dag.solve() + '\033[0m',  )
            print('\033[1m' + "#########################################################\n" + '\033[0m')
    else:
        print("Please enter a valid file")


if __name__ == "__main__":
    main()



# print("\n------------------")
    # for node_id in cc_dag.nodes:
    #     print("id:", node_id)
    #     for node_value in cc_dag.nodes[node_id]:
    #         print(node_value, ":", cc_dag.nodes[node_id][node_value])
    #     print("\n------------------")
    # visualize_dag(cc_dag)