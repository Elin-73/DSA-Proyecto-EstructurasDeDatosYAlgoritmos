class Stack:
		class Node:
				def __init__(self, value):
						self.value = value
						self.next = None
		def __init__(self):
				self.head = None
				self.size = 0
		
		def push(self, value):
				new_node = self.Node(value)
				if self.head:
						new_node.next = self.head
				self.head = new_node
				self.size += 1
		
		def pop(self):
				if self.isEmpty():
						return "Stack is empty"
				popped_node = self.head
				self.head = self.head.next
				self.size -= 1
				return popped_node.value
		
		def peek(self):
				if self.isEmpty():
						return "Stack is empty"
				return self.head.value
		
		def isEmpty(self):
				return self.size == 0
		
		def stackSize(self):
				return self.size
		
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

class TreeNode:
  def __init__(self, data):
    self.data = data
    self.left = None
    self.right = None