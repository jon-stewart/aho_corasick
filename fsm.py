#!/usr/bin/python

class Node():

    def __init__(self, state, depth, c, fail):
        self.state  = state
        self.c      = c 
        self.output = ""
        self.depth  = depth
        self.branch = {}
        self.fail   = fail


    def goto(self, c):
        '''
        If a branch node exists for the character return it
        '''
        if c in self.branch.keys():
            return self.branch[c]
        else:
            return None


    def insert(self, node):
        '''
        Create a new node, add it as a branch and return it.
        '''
        self.branch[node.c] = node
        return node


    def dump(self):
        '''
        '''
        s = self.state
        d = self.depth
        c = self.c
        o = self.output
        f = ''

        if self.fail:
            f = self.fail.state

        b = []
        for k in self.branch:
            b.append(k)

        print("s:{0} | d:{1} | c:{2} | f:{3} | b:{4} | {5}".format(s, d, c, f, b, o))

        for k,v in self.branch.items():
            v.dump()


class Fsm():
    '''
    Finite state machine with trie structure.

    This is based off the aho-corasick dictionary string matching algorithm.
    '''

    def __init__(self):
        self.state = 0
        self.base = Node(0, 0, '', None)
        self.alphabet = ""


    def construct(self, words):
        '''
        '''
        self.alphabet = "".join(words)

        self.__construct_goto(words)

        self.__construct_fail()


    def __construct_goto(self, words):
        '''
        Construct the goto transitions of the finite state machine

        For each word in the list traverse the trie, if no branch is available
        then create a new one outwards for each of the remaining characters.
        '''
        for word in words:
            node  = self.base

            for i,c in enumerate(word):
                if node.goto(c):
                    node = node.goto(c)
                else:
                    self.state += 1
                    node = node.insert(Node(self.state, i + 1, c, self.base))

            node.output = word


    def __construct_fail(self):
        '''
        Construct the failure transitions of the finite state machine.

        For each node find another node in the tree that has a matching suffix
        and a valid goto transition.
        '''
        stack = []
        stack.append(self.base)
        while len(stack):
            node = stack.pop(0)
            for c in self.alphabet:
                if node.goto(c):
                    nxt = node.goto(c)
                    f   = node.fail

                    while f and not f.goto(c):
                        f = f.fail

                    if f:
                        nxt.fail = f.goto(c)
                    else:
                        nxt.fail = self.base

                    if f and f.fail and f.fail.output:
                        nxt.output = f.fail.output

                    stack.append(nxt)


    def dump(self):
        '''
        Kick off the recursive printing of trie nodes
        '''
        print("-------------------")
        self.base.dump()


if __name__ == "__main__":
    fsm = Fsm()

    ls = []
    ls.append("hers")
    ls.append("his")
    ls.append("she")
    ls.append("he")
    ls.append("sh")
    ls.append("shes")

    fsm.construct(ls)

    fsm.dump()
