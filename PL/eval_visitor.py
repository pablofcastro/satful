"""
    A basic visitor to evaluate a formula given a valuation (dictionary)
"""
import form_visitor as visitor
import parser as parser

class EvalVisitor(visitor.FormVisitor):

    def __init__(self, valuation) :
        self.var_valuation = valuation # the valuation of each var
        self.form_valuation = {} # saves the value of each subformula
       
    def visit_constant(self, cons) :
        self.form_valuation[str(cons)] = eval(str(cons))

    def visit_var(self, var) :
        assert str(var) in self.var_valuation.keys(), f"""Var {str(var)} is not in the valuation."""
        self.form_valuation[str(var)] = self.var_valuation[str(var)]

    def visit_land(self, land) :
        self.form_valuation[str(land)] = max(self.form_valuation[str(land.left)]+self.form_valuation[str(land.left)]-1,0)

    def visit_lor(self, lor) :
        self.form_valuation[str(lor)] =  min(1, self.form_valuation[str(lor.left)]+self.form_valuation[str(lor.right)])

    def visit_pand(self, pand) :
        self.form_valuation[str(pand)] =  self.form_valuation[str(pand.left)] * self.form_valuation[str(pand.right)]
    
    def visit_por(self, por) :
        self.form_valuation[str(por)] = (self.form_valuation[str(por.left)] + self.form_valuation[str(por.right)]) - (self.form_valuation[str(por.left)] * self.form_valuation[str(por.right)]) 

    def visit_pimplies(self, pimplies) :
        left = self.form_valuation[str(pimplies.left)]
        right = self.form_valuation[str(pimplies.right)]
        self.form_valuation[str(pimplies)] = 1 if left <= right else right/left

    def visit_limplies(self, limplies) :
        left = self.form_valuation[str(limplies.left)]
        right = self.form_valuation[str(limplies.right)]
        self.form_valuation[str(limplies)] = 1 if (left <= right) else (1-left)+right

    def visit_lnot(self, lnot) :
        self.form_valuation[str(lnot)] = 1 - self.form_valuation[str(lnot.operand)]

    def visit_pnot(self, pnot) :
        self.form_valuation[str(pnot)] = 1 if self.form_valuation[str(pnot.operand)] == 0 else 0

    def visit_max(self, maxf) :
        self.form_valuation[str(maxf)] = max(self.form_valuation[str(maxf.left)],self.form_valuation[str(maxf.right)])

    def visit_min(self, minf) :
        self.form_valuation[str(minf)] = min(self.form_valuation[str(minf.left)],self.form_valuation[str(minf.right)])


def tests() :
    """ 
        Some tests for the valuation 
    """
    form1_string = "x lor y"
    form2_string = "x limplies (x lor y)"
    form3_string = "x por ((x max z) min z)"
    form4_string = "0.56 lor x"
    form5_string = "x pand y"
    form6_string = "x por y"
    form7_string = "x pimplies y"

    # The evaluation we use
    valuation = {"x":0.5, "y":0.2, "z":1}
    print(f"""Valuation: {valuation}""")
    for form_string in (form1_string, form2_string, form3_string, form4_string, form5_string, form6_string, form7_string) :
        # eval the  formula
        form = parser.parse(form_string) 
        eval = EvalVisitor(valuation)
        form.accept(eval)
        print(f""" Formula: { form_string } evaluates to {eval.form_valuation[str(form)]}""")


if __name__ == '__main__':
    tests()


    