class Linked_list:
    def __init__ (self, head):
        self.head = head
    def print(self):
        node_now = self.head
        while node_now.next != None:
            print(node_now.data, end = " ")
            node_now = node_now.next
        print(node_now.data)

    def length(self):
        node_now = self.head
        i = 1
        while node_now.next != None:
            node_now = node_now.next
            i += 1
        return i

    def append (self, Node):
        node_now = self.head
        while node_now.next != None:
            node_now = node_now.next
        node_now.next = Node
    
    def pop(self):
        self.head = self.head.next
    
    def erase(self, n): # erase n-th element, start with 0
        i = 0
        node_now = self.head
        while i < n - 1:
            node_now = node_now.next
            if node_now == None:
                return False
            i += 1
        if node_now.next == None:
            return False
        node_now.next = node_now.next.next

class Node:
    def __init__ (self, data):
        self.data = data
        self.next = None
        
head = Node(0)
ls = Linked_list(head)
for i in range(10):
    n = Node(i + 1)
    ls.append(n)

print()
print(ls.length())
ls.erase(5)
print()
ls.print()
print()
print(ls.length())
