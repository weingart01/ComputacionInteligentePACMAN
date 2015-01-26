__author__ = 'Usuario'



# Create example data and heapify
a = range(10)
a.reverse()
heapq.heapify(a)
print a

# remove an element and heapify again
a.remove(5)
heapq.heapify(a)
print a
