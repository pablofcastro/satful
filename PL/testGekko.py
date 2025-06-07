from pyscipopt import Model

from pyscipopt import Model
scip = Model ()
x = scip.addVar('x', vtype='C',lb=0.0,ub=1.0)
y = scip.addVar('y', vtype='C',lb=0.0,ub=1.0)
#scip. setObjective (x + y)
scip.addCons(eval("x*y >= 0.1"))
scip.addCons(x*y == 0.5)
scip.setHeuristics(3)
scip.setBoolParam("constraints/countsols/collect", True)
scip.setLongintParam("constraints/countsols/sollimit",100)
scip.hideOutput()
scip.optimize()
#scip.writeSol()
print(scip.getSols())
