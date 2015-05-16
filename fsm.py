#!/usr/bin/python

class Node():

    def __init__(self, state, depth, c):
        self.state  = state
        self.c      = c 
        self.output = ""
        self.depth  = depth
        self.branch = {}
        self.fail   = None

    def goto(self, c):
        '''
        If a branch node exists for the character return it
        '''
        if c in self.branch.keys():
            return self.branch[c]
        else:
            return None

    def insert(self, state, depth, c):
        '''
        Create a new node, add it as a branch and return it
        '''
        node = Node(state, depth, c)
        self.branch[c] = node
        return node

    def dump(self):
        '''
        '''
        s = self.state
        d = self.depth
        c = self.c
        o = self.output

        if self.fail:
            fail  = self.fail.state

        b = []
        for k in self.branch:
            b.append(k)

        print("s:{0} | d:{1} | c:{2} | b:{3} | {4}".format(s, d, c, b, o))

        for k,v in self.branch.items():
            v.dump()


class Fsm():
    '''
    Finite state machine with trie structure.

    This is based off the aho-corasick dictionary string matching algorithm.
    '''

    def __init__(self):
        self.state = 0
        self.base = Node(0, 0, '')
        self.alphabet = ""

    def construct(self, words):

        self.alphabet = "".join(words)

        self.__construct_goto(words)

        #self.__construct_fail()

    def __construct_goto(self, words):
        '''
        Construct the finite state machine

        For each word in the list traverse the trie, if no branch is available
        then create a new one outwards for each of the remaining characters.
        '''
        for word in words:
            node  = self.base

            for i,c in enumerate(word):
                if node.goto(c):
                    node = node.goto(c)
                else:
                    break

            depth = i
            if i < (len(word) - 1):
                for c in word[i:]:
                    self.state += 1
                    depth += 1
                    node = node.insert(self.state, depth, c)

            node.output = word

    def __construct_fail(self):
        '''
        '''
        ls = []
        ls.append(self.base)
        while len(ls):
            node = ls.pop(0)
            for c in self.alphabet:
                if node.goto(c):
                    nxt = node.goto(c)
                    s   = node.fail

                    while s and not s.goto(c):
                        s = s.fail

                    if s:
                        nxt.fail = s
                    else:
                        nxt.fail = self.base

                    if s and s.fail and s.fail.output:
                        nxt.output = s.fail.output

                    ls.append(nxt)


    def dump(self):
        '''
        Kick off the recursive printing of trie nodes
        '''
        print("-------------------")
        self.base.dump()


if __name__ == "__main__":
    fsm = Fsm()

    ls = []
#    ls.append("python")
    ls.append("main")
    #ls.append("manic")
#    ls.append("pythonic")
    ls.append("ma")

    fsm.construct(ls)

    fsm.dump()
