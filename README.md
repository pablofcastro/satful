# SATFuL: A Simple SAT solver for Fuzzy Logics

SATFuL is a simple solver for fuzzy logics, including:

* Lukasiewicz logic
* Produc logic
* Godel logic

the tool is completly written in Python and uses MINLP solvers for solving SAT problems for these logics.

# Running the tool

The typical command for running the tool is

```
python PL/satful.pl [-l|-s] -i <filename>
```

with option `-g` the tool uses Gurobi to solve the non-linear equations, with option `-s` the tool uses the solver SCIP. T You need to have installed some of these libraries to run the tool. 

# Benchmarks

The folder ``benchmarks/```contains several benchmarks and scripts used for evaluating the performance of the tool. 
