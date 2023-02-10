class linkedlist:

    def __init__(self):
        self.head = None
        self.last = None
        
    def append(self, num):
        newNode = node(num)
        if self.head is None:
            self.head = newNode
            self.last = newNode
        else:
            self.last.next = newNode
            self.last = newNode

    def __repr__(self):
        s = ""
        curr = self.head
        while curr != None:
            s += str(curr.num) + " "
            curr = curr.next
        return s

class node:
    
    def __init__(self, n):
        self.num = n
        self.next = None

class cell:
    
    def __init__(self):
        self.n = None

    def give(self, obj):
        self.n = obj
