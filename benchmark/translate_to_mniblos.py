"""""
    A simple script for translate formulas to mniblos syntax
    Usage: python to_mniblos input_dir output_dir
"""

import sys
sys.path.append('../PL/')
import form_visitor as visitor
import cl_parser as cl_parser
import sys
import os

class TranslateMNISVisitor(visitor.FormVisitor):

    def __init__(self) :
        self.form_translation = {} # saves the value of each subformula
       
    def visit_constant(self, cons) :
        self.form_translation[str(cons)] = str(cons)

    def visit_var(self, var) :
        self.form_translation[str(var)] = var.name

    def visit_land(self, land) :
        left = self.form_translation[str(land.left)]
        right = self.form_translation[str(land.right)]
        self.form_translation[str(land)] = f"""(con {left} {right})"""

    def visit_lor(self, lor) :
        left = self.form_translation[str(lor.left)]
        right = self.form_translation[str(lor.right)]
        self.form_translation[str(lor)] = f"""(wdis {left} {right})"""

    def visit_pand(self, pand) :
        left = self.form_translation[str(pand.left)]
        right = self.form_translation[str(pand.right)]
        self.form_translation[str(pand)] = f"""(con {left} {right})"""
    
    def visit_por(self, por) :
        left = self.form_translation[str(por.left)]
        right = self.form_translation[str(por.right)]
        self.form_translation[str(por)] = f"""(wdis {left} {right})"""

    def visit_pimplies(self, pimplies) :
        left = self.form_translation[str(pimplies.left)]
        right = self.form_translation[str(pimplies.right)]
        self.form_translation[str(pimplies)] = f"""(impl {left} {right})"""

    def visit_limplies(self, limplies) :
        left = self.form_translation[str(limplies.left)]
        right = self.form_translation[str(limplies.right)]
        self.form_translation[str(limplies)] = f"""(impl {left} {right})"""

    def visit_lnot(self, lnot) :
        operand = self.form_translation[str(lnot.operand)]
        self.form_translation[str(lnot)] = f"""(neg {operand})"""

    def visit_pnot(self, pnot) :
        operand = self.form_translation[str(pnot.operand)]
        self.form_translation[str(pnot)] = f"""(neg {operand})"""

    def visit_max(self, maxf) :
        left = self.form_translation[str(maxf.left)]
        right = self.form_translation[str(maxf.right)]
        self.form_translation[str(maxf)] = f"""(wdis {left} {right})"""
        
    def visit_min(self, minf) :
        left = self.form_translation[str(minf.left)]
        right = self.form_translation[str(minf.right)]
        self.form_translation[str(minf)] = f"""(wcon {left} {right})"""

if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    for file in os.listdir(input_dir) :
        print(file)
        output_file = open(output_dir+"/"+file,"w")
        input_file = open(input_dir+"/"+file, "r")
        text = input_file.read()
        ast = cl_parser.parse(text)
        output_file.write(":")
        for clause in ast.clauses : 
            visitor = TranslateMNISVisitor()
            form = clause.form
            lb = float(str(clause.lbound))
            ub = float(str(clause.ubound))
            form.accept(visitor)
            output_file.write(f""":(leq {lb} {visitor.form_translation[str(form)]})""")
            output_file.write(f""":(geq {ub} {visitor.form_translation[str(form)]})""")
        output_file.close()


            
