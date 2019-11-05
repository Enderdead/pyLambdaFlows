from dispenser import *



class Operation():
    def __init__(self, parent, funct, topologie, name=None):
        self.terminal = isinstance(parent, Operation)
        self.parent = parent
        self.funct = funct

        if(not isinstance(topologie, Dispenser)):
            raise AttributeError("You must provide  a Dispenser inherited class as a topologie arg")
        
        self.dispenser = topologie
        self.name = name

    def compile(self):
        " This function send this lambda op in AWS service"
        pass

    def eval(self):
        " Call this operation"
        pass

class Map(Operation):
    def __init__(self, parent, funct, name=None):
        super().__init__(parent, funct, DMap(), name=name)



if __name__ == "__main__":
    pass
