

class Dispenser():
    """
    This class will explain data dependancies over two layers
    """
    def distribute(self, size):
        """
            Function computing the next layer dependancies.
        """
        pass

    def __call__(self, size):
        return self.distribute(size)


class DHardReduce(Dispenser):
    def distribute(self, size):
        return [list(range(size)),]

class DMap(Dispenser):
    def distribute(self, size):
        return [ [i,] for i in range(size) ]



if __name__ == "__main__":
    pass
