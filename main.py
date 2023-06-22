from pysmt.smtlib.parser import SmtLibParser
from colorama import Fore
from pysmt.rewritings import CNFizer
from cc_dag import CC_DAG
from parse import *
import time
import sys
import os
#cython: language_level=3

def main():

    # Get the script name from command line arguments
    script_name = sys.argv[1]
    # script_name = "Test/test.txt"
    
    if ".smt2" in script_name and os.path.exists(script_name):
        start = time.time()

        # Parse the SMT-LIB script
        smt_parser = SmtLibParser()
        script = smt_parser.get_script_fname(script_name)

        # Translate the formula to a string and remove unnecessary characters
        formula = translate_string(str(script.get_strict_formula().serialize()))
        cc_dag = CC_DAG()
        new_formula = formula.replace("f", "")  # Change s to s1, s2, s3, s4 to test
        print('\033[1m' + "Formula:" + '\033[0m', Fore.WHITE + new_formula + Fore.RESET + "\n")

        # Parse the formula and create a list of nodes
        list_of_nodes, cc_dag = parse_formula(new_formula, cc_dag)

        # Sort the list of nodes in descending order of length
        list_of_nodes = sorted(list_of_nodes, key=len, reverse=True)
        
        create_graph(cc_dag, list_of_nodes)

        # Update equalities and inequalities based on the list of nodes
        cc_dag.equalities, cc_dag.inequalities = update_eq_ineq(cc_dag.equalities, cc_dag.inequalities, list_of_nodes)
        print('\033[1m', "EQUALITIES:" , '\033[0m', cc_dag.equalities )
        print('\033[1m' , "INEQUALITIES:"  '\033[0m', cc_dag.inequalities, "\n")
        # visualize_dag(cc_dag)
        # print('\033[1m' + "List of nodes:" + '\033[0m', list_of_nodes)
        
        # Solve the formula using the CC_DAG and print the result
        print('\033[1m' + "The Formula is:",Fore.YELLOW + cc_dag.solve() + '\033[0m' )

        end = time.time()
        print('\033[1m' + "Time:" + '\033[0m',round( end - start,3),"seconds")

    elif ".txt" in script_name  and os.path.exists(script_name):
        print('\033[1m' + Fore.LIGHTCYAN_EX+"_"*100 + "\n" + '\033[0m')
        start = time.time()

        # Read the script file line by line
        script = open(script_name, "r").read().splitlines()
        
        for line in script:
            if "or" in line:
                print('\033[1m' + "Formula:" + '\033[0m' , line.replace("f", "")   )
                line_or = line.split(" or ")

                # Process each sub-formula separated by 'or'
                for i in range(len(line_or)):
                    cc_dag = CC_DAG()
                    new_formula = line_or[i].replace("f", "")  # Change s to s1, s2, s3, s4 to test
                    print('\n\033[1m' + "Sub-formula:" + '\033[0m' , new_formula  )

                     # Parse the sub-formula and create a list of nodes
                    list_of_nodes, cc_dag = parse_formula(new_formula, cc_dag)
                    list_of_nodes = sorted(list_of_nodes, key=len, reverse=True)
                    
                    create_graph(cc_dag, list_of_nodes)
                    
                    # Update equalities and inequalities based on the list of nodes
                    cc_dag.equalities, cc_dag.inequalities = update_eq_ineq(cc_dag.equalities, cc_dag.inequalities, list_of_nodes)
                    print('\n\033[1m', "EQUALITIES:" , '\033[0m', cc_dag.equalities )
                    print('\033[1m' , "INEQUALITIES:"  '\033[0m', cc_dag.inequalities )
                    # print('\033[1m' + "List of nodes:" + '\033[0m', list_of_nodes, "\n")
                    # visualize_dag(cc_dag)

                    # Solve the sub-formula using the CC_DAG and print the result
                    if(cc_dag.solve() == "SAT"):
                        print("\n" + '\033[1m' + "The Formula is:",Fore.GREEN + cc_dag.solve() + '\033[0m')
                        break

                    if i+1 == len(line_or) :
                        print("\n" + '\033[1m' + "The Formula is:",Fore.RED + cc_dag.solve() + '\033[0m')
            else:
                cc_dag = CC_DAG()
                new_formula = line.replace("f", "")  # Change s to s1, s2, s3, s4 to test
                print('\033[1m' + "Formula:" + '\033[0m' , new_formula)

                # Parse the formula and create a list of nodes
                list_of_nodes, cc_dag = parse_formula(new_formula, cc_dag)
                list_of_nodes = sorted(list_of_nodes, key=len, reverse=True)
                
                create_graph(cc_dag, list_of_nodes)
                
                # Update equalities and inequalities based on the list of nodes
                cc_dag.equalities, cc_dag.inequalities = update_eq_ineq(cc_dag.equalities, cc_dag.inequalities, list_of_nodes)
                print('\n\033[1m' + "EQUALITIES:" , '\033[0m', cc_dag.equalities )
                print('\033[1m' + "INEQUALITIES:"  '\033[0m', cc_dag.inequalities )
                # print('\033[1m' + "List of nodes:" + '\033[0m', list_of_nodes, "\n")
                #visualize_dag(cc_dag)

                # Solve the formula using the CC_DAG and print the result
                if cc_dag.solve() == "SAT":
                    print("\n"+'\033[1m' + "The Formula is:",Fore.GREEN + cc_dag.solve() + '\033[0m', "\n"  )
                else:
                    print("\n"+'\033[1m' + "The Formula is:",Fore.RED + cc_dag.solve() + '\033[0m', "\n"  )

                

            print('\033[1m' + Fore.LIGHTCYAN_EX+"_"*100 + "\n" + '\033[0m')
        end = time.time()
        print('\033[1m' + "Time:" + '\033[0m',round( end - start,3),"seconds")
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