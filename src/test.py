import numpy

list1 = numpy.array([[1,2,3],[1,1,2],[3,2,1]])

list2 = numpy.array([[3,3,3]])

result = numpy.append(list1, list2, axis=0)

print(result)