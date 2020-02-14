import random

class Gene(object):
    def __init__(self, _name, _range):
        self.name = _name
        self.value_range = _range
        self.value = self.pickRandomValue()
    
    def pickRandomValue(self):
        return random.choice(self.value_range)