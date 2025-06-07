"""
This is the AST class hierarchy for the SATFuL
"""

from abc import ABC, abstractmethod

#class for Clauses
class Clauses(ABC) :
    def __init__(self, *clauses) :
        self.clauses = clauses
    
    def __str__(self) :
        return "\n".join(map(str, self.clauses))

    def add_clause(self, clause) :
        self.clauses.append(clause)

    def accept(self, visitor) :
        for cl in self.clauses : 
            cl.accept(visitor)

# Class for clause
class Clause(ABC) :
    """
    A basic class for a clause, a clause is a formula and an upper bound together with a lower bound
    """
    def __init__(self, lbound, ubound, form) :
        self.lbound = lbound
        self.ubound = ubound
        self.form = form
    
    def __str__(self) :
        return f"{self.lbound} <= {self.form} <= {self.ubound}"

    def __eq__(self, other) :
        return str(self) == str(other)

    def accept(self, visitor) :
        self.form.accept(visitor)

# Base class for all logical formulas
class Form(ABC):

    def __eq__(self, other) :
        return str(self) == str(other)

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def accept(visitor) :
        pass


# Represents a variable, e.g., "p" or "q"
class Var(Form):
    def __init__(self, name) :
        self.name = name

    def __str__(self):
        return self.name
    
    def accept(self, visitor) :
        visitor.visit_var(self)


# Represents a constant (a number in [0,1])
class Constant(Form):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def accept(self, visitor) :
        visitor.visit_constant(self)


# Base class for unary operations
class UnaryOperation(Form):
    def __init__(self, operand):
        self.operand = operand

    def accept(self, visitor) :
        self.operand.accept(visitor)
       

# Unary operation for luk. negation (lnot)
class Lnot(UnaryOperation):
    def __str__(self):
        return f"lnot {self.operand}"

    def accept(self, visitor) :
        super().accept(visitor)
        visitor.visit_lnot(self)


# Unary operation for product negation (pnot)
class Pnot(UnaryOperation):
    def __str__(self):
        return f"pnot {self.operand}"

    def accept(self, visitor) :
        super().accept(visitor)
        visitor.visit_pnot(self)
   

# Base class for binary operations
class BinaryOperation(Form):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor) :
        self.left.accept(visitor)
        self.right.accept(visitor)


# Binary operation for luk. conjunction (land)
class Land(BinaryOperation):
    def __str__(self):
        return f"({self.left} land {self.right})"

    def accept(self, visitor) :
        super().accept(visitor)
        visitor.visit_land(self)

# Binary operation for luk. disjunction (lor)
class Lor(BinaryOperation):
    def __str__(self):
        return f"({self.left} lor {self.right})"

    def accept(self, visitor) :
        super().accept(visitor)
        visitor.visit_lor(self)

# Binary operation for prod. conjunction (pand)
class Pand(BinaryOperation):
    def __str__(self):
        return f"({self.left} pand {self.right})"

    def accept(self, visitor) :
        super().accept(visitor)
        visitor.visit_pand(self)

# Binary operation for prod. disjunction (por)
class Por(BinaryOperation):
    def __str__(self):
        return f"({self.left} por {self.right})"

    def accept(self, visitor) :
        super().accept(visitor)
        visitor.visit_por(self)
   

# Binary operation for luk. imp (lor)
class Limp(BinaryOperation):
    def __str__(self):
        return f"({self.left} limp {self.right})"

    def accept(self, visitor) :
        super().accept(visitor)
        visitor.visit_limplies(self)

# Binary operation for product disjunction (lor)
class Pimp(BinaryOperation):
    def __str__(self):
        return f"({self.left} pimp {self.right})"
    
    def accept(self, visitor) :
        super().accept(visitor)
        visitor.visit_pimplies(self)

# Binary operation for max 
class Max(BinaryOperation):
    def __str__(self):
        return f"({self.left} max {self.right})"

    def accept(self, visitor) :
        super().accept(visitor)
        visitor.visit_max(self)

# Binary operation for Min 
class Min(BinaryOperation):
    def __str__(self):
        return f"({self.left} min {self.right})"

    def accept(self, visitor) :
        super().accept(visitor)
        visitor.visit_min(self)