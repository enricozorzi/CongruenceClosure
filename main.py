from cc_dag import *
from parse import *



a= CC_DAG()
cnf_parser = CNFizer()
smtparse = SmtLibParser()
script = smtparse.get_script_fname("Test/test4.smt2") # Change test1,test2,test3,test4 to test

s1 = "f(a,b) = a and f(f(a,b),b) != a" 
s2 = "f(o,p) = a and f(a,f(a,b,c,g),b,f(c,d)) != a"
s3 = "f(f(f(f(f(a))))) = a and f(a) != a"
s4 = traduceString(str(script.get_strict_formula().serialize()))

new_string = s4.replace("f","") # Change s to s1,s2,s3,s4 to test
print("string:",new_string)

list_node,a = parsing(new_string,a)
list_node = sorted(list_node, key=len,  reverse=True)
print("list of node:",list_node)

create_graph(a,list_node)
print("\n------------------")
for i in a.nodes:
    print("id:",i)
    for j in a.nodes[i]:
        print( j,":", a.nodes[i][j])
    print("\n------------------")
        



a.equalities,a.inequalities = update_eq_ineq(a.equalities,a.inequalities,list_node)
print("eq_node:",a.equalities)
print("ineq_node:",a.inequalities)
print("------------------\n")
visualize_dag(a)

print(a.solve())


