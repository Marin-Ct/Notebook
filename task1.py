"""
Task 1: Queue Abstract Classes
Implements Queue interface and three concrete implementations with tests.
"""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional
import unittest

T = TypeVar('T')


class Queue(ABC, Generic[T]):
    """Abstract Queue interface that all queue implementations must follow."""
    
    @abstractmethod
    def enqueue(self, item: T) -> None:
        """Add an item to the queue."""
        pass
    
    @abstractmethod
    def dequeue(self) -> Optional[T]:
        """Remove and return the front item from the queue."""
        pass
    
    @abstractmethod
    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        pass
    
    @abstractmethod
    def size(self) -> int:
        """Return the number of items in the queue."""
        pass


class ListQueue(Queue[T]):
    """Simple list-based queue implementation (FIFO)."""
    
    def __init__(self):
        self._items: List[T] = []
    
    def enqueue(self, item: T) -> None:
        self._items.append(item)
    
    def dequeue(self) -> Optional[T]:
        if self.is_empty():
            return None
        return self._items.pop(0)
    
    def is_empty(self) -> bool:
        return len(self._items) == 0
    
    def size(self) -> int:
        return len(self._items)


class CircularQueue(Queue[T]):
    """Circular queue implementation with fixed capacity."""
    
    def __init__(self, capacity: int = 100):
        self._capacity = capacity
        self._items: List[Optional[T]] = [None] * capacity
        self._front = 0
        self._rear = 0
        self._size = 0
    
    def enqueue(self, item: T) -> None:
        if self._size >= self._capacity:
            raise OverflowError("Queue is full")
        self._items[self._rear] = item
        self._rear = (self._rear + 1) % self._capacity
        self._size += 1
    
    def dequeue(self) -> Optional[T]:
        if self.is_empty():
            return None
        item = self._items[self._front]
        self._items[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return item
    
    def is_empty(self) -> bool:
        return self._size == 0
    
    def size(self) -> int:
        return self._size


class LinkedQueue(Queue[T]):
    """Linked list-based queue implementation."""
    
    class _Node:
        def __init__(self, data: T):
            self.data = data
            self.next: Optional['LinkedQueue._Node'] = None
    
    def __init__(self):
        self._head: Optional[LinkedQueue._Node] = None
        self._tail: Optional[LinkedQueue._Node] = None
        self._size = 0
    
    def enqueue(self, item: T) -> None:
        new_node = self._Node(item)
        if self._tail is None:
            self._head = self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1
    
    def dequeue(self) -> Optional[T]:
        if self.is_empty():
            return None
        item = self._head.data
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return item
    
    def is_empty(self) -> bool:
        return self._head is None
    
    def size(self) -> int:
        return self._size


# TESTS
class TestQueueImplementations(unittest.TestCase):
    """Test all queue implementations with integers and strings."""
    
    def test_list_queue_with_integers(self):
        queue = ListQueue[int]()
        self.assertTrue(queue.is_empty())
        self.assertEqual(queue.size(), 0)
        
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
        
        self.assertFalse(queue.is_empty())
        self.assertEqual(queue.size(), 3)
        
        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual(queue.dequeue(), 2)
        self.assertEqual(queue.size(), 1)
        self.assertEqual(queue.dequeue(), 3)
        self.assertTrue(queue.is_empty())
        self.assertIsNone(queue.dequeue())
    
    def test_list_queue_with_strings(self):
        queue = ListQueue[str]()
        queue.enqueue("first")
        queue.enqueue("second")
        queue.enqueue("third")
        
        self.assertEqual(queue.dequeue(), "first")
        self.assertEqual(queue.dequeue(), "second")
        self.assertEqual(queue.dequeue(), "third")
    
    def test_circular_queue_with_integers(self):
        queue = CircularQueue[int](capacity=3)
        queue.enqueue(10)
        queue.enqueue(20)
        queue.enqueue(30)
        
        self.assertEqual(queue.size(), 3)
        with self.assertRaises(OverflowError):
            queue.enqueue(40)
        
        self.assertEqual(queue.dequeue(), 10)
        queue.enqueue(40)
        self.assertEqual(queue.dequeue(), 20)
        self.assertEqual(queue.dequeue(), 30)
        self.assertEqual(queue.dequeue(), 40)
        self.assertTrue(queue.is_empty())
    
    def test_linked_queue_with_integers(self):
        queue = LinkedQueue[int]()
        queue.enqueue(100)
        queue.enqueue(200)
        queue.enqueue(300)
        
        self.assertEqual(queue.size(), 3)
        self.assertEqual(queue.dequeue(), 100)
        self.assertEqual(queue.dequeue(), 200)
        self.assertEqual(queue.size(), 1)
        self.assertEqual(queue.dequeue(), 300)
        self.assertIsNone(queue.dequeue())
    
    def test_linked_queue_with_strings(self):
        queue = LinkedQueue[str]()
        queue.enqueue("alpha")
        queue.enqueue("beta")
        
        self.assertEqual(queue.dequeue(), "alpha")
        queue.enqueue("gamma")
        self.assertEqual(queue.dequeue(), "beta")
        self.assertEqual(queue.dequeue(), "gamma")
        self.assertTrue(queue.is_empty())
    
    def test_all_queues_polymorphism(self):
        """Test that all implementations work polymorphically."""
        queues: List[Queue[int]] = [
            ListQueue[int](),
            CircularQueue[int](10),
            LinkedQueue[int]()
        ]
        
        for queue in queues:
            queue.enqueue(1)
            queue.enqueue(2)
            self.assertEqual(queue.dequeue(), 1)
            self.assertEqual(queue.dequeue(), 2)
            self.assertTrue(queue.is_empty())


if __name__ == "__main__":
    unittest.main()
