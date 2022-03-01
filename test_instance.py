class Test:
    _num = 0

    def __init__(self, text):
        self.label = text
        self.nodes = {}

    def add_node(self):
        self.nodes[self._num] = []
        self._num += 1

    def __str__(self):
        return "nodes:{}".format(self.nodes)


t = Test("Hello")
t.add_node()
t.add_node()
t.add_node()
print(t)
print(t._num)
