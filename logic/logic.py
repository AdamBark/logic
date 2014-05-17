class TwoInOneOutGate:
    def __init__(self, out_link=None):
        self.in1 = None
        self.in2 = None
        self.out_link = out_link

    def connect_inputs(self, one=None, two=None):
        if one:
            self.in1 = one
        if two:
            self.in2 = two
        if self.in_1 and self.in_2:
            self.out_link(self.process)
            
    def connect_inputs(self, **kwargs):
        pass

class AND(TwoInOneOutGate):
    def process(self):
        return self.in_1 and self.in_2

class OR(TwoInOneOutGate):
    def process(self):
        return self.in_1 or self.in_2
