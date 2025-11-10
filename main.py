from estructuras import Stack, Queue

def main() -> None:
  myStack = Stack()
  myStack.push('A')
  myStack.push('B')
  myStack.push('C')

  print("Pop: ", myStack.pop())
  print("Peek: ", myStack.peek())
  print("isEmpty: ", myStack.isEmpty())
  print("Size: ", myStack.stackSize())

  myQueue = Queue()

  myQueue.enqueue('A')
  myQueue.enqueue('B')
  myQueue.enqueue('C')
  print("Queue: ", myQueue.queue)

  print("Dequeue: ", myQueue.dequeue())

  print("Peek: ", myQueue.peek())

  print("isEmpty: ", myQueue.isEmpty())

  print("Size: ", myQueue.size())

if __name__ == "__main__":
  main()