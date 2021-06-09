

class Stack(object):

    # region Constructer
    def __init__(self):

        self.stack = []
        self.length = 0
    # endregion

    # region Methods
    # pushes an item into the stack
    def push(self, item):

        self.stack.append(item)
        self.length += 1

    def pop(self):

        if self.length > 0:
            self.length -= 1
            return self.stack.pop(self.length)

        return "No items in the stack"

    def __str__(self):

        return str(self.stack)
    # endregion