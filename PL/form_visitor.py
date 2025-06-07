from abc import ABC, abstractmethod

#Visitor interface for formula
class FormVisitor(ABC):
    @abstractmethod
    def visit_constant(self, cons) :
        pass

    @abstractmethod
    def visit_var(self, var) :
        pass

    @abstractmethod
    def visit_land(self, land) :
        pass

    @abstractmethod
    def visit_lor(self, lor) :
        pass

    @abstractmethod
    def visit_pand(self, pand) :
        pass
    
    @abstractmethod
    def visit_por(self, por) :
        pass

    @abstractmethod
    def visit_pimplies(self, pimplies) :
        pass

    @abstractmethod
    def visit_limplies(self, limplies) :
        pass

    @abstractmethod
    def visit_lnot(self, lnot) :
        pass

    @abstractmethod
    def visit_pnot(self, pnot) :
        pass

    @abstractmethod
    def visit_max(self, max) :
        pass

    @abstractmethod
    def visit_min(self, min) :
        pass

   


    