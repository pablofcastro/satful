import form_visitor as visitor

class ScipVisitor(visitor.FormVisitor) :
    
    def __init__(self, model) :
        self.model = model # the scip model
        self.vars = {} # a dict to save the vars of the model
        self.number_aux_vars = 0;
 
    def visit_var(self, var) :
        if  not (str(var) in self.vars) :
            newVar = self.model.addVar(str(var), vtype = 'C', lb=0.0, ub=1.0)
            self.vars[str(var)] = newVar
    
    def visit_constant(self, cons) :
        if  not (str(cons) in self.vars) :
            newVar = self.model.addVar(str(cons), vtype = 'C')
            self.vars[str(cons)] = newVar
            self.model.addCons(newVar == eval(str(cons)))
    
    def visit_max(self, max) :
        assert str(max.left) in self.vars, "the left operator is not in the model"
        assert str(max.right) in self.vars, "the right operator is not in the model"
        if not (str(max) in self.vars) :
            newVar = self.model.addVar(str(max), vtype = 'B') # the new var for the expression
            self.vars[str(max)] = newVar # the var for the current formula is added
            auxVarName = self.new_aux_var()
            auxVar = self.model.addVar(auxVarName, vtype = 'B')
            self.model.addCons(auxVar >= self.vars[str(max.left)] - self.vars[str(max.right)])
            self.model.addCons(1 - auxVar >= self.vars[str(max.right)] - self.vars[str(max.left)])
            self.model.addCons(newVar == auxVar * self.vars[str(max.left)] + (1-auxVar)* self.vars[str(max.right)])

    def visit_min(self, min) :
        assert str(min.left) in self.vars, "the left operator is not in the model"
        assert str(min.right) in self.vars, "the right operator is not in the model"
        if not (str(min) in self.vars) :
            newVar = self.model.addVar(str(min), vtype = 'B') # the new var for the expression
            self.vars[str(min)] = newVar # the var for the current formula is added
            auxVarName = self.new_aux_var()
            auxVar = self.model.addVar(auxVarName, vtype = 'B')
            self.model.addCons(auxVar >= self.vars[str(min.left)] - self.vars[str(min.right)])
            self.model.addCons(1 - auxVar >= self.vars[str(min.right)] - self.vars[str(min.left)])
            self.model.addCons(newVar == auxVar * self.vars[str(min.right)] + (1-auxVar)* self.vars[str(min.left)])

    def new_aux_var(self) : 
        self.number_aux_vars += 1
        return "_x"+str(self.number_aux_vars) # a new auxiliary var is created for decisions and returned

    def visit_pand(self, pand) :
        # we assume that the vars for the left and right are already in the model if not an exception is raised
        assert str(pand.left) in self.vars, "the left operator is not in the model"
        assert str(pand.right) in self.vars, "the right operator is not in the model"
        if not (str(pand) in self.vars) :
            newVar = self.model.addVar(str(pand), vtype = 'C', lb=0.0,ub=1.0)
            self.vars[str(pand)] = newVar
            self.model.addCons(newVar == self.vars[str(pand.left)] * self.vars[str(pand.right)])

    def visit_por(self, por) :
        # we assume that the vars for the left and right are already in the model if not an exception is raised
        assert str(por.left) in self.vars, "the left operator is not in the model"
        assert str(por.right) in self.vars, "the right operator is not in the model"
        if not (str(por) in self.vars) :
            newVar = self.model.addVar(str(por), vtype = 'C', lb=0.0,ub=1.0)
            self.vars[str(por)] = newVar
            self.model.addCons(newVar == (self.vars[str(por.left)] + self.vars[str(por.right)]) - (self.vars[str(por.left)] * self.vars[str(por.right)]))

    def visit_pnot(self, pnot) :
        # we assume that the vars for the left and right are already in the model if not an exception is raised
        assert str(pnot.operand) in self.vars, "the operand is not in the model"
        if not (str(pnot) in self.vars) :
            newVar = self.model.addVar(str(pnot), vtype = 'B') # the new var for the expression
            self.vars[str(pnot)] = newVar # the var for the current formula is added
            self.model.addCons(newVar >= 1 - self.vars[str(pnot.operand)])
            self.model.addCons(1 - newVar >= self.vars[str(pnot.operand)])

    def visit_pimplies(self,  pimplies) :
        assert str(pimplies.left) in self.vars, "error constructing the model, the left operator is not in the model"
        assert str(pimplies.right) in self.vars, "error constructing the model, the right operator is not in the model"
        if not (str(pimplies) in self.vars) :
            newVar = self.model.addVar(str(pimplies), vtype = 'C') # the new var for the expression
            self.vars[str(pimplies)] = newVar # the var for the current formula is added
            auxVarName = self.new_aux_var()
            auxVar = self.model.addVar(auxVarName, vtype = 'B')
            self.model.addCons(auxVar >= self.vars[str(pimplies.left)] - self.vars[str(pimplies.right)])
            self.model.addCons(1-auxVar >= self.vars[str(pimplies.right)] - self.vars[str(pimplies.left)])
            self.model.addCons(newVar  == (self.vars[str(pimplies.right)]/self.vars[str(pimplies.left)]) * auxVar + (1 - auxVar)) # check issues with division by zero
            
    def visit_land(self, land) :
        assert str(land.left) in self.vars, "error constructing the model, the left operator is not in the model"
        assert str(land.right) in self.vars, "error constructing the model, the right operator is not in the model"
        if not (str(land) in self.vars) :
            newVar = self.model.addVar(str(land), vtype = 'C', lb=0.0,ub=1.0)
            self.vars[str(land)] = newVar # the var for the current formula is added
            auxVarName = self.new_aux_var()
            auxVar = self.model.addVar(auxVarName, vtype = 'B')
            self.model.addCons(auxVar >= 1 - self.vars[str(land.left)] - self.vars[str(land.right)])
            self.model.addCons((1-auxVar) >= self.vars[str(land.left)] + self.vars[str(land.right)] - 1)
            self.model.addCons(newVar ==  (1-auxVar)*(self.vars[str(land.left)] + self.vars[str(land.right)] - 1))

    def visit_limplies(self, limplies) :
        assert str(limplies.left) in self.vars, "error constructing the model, the left operator is not in the model"
        assert str(limplies.right) in self.vars, "error constructing the model, the right operator is not in the model"
        if not (str(limplies) in self.vars) :
            newVar = self.model.addVar(str(limplies), vtype = 'C', lb=0.0,ub=1.0)
            self.vars[str(limplies)] = newVar # the var for the current formula is added
            auxVarName = self.new_aux_var()
            auxVar = self.model.addVar(auxVarName, vtype = 'B')
            self.model.addCons(auxVar >= self.vars[str(limplies.left)] - self.vars[str(limplies.right)])
            self.model.addCons((1-auxVar) >= self.vars[str(limplies.right)] - self.vars[str(limplies.left)])
            self.model.addCons(newVar ==  auxVar + (1- auxVar)*(1 - self.vars[str(limplies.left)] + self.vars[str(limplies.right)]))

    def visit_lor(self, lor) : 
        assert str(lor.left) in self.vars, "error constructing the model, the left operator is not in the model"
        assert str(lor.right) in self.vars, "error constructing the model, the right operator is not in the model"
        if not (str(lor) in self.vars) :
            newVar = self.model.addVar(str(lor), vtype = 'C', lb=0.0,ub=1.0)
            self.vars[str(lor)] = newVar # the var for the current formula is added
            auxVarName = self.new_aux_var()
            auxVar = self.model.addVar(auxVarName, vtype = 'B')
            self.model.addCons(auxVar >= 1 - self.vars[str(lor.left)] - self.vars[str(lor.right)])
            self.model.addCons((1-auxVar) >= self.vars[str(lor.right)] + self.vars[str(lor.left)] - 1)
            self.model.addCons(newVar == auxVar + (1- auxVar)*(self.vars[str(lor.left)] + self.vars[str(lor.right)]))

    def visit_lnot(self, lnot) : 
        assert str(lnot.operand) in self.vars, "error constructing the model, the left operator is not in the model"
        if not (str(lnot) in self.vars) :
            newVar = self.model.addVar(str(lnot), vtype = 'C', lb=0.0,ub=1.0)
            self.vars[str(lnot)] = newVar # the var for the current formula is added
            self.model.addCons(newVar ==  1 - self.vars[str(lnot.operand)])
            #auxVarName = self.new_aux_var()
            #auxVar = self.model.addVar(auxVarName, vtype = 'B')
            #self.model.addCons(auxVar >= 1 - self.vars[str(lnot.operand)])
            #self.model.addCons((1-auxVar) >= self.vars[str(lnot.operand)])
            #self.model.addCons(newVar ==  auxVar + (1- auxVar)*(1 - self.vars[str(lnot.operand)]))






