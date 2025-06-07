import argparse, os
import parser as parser
import cl_parser as cl_parser
import AST as ast
import scip_visitor as scip_visitor
import gurobi_visitor as gurobi_visitor
import gurobipy as gp
from gurobipy import GRB
from pyscipopt import Model
import sys

rels = ["geq", "leq"]
verbose = False

def validate_file(f):
    if not os.path.exists(f):
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError(f"Couldn't find {f}.")
    return f


def sat_form_scip(formula, ineq, bound) :
    assert ineq in rels
    assert (0 <= bound) & (bound <= 1)  
    ast = parser.parse(formula)
    print(str(ast))
    model = Model()
    visitor = scip_visitor.ScipVisitor(model)
    scip = visitor.model
    scip.setHeuristics(3)
    ast.accept(visitor)
    if (ineq == "geq") :
        model.addCons(visitor.vars[str(ast)] >= bound)
    elif (ineq == "leq") :
        model.addCons(visitor.vars[str(ast)] <= bound)
    #scip.setBoolParam("constraints/countsols/collect", True)
    #scip.setLongintParam("constraints/countsols/sollimit",100)
    #scip.hideOutput()
    scip.presolve()
    scip.optimize()
    #scip.writeSol()

def sat_form_gurobi(formula, ineq, bound) :
   pass

def sat_clauses_scip(problem) :
    ast = cl_parser.parse(problem)
    model = Model()
    model.hideOutput()
    visitor = scip_visitor.ScipVisitor(model)
    scip = visitor.model
    scip.setHeuristics(3)
    for clause in ast.clauses :
        form = clause.form
        lb = clause.lbound
        ub = clause.ubound
        #print(str(form))
        form.accept(visitor)
        model.addCons(visitor.vars[str(form)] >= float(str(lb)))
        model.addCons(visitor.vars[str(form)] <= float(str(ub)))
        #scip.presolve()
    scip.optimize()
    #print(scip.getSols())
    if scip.getStatus() == "optimal" :
        print("Result : SAT")
    else :
        print("Result : UNSAT")
    print(f"Time : {model.getSolvingTime()} secs")
    #print(scip.count())

def sat_clauses_gurobi(problem, verbose=False) :
    ast = cl_parser.parse(problem)
    # print(str(ast))
    env = gp.Env(empty=True)
    env.setParam('OutputFlag', 0)
    env.start()
    model  = gp.Model("NLP",env=env)
    visitor = gurobi_visitor.GurobiVisitor(model)
    gurobi = visitor.model
    for clause in ast.clauses :
        form = clause.form
        lb = clause.lbound
        ub = clause.ubound
        #print(str(form))
        form.accept(visitor)
        model.addConstr(visitor.vars[str(form)] >= float(str(lb)))
        model.addConstr(visitor.vars[str(form)] <= float(str(ub)))
        # if we want to inspect the model
        # model.write("model.lp")
    gurobi.optimize()
    print("Result : SAT" if model.status == GRB.OPTIMAL else "Result : UNSAT")
    print(f"Time : {model.Runtime} secs")
    if verbose and model.status == GRB.OPTIMAL:
        valuation = {}
        # if verbose, the values of the variables are shown
        for v in model.getVars():
            if v.VarName in visitor.prop_vars :
                valuation[v.VarName] = v.X
        print(f"Valuation found: {valuation}")

   
def main() :
    """ This is the main function of the solver 
        the options can be:
        + --help: shows the options
        + --file (-f): process a file
        + --gurobi (-g): uses gurobi
        + --scip (-s): uses scip, this is the default 
    """
    parser = argparse.ArgumentParser()
    file = ""
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-g", "--gurobi", help="uses gurobi as a MINLP solver", action="store_true")
    parser.add_argument("-s", "--scip", help="uses scip as a MINLP solver (default)", action="store_true")
    parser.add_argument("-i", "--input", dest="file", required=True, type=validate_file,
                        help="the file with the formula", metavar="FILE")
    parser.add_argument("-p", "--plain", help="to indicate that the format of the formula is the plain style (default)", action="store_true")
    parser.add_argument("-c", "--clause", help="to indicate that the format of the formula is the clause style", action="store_true")    
    args = parser.parse_args()
    try :
        file = open(args.file, "r")
    except OSError:
        print(f"Error: Couldn't open input file")
        sys.exit()

    problem = file.read()

    if args.gurobi :
        # the gurobi solver was selected.
        try :
            #if args.clause :
            sat_clauses_gurobi(problem, args.verbose)
            #else :
            #    sat_form_gurobi(problem)
        except :
            raise("Error executing Gurobi, please check the installation") 
    elif args.scip :
        try :
            sat_clauses_scip(problem)
        except :
            raise("Error executing scip, please check the installation")
    elif args.scip :
        try :
            if args.clause :
                sat_clauses_scip(problem)
            else :
                sat_form_scip(problem)
        except :
            raise("Error executing scip, please check the installation")


