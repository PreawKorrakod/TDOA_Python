import math

x1, y1 = 0.035, 0.025
x2, y2 = 0.21, 0.26
x3, y3 = 0.38, 0.025



def calDistance(tx,ty):

    tx,ty = tx / 100, ty/ 100

    x1, y1 = 0.035, 0.025
    x2, y2 = 0.21, 0.26
    x3, y3 = 0.38, 0.025

    d1 = math.sqrt((x1 - tx)**2 + (y1 - ty)**2)
    d2 = math.sqrt((x2 - tx)**2 + (y2 - ty)**2)
    d3 = math.sqrt((x3 - tx)**2 + (y3 - ty)**2)

    return d1, d2, d3




tx = float(input("input tx: "))
ty = float(input("input ty: "))

value = calDistance(tx, ty)

print(value)