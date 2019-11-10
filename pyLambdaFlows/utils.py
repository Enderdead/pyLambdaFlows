

class Tree():

class InstanceNode():
    def __init__(self, funct, args, idx, parent=None, children=None):
        self.funct = funct
        self.args = args
        self.idx = idx
        self.parent = None
        self.children = None