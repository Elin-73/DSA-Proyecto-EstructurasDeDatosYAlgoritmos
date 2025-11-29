from collections import deque

class Stack:
    def __init__(self):
        self.stack = []
    
    def push(self, element):
        self.stack.append(element)
    
    def pop(self):
        if self.isEmpty():
            return "Stack is empty"
        return self.stack.pop()
    
    def peek(self):
        if self.isEmpty():
            return "Stack is empty"
        return self.stack[-1]
    
    def isEmpty(self):
        return len(self.stack) == 0
    
    def size(self):
        return len(self.stack)
    
    def toList(self):
        stackList = ""
        for i in range(self.size()-1, -1, -1):
            stackList += f"│  #{i} Item: {self.stack[i]}  │\n"
            stackList += "├─────┤\n"
        return stackList


class Queue:
    def __init__(self):
        self.queue = []
    
    def enqueue(self, element):
        self.queue.append(element)
    
    def dequeue(self):
        if self.isEmpty():
            return "Queue is empty"
        return self.queue.pop(0)
    
    def peek(self):
        if self.isEmpty():
            return "Queue is empty"
        return self.queue[0]
    
    def isEmpty(self):
        return len(self.queue) == 0
    
    def size(self):
        return len(self.queue)
    
    def toList(self):
        queueList = ""
        queueList += "Caja"
        for i in range(self.size()):
            queueList += f"<- #{i} Item: {self.queue[i]}|"
        return queueList


class Tree:
    class TreeNode:
        def __init__(self, data):
            self.data = data
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = self.TreeNode(value)
        if self.root is None:
            self.root = new_node
            return new_node
        current = self.root
        while True:
            if value <= current.data:
                if current.left is None:
                    current.left = new_node
                    return new_node
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    return new_node
                current = current.right

    # Get inorder successor (smallest in right subtree)
    def getSuccessor(self, curr):
        curr = curr.right
        while curr is not None and curr.left is not None:
            curr = curr.left
        return curr

    # Delete a node with value x from BST
    def delNode(self, root, x):
        if root is None:
            return root

        if root.data > x:
            root.left = self.delNode(root.left, x)
        elif root.data < x:
            root.right = self.delNode(root.right, x)
        else:
            
            # node with 0 or 1  children
            if root.left is None:
                return root.right
            if root.right is None:
                return root.left
            
            #  Node with 2 children
            succ = self.getSuccessor(root)
            root.data = succ.data
            root.right = self.delNode(root.right, succ.data)

        return root

    def getHeight(self, root, h):
        if root is None:
            return h - 1
        return max(self.getHeight(root.left, h + 1),
                self.getHeight(root.right, h + 1))

    # Return level-order as array [root, left, right, ...] (None for missing nodes)
    def levelOrder(self, root):
        if root is None:
            return []

        height = self.getHeight(root, 0)
        q = deque()
        q.append((root, 0))
        result = []

        while q:
            node, lvl = q.popleft()
            if lvl > height:
                break

            if node is None:
                result.append(None)
                continue

            result.append(node.data)

            # only enqueue children if we haven't reached max height
            if lvl < height:
                q.append((node.left, lvl + 1))
                q.append((node.right, lvl + 1))

        # trim trailing None values for a compact representation
        while result and result[-1] is None:
            result.pop()

        return result

    def preOrderTraversal(self, node):
        if node is None:
            return "Tree is empty"
        print(node.data, end=", ")
        self.preOrderTraversal(node.left)
        self.preOrderTraversal(node.right)

    def inOrderTraversal(self, node):
        if node is None:
            return
        self.inOrderTraversal(node.left)
        print(node.data, end=", ")
        self.inOrderTraversal(node.right)

    def postOrderTraversal(self, node):
        if node is None:
            return
        self.postOrderTraversal(node.left)
        self.postOrderTraversal(node.right)
        print(node.data, end=", ")

    def search(self, node, target):
        if node is None:
            return None 
        elif node.data == target:
            return node
        elif target < node.data:
            return self.search(node.left, target)
        else:
            return self.search(node.right, target)


class CircularList:
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None
    
    def __init__(self):
        self.size = 0
        self.head = None
    
    def push(self, data):
        new_node = self.Node(data)
        
        if self.head is None:
            self.head = new_node
            new_node.next = self.head
            self.size += 1
            return new_node
        
        current = self.head
        while current.next != self.head:
            current = current.next
        
        current.next = new_node
        new_node.next = self.head
        self.size += 1
        return new_node
    
    def insert_at(self, position, data):
        if position < 0 or position > self.size:
            return "Invalid position"
        
        if position == 0:
            new_node = self.Node(data)
            
            if self.head is None:
                self.head = new_node
                new_node.next = self.head
            else:
                current = self.head
                while current.next != self.head:
                    current = current.next
                
                new_node.next = self.head
                current.next = new_node
                self.head = new_node
            
            self.size += 1
            return new_node
        
        if position == self.size:
            return self.push(data)
        
        new_node = self.Node(data)
        current = self.head
        
        for i in range(position - 1):
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
        self.size += 1
        return new_node
    
    def pop(self):
        if self.head is None:
            return "List is Empty!"
        
        if self.size == 1:
            data = self.head.data
            self.head = None
            self.size = 0
            return data
        
        current = self.head
        while current.next != self.head:
            current = current.next
        
        data = self.head.data
        current.next = self.head.next
        self.head = self.head.next
        self.size -= 1
        return data
    
    def delete_at(self, position):
        if self.head is None:
            return "List is Empty!"
        
        if position < 0 or position >= self.size:
            return "Invalid position"
        
        if position == 0:
            return self.pop()
        
        current = self.head
        for i in range(position - 1):
            current = current.next
        
        deleted_data = current.next.data
        
        current.next = current.next.next
        self.size -= 1
        return deleted_data
    
    def get_at(self, position):
        if self.head is None or position < 0 or position >= self.size:
            return None
        
        current = self.head
        for i in range(position):
            current = current.next
        
        return current.data
    
    def display(self):
        if self.head is None:
            return "Lista vacía"
        
        result = []
        current = self.head
        
        while True:
            result.append(str(current.data))
            current = current.next
            if current == self.head:
                break
        
        return " → ".join([f"[{item}]" for item in result]) + f" → [vuelve a {self.head.data}] ↻"
    
    def traverse(self):
        if self.head is None:
            return []
        
        result = []
        current = self.head
        
        while True:
            result.append(current.data)
            current = current.next
            if current == self.head:
                break
        
        return result
    
    def is_empty(self):
        return self.head is None
    
    def get_size(self):
        return self.size