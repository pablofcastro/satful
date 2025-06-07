import logging
import AST as ast
from lark import Lark, Transformer, v_args
logging.basicConfig(level=logging.DEBUG)

# Define the grammar for plain fuzzy formulas
grammar = """
    ?start: form
    ?form: conj
    ?conj: disj
         | conj "land" disj -> land
         | conj "pand" disj -> pand
         | conj "min" disj  -> min

    ?disj: imp
         | disj "lor" imp -> lor
         | disj "por" imp -> por
         | disj "max" imp -> max

    ?imp: imp "limplies" elem -> limplies
        | imp "pimplies" elem -> pimplies
        | elem

    ?elem: "lnot" elem -> lnot
         | "pnot" elem -> pnot
         | var
         | constant
         | "(" form ")"

    var: /[a-zA-Z_][a-zA-Z0-9_]*/   // Variable: alphanumeric starting with a letter
    constant: /-?\d+(\.\d+)?([eE][+-]?\d+)?/  // Constants in decimal notation
    %import common.WS
    %ignore WS
"""

@v_args(inline=True)

# we define a transformer for creating the AST
class ASTTransformer(Transformer) :
    land = ast.Land
    pand = ast.Pand
    min = ast.Min
    lor = ast.Lor
    por = ast.Por
    max = ast.Max
    limplies = ast.Limp
    pimplies = ast.Pimp
    lnot = ast.Lnot
    pnot = ast.Pnot
    var = ast.Var
    constant = ast.Constant

# a function to parse a string, it returns an AST
def parse(form) :
    fuzzy_parser = Lark(grammar, start='start', parser='lalr',  debug=True)
    tree = fuzzy_parser.parse(form)
    return ASTTransformer().transform(tree)

# some tests for testing the parser
def tests() :
    form1 = "x lor y"
    form2 = "x"
    form3 = "x limplies (x lor y)"
    form4 = "x por ((x max z) min z)"
    form5 = "0.56 lor x"

    fuzzy_parser = Lark(grammar, start='start', parser='lalr',  debug=True)
    fparser = Lark(grammar, start='start', parser='lalr',  debug=True)
    tree1 = fuzzy_parser.parse(form1)
    print(ASTTransformer().transform(tree1))
    tree2 = fuzzy_parser.parse(form2)
    print(ASTTransformer().transform(tree2))
    tree3 = fuzzy_parser.parse(form3)
    print(ASTTransformer().transform(tree3))
    tree4 = fuzzy_parser.parse(form4)
    print(ASTTransformer().transform(tree4))
    tree5 = fuzzy_parser.parse(form5)
    print(ASTTransformer().transform(tree5))
