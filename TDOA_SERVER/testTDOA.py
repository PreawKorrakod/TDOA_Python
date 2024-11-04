import numpy as np
import math

# ความเร็วเสียง (สมมุติเป็น 343 m/s ในอากาศ)
v = 343

x1, y1 = 0, 0
x2, y2 = 0.5 ,1
x3, y3 = 1, 0


def calDistance(tx,ty):

    tx,ty = tx / 100, ty/ 100

    d1 = math.sqrt((x1 - tx)**2 + (y1 - ty)**2)
    d2 = math.sqrt((x2 - tx)**2 + (y2 - ty)**2)
    d3 = math.sqrt((x3 - tx)**2 + (y3 - ty)**2)

    return d1, d2, d3

def calculatePosition(tx, ty):
    data = calDistance(tx, ty)

    d1 = data[0]  
    d2 = data[1] 
    d3 = data[2]   


    print(d1,d2,d3)


    A = np.array( [[ 2 * (x1 - x3), 2 * (y1 - y3)],
                   [ 2 * (x1 - x2), 2 * (y1 - y2)]] )

    b = np.array([(d3**2-d1**2-x3**2+x1**2-y3**2+y1**2), (d2**2-d1**2-x2**2+x1**2-y2**2+y1**2)])

    solution = np.linalg.solve(A, b)

    return solution

tx = float(input("tx: "))
ty = float(input("ty: "))

point = calculatePosition(tx, ty)
print(point[0], point[1])
