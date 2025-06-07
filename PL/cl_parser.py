""" This is the parser for clauses, that is, collection of formulas of the style 
    lb; ub; form
    where up and lb are constants in [0,1], the meaning is that lb <= form <= ub
    you also conside list of clauses meaning the disjunction of them
"""

import logging
import AST as ast
from lark import Lark, Transformer, v_args
logging.basicConfig(level=logging.DEBUG)

# Define the grammar for collection of clauses
grammar = """
    ?start: clauses
    ?clauses: clause (clause)* -> clauses
    
    ?clause : constant ";" constant ";" form -> clause
    
    ?form : "TW" "(" form "," form ")" -> land
          | "TM" "(" form "," form ")" -> min
          | "TP" "(" form "," form ")" -> pand
          | "SM" "(" form "," form ")" -> max
          | "SW" "(" form "," form ")" -> lor
          | "SP" "(" form "," form ")" -> por
          | "IW" "(" form "," form ")" -> limplies
          | "IP" "(" form "," form ")" -> pimplies
          | "N" "(" form ")" -> lnot
          | "NP" "(" form ")" -> pnot
          | var 
          | constant 

    var: /[a-zA-Z_][a-zA-Z0-9_]*/   // Variable: alphanumeric starting with a letter
    constant: /-?\d+(\.\d+)?([eE][+-]?\d+)?/  // Constants in decimal notation
    %import common.WS
    %ignore WS
"""

@v_args(inline=True)

# we define a transformer for creating the AST
class ASTTransformer(Transformer) :
    clauses = ast.Clauses
    clause = ast.Clause
    land = ast.Land
    min = ast.Min
    lor = ast.Lor
    por = ast.Por
    max = ast.Max
    limplies = ast.Limp
    lnot = ast.Lnot
    pnot = ast.Pnot
    pand = ast.Pand
    por = ast.Por
    pimplies = ast.Pimp
    var = ast.Var
    constant = ast.Constant

# a function to parse a string, it returns an AST
def parse(clauses) :
    fuzzy_parser = Lark(grammar, start='start', parser='lalr',  debug=True)
    tree = fuzzy_parser.parse(clauses)
    return ASTTransformer().transform(tree)

def tests() :
    form1 = """0;1;TW(0.5,0.5)
               0;1;TW(0.5,0.5)
               0;1;IW(0.5,0.1)
            """
    fuzzy_parser = Lark(grammar, start='start', debug=True)
    tree1 = fuzzy_parser.parse(form1)
    print(tree1)



