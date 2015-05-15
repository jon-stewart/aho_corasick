#!/usr/bin/python

class Node():

    def __init__(self, state, depth, c):
        self.state  = state
        self.c      = c 
        self.output = ""
        self.depth  = depth
        self.branch = {}

    def add_output(self, output):
        self.output = output

    def goto(self, c):
        if c in self.branch.keys():
            return self.branch[c]
        else:
            return None

    def insert(self, state, depth, c):
        node = Node(state, depth, c)
        self.branch[c] = node
        return node

    def dump(self):
        print(self.state, self.depth, self.c, self.branch.keys(), self.output)
        for k,v in self.branch.items():
            v.dump()


class Fsm():

    def __init__(self):
        self.state = 0
        self.base = Node(0, 0, '')

    def construct(self, words):
        for word in words:
            i     = 0
            depth = 0
            node  = self.base

            while node.goto(word[i]):
                node = node.goto(word[i])
                i += 1

            depth = i
            for c in word[i:]:
                self.state += 1
                depth += 1
                node = node.insert(self.state, depth, c)

            node.add_output(word)

    def dump(self):
        self.base.dump()


if __name__ == "__main__":
    fsm = Fsm()

    ls = []
    ls.append("only")
    ls.append("onyx")
    ls.append("dunmps")
    ls.append("dala")

    fsm.construct(ls)

    fsm.dump()
