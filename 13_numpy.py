import numpy as np

#vamos criar um array (vetor)

arr = np.array([1, 2, 3, 4, 5])

print(f'Array: {arr}')

#multiplicar array

print(arr * 2)

#somando array

arr2 = np.array([10, 20, 30, 40, 50])
print(arr + arr2)

#vamos criar uma matriz 2d

matriz = np.array([[1,2,3] , [4,5,6]])
print(matriz)

#transposta da matriz
print(matriz.T)

#gerando matriz com valores aleatorias
print(np.random.rand(3,3))