# the main entry 
if __name__ == "__main__" :
    main()


def read_file(file) :
    try :
        file = open(file, "r")
    except : 
        print(f"Error opening file: {file}")
    problem = file.read()



clauses0 = """0.25;1.0;N(TW(v8,N(TW(N(TW(v12,N(TW(v9,v16)))),N(v24)))))
0.0;1.0;TW(v1,N(TW(N(TW(v22,N(v28))),TW(v16,v0))))
0.0;1.0;TW(v29,TW(TW(N(TW(N(v28),N(v10))),N(v6)),N(v3)))
0.0;1.0;TW(TW(N(TW(N(v20),v0)),N(TW(N(v4),N(v2)))),N(v9))
0.0;1.0;TW(v8,TW(v28,TW(TW(v3,v7),v14)))
1.0;1.0;N(TW(N(TW(TW(N(v27),v4),N(TW(N(v18),N(v17))))),v12))
0.0;1.0;TW(TW(TW(v5,v14),v7),TW(N(v26),v2))
0.25;1.0;N(TW(TW(v29,N(v20)),N(TW(N(TW(v16,N(v25))),N(v6)))))
1.0;1.0;N(TW(TW(N(v6),TW(N(v20),N(v17))),N(TW(v19,v11))))
1.0;1.0;N(TW(N(TW(N(v27),v22)),TW(N(v17),TW(v23,v21))))
0.75;1.0;N(TW(v27,N(TW(TW(N(v23),N(v10)),TW(v15,v26)))))
1.0;1.0;N(TW(TW(N(v26),N(TW(N(v27),N(TW(N(v29),v13))))),v15))
0.75;1.0;TW(v18,N(TW(N(TW(N(v4),N(v8))),TW(N(v2),v28))))
0.0;1.0;TW(TW(TW(v24,N(TW(N(v3),N(v8)))),N(v0)),v27)
0.25;1.0;TW(v6,N(TW(N(v16),TW(TW(N(v21),N(v1)),v27))))
0.0;1.0;TW(TW(N(TW(N(v27),v10)),N(v3)),TW(v9,N(v7)))
0.0;1.0;TW(TW(N(v21),TW(v14,N(v19))),TW(N(v11),v12))
0.0;1.0;TW(N(TW(N(TW(N(v25),v2)),v1)),TW(v9,v5))
0.0;1.0;TW(TW(N(v15),TW(N(v2),N(TW(v5,N(v21))))),v6)
1.0;1.0;N(TW(TW(TW(N(v3),N(v28)),N(TW(N(v2),v7))),v8))
0.25;1.0;N(TW(N(TW(v9,N(TW(N(TW(N(v5),v0)),v24)))),v29))
0.5;1.0;N(TW(N(v2),TW(N(TW(N(TW(N(v22),v15)),N(v12))),v16)))
0.0;1.0;TW(N(TW(N(v15),N(TW(v12,v5)))),TW(v24,v9))
0.0;1.0;TW(N(v17),TW(N(TW(N(TW(v9,v18)),N(v28))),N(v24)))
0.0;1.0;TW(TW(v6,v17),N(TW(TW(v7,N(v9)),N(v3))))
0.0;1.0;TW(v9,N(TW(N(v7),N(TW(N(v19),TW(v6,N(v15)))))))
0.0;1.0;TW(N(TW(N(TW(N(v19),v14)),N(TW(N(v5),v12)))),v27)
0.0;1.0;TW(N(v15),TW(N(TW(N(v17),v18)),N(TW(N(v2),v11))))
0.25;1.0;N(TW(N(v25),N(TW(v14,TW(N(TW(N(v28),N(v22))),v2)))))
0.25;1.0;TW(N(TW(N(v2),v26)),TW(v14,N(TW(N(v18),v25))))
0.75;1.0;N(TW(N(v4),N(TW(TW(v6,N(v7)),N(TW(v14,N(v1)))))))
0.75;1.0;N(TW(N(TW(N(TW(N(v27),v13)),N(TW(v9,v3)))),N(v15)))
0.5;1.0;N(TW(N(TW(TW(TW(N(v2),N(v17)),N(v26)),N(v4))),v22))
0.75;1.0;TW(N(TW(v0,N(v26))),N(TW(N(v12),N(TW(v17,v16)))))
0.5;1.0;N(TW(N(v3),N(TW(N(v4),TW(v28,N(TW(v14,v8)))))))
0.0;1.0;TW(TW(v12,N(v20)),TW(TW(N(v26),N(v28)),v15))
0.75;1.0;TW(N(TW(TW(v3,v9),v6)),N(TW(v17,N(v8))))
0.0;1.0;TW(TW(v25,N(TW(N(v12),v27))),N(TW(v6,v26)))
0.0;1.0;TW(N(TW(N(TW(N(TW(N(v26),v7)),N(v8))),N(v19))),N(v16))
0.0;1.0;N(TW(N(TW(N(v4),TW(N(v14),N(v15)))),N(TW(N(v17),N(v11)))))
0.0;1.0;TW(TW(TW(N(v27),v12),N(v24)),N(TW(N(v6),N(v10))))
1.0;1.0;N(TW(TW(N(v12),N(v18)),N(TW(N(v27),N(TW(N(v21),v3))))))
0.25;1.0;N(TW(v16,N(TW(N(TW(N(v29),N(TW(N(v14),v9)))),N(v15)))))
0.0;1.0;TW(TW(TW(N(v26),N(v8)),v18),TW(v3,N(v19)))
1.0;1.0;N(TW(TW(N(TW(v21,v4)),v26),TW(N(v10),N(v20))))
0.75;1.0;N(TW(N(TW(N(v21),TW(v6,v9))),TW(v4,v8)))
1.0;1.0;TW(N(TW(N(v7),TW(v25,v19))),N(TW(v28,N(v9))))
0.25;1.0;TW(N(TW(v20,N(TW(N(v26),v0)))),TW(v27,N(v12)))
1.0;1.0;N(TW(v9,TW(N(TW(N(v24),N(TW(v23,N(v6))))),v20)))
0.75;1.0;N(TW(v16,TW(N(TW(TW(N(v7),N(v6)),v19)),N(v20))))
1.0;1.0;N(TW(N(TW(N(v15),N(TW(N(v4),N(v14))))),TW(N(v10),v2)))
1.0;1.0;N(TW(TW(N(v18),v25),TW(N(TW(v21,v27)),N(v0))))
0.0;1.0;TW(N(TW(N(v14),v12)),N(TW(N(TW(N(v3),N(v1))),v9)))
0.0;1.0;N(TW(v16,N(TW(TW(v29,v13),N(TW(v20,v11))))))
1.0;1.0;N(TW(v25,TW(TW(v10,N(v6)),TW(v5,N(v27)))))
1.0;1.0;TW(N(TW(N(v13),v25)),N(TW(N(TW(v4,v11)),v17)))
1.0;1.0;N(TW(TW(N(TW(v18,N(v5))),v29),TW(N(v2),N(v16))))
0.25;1.0;TW(TW(TW(v11,N(v12)),N(v2)),N(TW(v13,N(v24))))
0.0;1.0;TW(N(v15),TW(N(TW(N(v23),v29)),TW(N(v20),N(v8))))
0.0;1.0;TW(TW(N(v2),TW(N(v28),N(v19))),TW(v17,N(v16)))
0.0;1.0;TW(TW(v6,N(TW(v8,v21))),N(TW(N(v24),N(v4))))
0.0;1.0;TW(TW(N(v10),N(v17)),N(TW(v2,N(TW(v4,N(v6))))))
0.0;1.0;TW(TW(N(v18),TW(N(v13),v11)),N(TW(v15,v6)))
1.0;1.0;N(TW(N(v4),TW(TW(N(TW(v16,v6)),v28),N(v24))))
0.25;1.0;N(TW(N(TW(N(TW(N(TW(N(v3),N(v26))),v20)),N(v11))),v5))
0.0;1.0;TW(TW(v8,N(TW(N(TW(N(v22),N(v3))),v21))),N(v25))
0.0;1.0;TW(N(TW(N(TW(N(v27),v1)),N(TW(v29,N(v24))))),N(v17))
0.0;1.0;TW(TW(N(v10),v18),TW(N(TW(N(v23),N(v9))),v21))
0.0;1.0;TW(v15,TW(N(v18),TW(N(v7),TW(v19,v2))))
1.0;1.0;N(TW(N(TW(v12,N(v24))),TW(N(v21),TW(v7,v14))))
0.75;1.0;TW(N(TW(v14,N(TW(N(v11),N(v13))))),N(TW(N(v3),N(v8))))
0.0;1.0;TW(TW(TW(v2,N(v14)),TW(v20,N(v11))),v17)
0.5;1.0;N(TW(N(TW(v14,v16)),N(TW(v5,TW(N(v7),v2)))))
0.25;1.0;TW(TW(N(v10),N(TW(v19,N(v28)))),N(TW(v18,N(v1))))
1.0;1.0;N(TW(TW(v25,N(v11)),N(TW(v27,TW(N(v20),N(v28))))))
0.0;1.0;TW(N(v5),TW(N(TW(N(v19),N(TW(v24,N(v9))))),v12))
0.0;1.0;TW(N(v16),N(TW(TW(N(v9),N(v3)),N(TW(N(v28),v4)))))
0.25;1.0;N(TW(TW(v19,v29),N(TW(N(v23),TW(v25,v18)))))
0.0;1.0;TW(TW(v12,N(v23)),TW(N(TW(N(v25),v9)),v15))
0.0;1.0;TW(TW(N(TW(v5,v23)),v27),N(TW(N(v10),N(v24))))
0.5;1.0;N(TW(N(TW(TW(N(v3),N(v1)),TW(N(v16),v25))),N(v23)))
0.0;1.0;TW(TW(v24,N(TW(TW(N(v5),v13),N(v0)))),v8)
0.0;1.0;TW(TW(v28,v16),TW(N(TW(v8,v26)),v27))
0.0;1.0;TW(TW(v6,v16),TW(N(TW(v10,v13)),N(v24)))
1.0;1.0;N(TW(TW(v1,N(v5)),N(v0)))
0.0;1.0;TW(N(TW(N(TW(v28,v6)),N(v25))),TW(v27,N(v8)))
0.0;1.0;N(TW(N(TW(N(v14),N(v12))),N(TW(TW(v13,v11),N(v29)))))
0.5;1.0;N(TW(N(TW(N(TW(N(v24),N(TW(v26,v27)))),v8)),N(v28)))
0.0;1.0;TW(N(TW(N(TW(N(v17),TW(v11,N(v7)))),N(v8))),v3)
1.0;1.0;N(TW(N(TW(v28,N(TW(v6,N(v13))))),TW(N(v20),v1)))
1.0;1.0;TW(N(TW(TW(v24,v25),v17)),N(TW(N(v13),N(v1))))
0.0;1.0;TW(N(TW(N(v10),N(TW(N(TW(v22,N(v16))),v0)))),v14)
0.75;1.0;N(TW(N(TW(N(TW(N(v8),N(v4))),v21)),N(TW(N(v23),v17))))
0.25;1.0;N(TW(v4,N(TW(N(TW(N(TW(v28,N(v3))),v10)),v14))))
1.0;1.0;N(TW(TW(N(TW(N(v2),N(v14))),N(v3)),TW(N(v15),v0)))
0.0;1.0;TW(TW(N(v24),TW(v19,N(TW(N(v29),N(v5))))),N(v15))
0.0;1.0;TW(N(v5),N(TW(TW(v13,v9),TW(N(v29),v4))))
0.75;1.0;TW(N(TW(N(v19),N(TW(N(v17),N(v9))))),N(TW(v25,N(v16))))
0.0;1.0;TW(v19,TW(N(TW(N(TW(v2,v12)),v29)),v3))
0.0;1.0;TW(TW(TW(N(v12),v7),N(v9)),N(TW(N(v17),v14)))
            """
#sat_clauses_gurobi(clauses0)
# formula_test = "((0.5 limplies 0.5) land 0.1)"
# sat_form(formula_test, "geq", 0) 