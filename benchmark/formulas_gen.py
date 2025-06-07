"""
    Functions to generate random formulas
"""
import random
import sys
sys.path.append('../PL/')
from eval_visitor import EvalVisitor
import cl_parser as parser



file_path = "generatedforms" # by default the formulas are written in the folder generated formulas
num_forms = 100 # number of formulas to be generated
num_vars = 50 # number of vars in the formulas
num_cl = 50 # number of clauses
logic = "Product"
logics = ["L", "P", "G"]
vars_used = []

ops = {"L":["TW"], "P":["TP","IP"]}


def form_gen(p) : 
    """ 
        generates a formula with p vars
    """
    # base case
    if p == 1 :
        index = random.randint(1, num_vars)
        vars_used.append(f"""x{index}""")
        return f"""x{index}"""
    else :
        random_op = random.choice(ops[logic]) 
        random_bool = random.choice([True, False])
        #if random_op != "NP" and  random_op != "N" :
        if random_bool :
            # we choose a binary one
            rand_number = random.randint(1, p-1)
            return random_op+"("+form_gen(rand_number)+","+form_gen(p - rand_number)+")"
        else :
            # we choose the negation
            rand_number = random.randint(1, p-1)
            neg = "N" if logic == "L" else "NP"
            return neg+"("+random_op+"("+form_gen(rand_number)+","+form_gen(p - rand_number)+"))"
            return random_op+"("+form_gen(p-1)+")"
        
def val_gen() :
    """ it generates a random valuation using seed s
    """
    result = {}
    for v in vars :
        result[v] = random.random()
    return result

if __name__ == '__main__' :
    num_forms = int(sys.argv[1]) # number of formulas is the first argument
    num_vars = int(sys.argv[2])  # number of vars is the second argument
    #num_clauses = int(sys.argv[3])
    number_of_vars_in_form = int(sys.argv[3])
    logic = sys.argv[4] # the logic: L, P
    tool = sys.argv[5] # mniblos or satful
    #bounds = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1] 
    bounds = [0,0.25,0.5,0.75,1] 
    vars = [f"""x{i}""" for i in range(num_vars+1) if i>0] # the vars
    #for i in range(num_forms) :
    i = 0
    for i in range(num_forms) :
        file = open(file_path+f"""/form{i}.txt""", "w")
        vars_used = []
        #for j in range(num_clauses) :
        while set(vars_used) != set(vars) :
            #print(vars_used)
            #print(vars)
            # a formula is generated
            form_string = form_gen(number_of_vars_in_form)
            ast = parser.parse("0;1;"+form_string)
            form = ast.clauses[0].form

            # we generate two valuations
            val1 = val_gen() 
            val2 = val_gen()
            #print(val1)
            #print(val2)

            # the first valuation is used
            eval1 = EvalVisitor(val1)
            form.accept(eval1)
            value1 = eval1.form_valuation[str(form)]

            # the second valuation is used
            eval2 = EvalVisitor(val2)
            form.accept(eval2)
            value2 = eval2.form_valuation[str(form)]

            lbound0 = max([b for b in bounds if b <= value1])
            lbound1 = min([b for b in bounds if b >= value2])
            lbound = random.choice([lbound0,lbound1])
            ubound = random.choice([b for b in bounds if b >= lbound])


            #lbound = random.choice(bounds)
            cond = random.choice([True,False])
            if cond :
                file.write(f"""{lbound};{1};{form_string}\n""")
            else :
                file.write(f"""{0};{ubound};{form_string}\n""")
        



