#!/usr/bin/python

class Var(object):
    def __init__(self, initial, step, min, max=None):
        self.initial = initial
        self.step = step
        if max is None:
            max = -min
        if min > max:
            min, max = max, min
        self.min = min
        self.max = max
        self.value = initial

    def next(self):
        value = self.value + self.step
        if value < self.min:
            value = self.min
            self.step = -self.step
        elif value > self.max:
            value = self.max
            self.step = -abs(self.step)
        self.value = value
        return value
