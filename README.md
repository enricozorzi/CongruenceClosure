
# Congruence Closure Algorithm

In this project, i have implemented a solver based on the congruence closure decision algorithm.

The solver is capable of analyzing an SMT-LIB formula or a plain formula from .txt and .smt2, constructing a CC-DAG graph, and solving the satisfiability of the formula.


## Running Tests

Open the following link:

- [ColabTest](https://colab.research.google.com/drive/1Ehsiv_tYa7r91EsGEzvjg3tAge017yvs?usp=sharing)
1.  Run the REQUIREMENTS cell that contain this code
    ```bash
        !git clone https://github.com/enricozorzi/CongruenceClosure
        !pip install pysmt
        !pip install networkx
        !pip install colorama
        !pip install --upgrade cython
        !pip install --upgrade pysmt
        %cd CongruenceClosure/
    ```


2.  Run the TEST cell that contain this code
    ```bash
        !python main.py Test/test.txt
    ```
    



## Authors

- [@enricozorzi](https://github.com/enricozorzi)

