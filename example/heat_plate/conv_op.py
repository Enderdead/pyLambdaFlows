from pyLambdaFlows.dispenser import Dispenser
from pyLambdaFlows.op import Operation
class ConvDispenser(Dispenser):

    def distribute(self, size):
        result = [list() for _ in range(size)]
        for _ in range(3):
            result[0].append(0)
            result[-1].append(size-1)
        for index in range(1, size-1):
            result[index].append(index-1)
            result[index].append(index)
            result[index].append(index+1)
        return result

class ConvOp(Operation):
    def __init__(self, parent, funct, name=None ):
        Operation.__init__(self, parent, funct, ConvDispenser(), name=name)

if __name__ == "__main__":
    print(ConvDispenser().distribute(5))