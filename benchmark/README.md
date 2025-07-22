# Benchmarks for evaluating SATFuL

This folder contains several scripts and examples used to evaluate the tool. 

* ``run_benchmark.py``: runs the different benchmarks, for instance: 
```
python run_benchmarks -g -product
``` 
runs all the product logic benchmarks using Gurobi the results are saved in a .csv file.

*  ``translate_to_mniblos.py``: translates the benchmarks to the syntax of niblos. 

* ``scatter_plot.py``: generates the scatter plots using the obtained results

* ``scatter_plot_product.py``: generates the scatter plots for the product logics.

* ``formulas_gen.py``: it randomly generates formulas. To generate formulas you can execute: 
``python formulas_gen.py 50 10 10 P satful`` generates 50 formulas using 10 variables, each formula contains ocurrence of the 10 variables, with the satful syntax. The results are saved in the ``generatedForms/`` folder.

All the generated scatter plots can be found at folder `` plots/``

# Running the benchmarks

To run the benchmarks again you have to use the ``run_benchmark.py`` scrip:

Examples:
``python run_benchmarks -g -product``: Runs all the benchmarks for product logic using gurobi
``python run_benchmarks -s -product``: Runs the benchmarks for product logic using SCIP
``python run_benchmarks -g -luk``: Runs the benchmarks for Luk logic using Gurobi
``python run_benchmarks -s -luk``: Runs the benchmarks for Luk logic using SCIP

# Folders

The folders contains the datasets for the benchmarks.

``randomFormulas/``: it contains formulas with 10,20,30,40 variables. This is the benchmark used in [1]
``FuzzySAT/``: contains the results obtained for fuzzysat
``productRandomClauses/``: contains the benchmark for product formulas, generated using the script ``formulas_gen.py``. It also contains the translation of these formulas to niblos syntax.


