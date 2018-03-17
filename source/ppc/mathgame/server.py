#!/usr/bin/env python
# -*- coding=utf-8 -*-

from Crypto.Util.number import isPrime,getPrime
from hashlib import sha256
import threading
import random
import time
import sys
import signal
import itertools
import pdb
import z3, os

flag = "N1CTF{This_1s_a_1j_Math_Game4!}"
bit_len = 32
num_len = len(str(2**(bit_len+1)-1))
factorial = 7
stop = 0

# generate 7*7 matrix
def genNPrimeMatrix():
    num = []
    for x in range(factorial):
        tmp_num = [getNotPrime(bit_len) for y in range(factorial)]
        num.append(tmp_num)
    return num

def genPrimeMatrix():
    num = []
    for x in range(factorial):
        tmp_num = [getPrime(bit_len) for y in range(factorial)]
        num.append(tmp_num)
    return num

def genOddMatrix():
    num = []
    for x in range(factorial):
        tmp_num = [getOdd(bit_len) for y in range(factorial)]
        num.append(tmp_num)
    return num
    
def genEvenMatrix():
    num = []
    for x in range(factorial):
        tmp_num = [getEven(bit_len) for y in range(factorial)]
        num.append(tmp_num)
    return num

def getDPrimeMatrix():
    num = []
    for x in range(factorial):
        tmp_num = [getPrime(bit_len/2)*getPrime(bit_len/2) for y in range(factorial)]
        num.append(tmp_num)
    return num

def getOdd(n):
    while True:
        r = random.randint(2**n,2**(n+1)-1)
        if r % 2 == 1:
            break
    return r

def getTPrime(n):
    return getPrime(n/3)*getPrime(n/3)*getPrime(n/3)

def getEven(n):
    while True:
        r = random.randint(2**n,2**(n+1)-1)
        if r % 2 == 0:
            break
    return r

def getNotPrime(n):
    while True:
        r = random.randint(2**n,2**(n+1)-1)
        if not isPrime(r) and r % 2 == 1:
            break
    return r

# get Line general equation
def calLineEqut(A, B):
    t = z3.Real('t')
    x = (B[0] - A[0])*t + A[0] + 0.5
    y = (B[1] - A[1])*t + A[1] + 0.5
    z = (B[2] - A[2])*t + A[2] + 0.5
    return [x, y, z]
    # while True:
    #     C = getLinePonit(A, B)
    #     if C:
    #         break
    # while True:
    #     D = getLinePonit(A, B)
    #     if D and D != C:
    #         break
    # a, b, c, d = z3.Reals('a b c d')
    # cal = z3.Solver()
    # formula1 = A[0]*a + A[1]*b + A[2]*c + d == 0
    # formula2 = B[0]*a + B[1]*b + B[2]*c + d == 0
    # formula3 = C[0]*a + C[1]*b + C[2]*c + d == 0
    # formula4 = D[0]*a + D[1]*b + D[2]*c + d == 0
    # cal.add(formula1)
    # cal.add(formula2)
    # cal.add(formula3)
    # cal.add(formula4)
    # if C[0] != D[0]:
    #     cal.add(a != 0)
    # else:
    #     cal.add(a == C[0])
    # if C[1] != D[1]:
    #     cal.add(b != 0)
    # else:
    #     cal.add(b == C[1])
    # if C[2] != D[2]:
    #     cal.add(c != 0)
    # else:
    #     cal.add(c == C[2])
    # if cal.check() != z3.sat:
    #     # print(cal)
    #     return False
    # m = cal.model()
    # return [m[a], m[b], m[c], m[d]]

# get a Line other Point
def getLinePonit(A, B):
    x, y, z = z3.Ints('x y z')
    cal = z3.Solver()
    formula1 = (x - A[0]) * (B[1] - A[1]) == (y - A[1]) * (B[0] - A[0])
    formula2 = (x - A[0]) * (B[2] - A[2]) == (z - A[2]) * (B[0] - A[0])
    formula3 = (z - A[2]) * (B[1] - A[1]) == (y - A[1]) * (B[2] - A[2])
    if  A[0] - B[0] != 0 and A[1] - B[1] != 0 and A[2] - B[2] != 0:
        cal.add(formula1)
        cal.add(formula2)
        cal.add(formula3)
    if A[0] - B[0] == 0:
        cal.add(x == A[0])
        cal.add(formula3)
    if A[1] - B[1] == 0:
        cal.add(y == A[1])
        cal.add(formula2)
    if A[2] - B[2] == 0:
        cal.add(z == A[2])
        cal.add(formula1)
    if A[0] - B[0] != 0:
        while True:
            tmp = random.randint(10, 200)
            if tmp != A[0] and tmp != B[0]:
                break
        cal.add(x == tmp)
    elif A[1] - B[1] != 0:
        while True:
            tmp = random.randint(10, 200)
            if tmp != A[1] and tmp != B[1]:
                break
        cal.add(y == tmp)
    elif A[2] - B[2] != 0:
        while True:
            tmp = random.randint(10, 200)
            if tmp != A[2] and tmp != B[2]:
                break
        cal.add(z == tmp)
    else:
        return False
    if cal.check() != z3.sat:
        # print(cal)
        return False
    m = cal.model()
    return [m[x].as_long(), m[y].as_long(), m[z].as_long()]

def calFocus(lineAB, lineCD):
    # x, y, z, t = z3.Reals('x y z t')
    # cal = z3.Solver()
    # cal.add(x>=0)
    # cal.add(y>=0)
    # cal.add(z>=0)
    # cal.add(x<=(factorial-1))
    # cal.add(y<=(factorial-1))
    # cal.add(z<=(factorial-1))
    # lineAB_Equ = calLineEqut(lineAB[0], lineAB[1])
    # lineCD_Equ = calLineEqut(lineCD[0], lineCD[1])
    # if not lineAB_Equ or not lineCD_Equ:
    #     return False
    # cal.add(lineAB_Equ[0] == lineCD_Equ[0])
    # cal.add(lineAB_Equ[1] == lineCD_Equ[1])
    # cal.add(lineAB_Equ[2] == lineCD_Equ[2])
    # if cal.check() != z3.sat:
    #     # print(cal)
    #     return False
    # m = cal.model()
    # cal.reset()
    # cal.add(lineAB_Equ[0]==x, lineAB_Equ[1]==y, lineAB_Equ[2]==z, t==m[t])
    # if cal.check() != z3.sat:
    #     return False
    # m2 = cal.model()
    # return [m2[x], m2[y], m2[z]]
    # result = []
    lineAB_List = calLinePassPoint(lineAB[0], lineAB[1])
    lineCD_List = calLinePassPoint(lineCD[0], lineCD[1])
    focus = lineAB_List.intersection(lineCD_List)
    if len(focus) == 1:
        return list(focus)[0]
    return False

def calLinePassPoint(A, B):
    # version 2
    result = set()
    lineAB_Equ = calLineEqut(A, B)
    x, y, z = z3.Reals("x y z")
    cal = z3.Solver()
    cal.add(lineAB_Equ[0]==x, lineAB_Equ[1]==y, lineAB_Equ[2]==z)
    cal.push()
    minX, maxX = sorted([A[0], B[0]])
    minY, maxY = sorted([A[1], B[1]])
    minZ, maxZ = sorted([A[2], B[2]])
    for a1 in range(minX, maxX+1):
        for b1 in range(minY, maxY+1):
            for c1 in range(minZ, maxZ+1):
                cal.pop()
                cal.push()
                cal.add(x>=a1, x<a1+1)
                cal.add(y>=b1, y<b1+1)
                cal.add(z>=c1, z<c1+1)
                if cal.check() != z3.sat:
                    continue
                m = cal.model()
                tmp_point = [floatSymbolToInt(m[x]), floatSymbolToInt(m[y]), floatSymbolToInt(m[z])]
                result.add(tuple(tmp_point))
    return result
    # version 1
    # result = []
    # lineAB_Equ = calLineEqut(A, B)
    # x, y, z = z3.Reals("x y z")
    # cal = z3.Solver()
    # cal.add(lineAB_Equ[0]==x, lineAB_Equ[1]==y, lineAB_Equ[2]==z)
    # cal.push()
    # # x
    # cal.add(y>=0, y<=(factorial-1))
    # cal.add(z>=0, z<=(factorial-1))
    # # minX, maxX = sorted([A[0], B[0]])
    # for i in range(0, factorial):
    #     cal.push()
    #     cal.add(x == i)
    #     if cal.check() != z3.sat:
    #         cal.pop()
    #         continue
    #     m = cal.model()
    #     result.append([m[x], m[y], m[z]])
    #     cal.pop()
    # # y 
    # cal.pop()
    # cal.push()
    # cal.add(x>=0, x<=(factorial-1))
    # cal.add(z>=0, z<=(factorial-1))
    # for i in range(0, factorial):
    #     cal.push()
    #     cal.add(y == i)
    #     if cal.check() != z3.sat:
    #         cal.pop()
    #         continue
    #     m = cal.model()
    #     result.append([m[x], m[y], m[z]])
    #     cal.pop()
    # # z
    # cal.pop()
    # # cal.push()
    # cal.add(x>=0, x<=(factorial-1))
    # cal.add(y>=0, y<=(factorial-1))
    # # minZ, maxZ = sorted([A[2], B[2]])
    # for i in range(0, factorial):
    #     cal.push()
    #     cal.add(z == i)
    #     if cal.check() != z3.sat:
    #         cal.pop()
    #         continue
    #     m = cal.model()
    #     result.append([m[x], m[y], m[z]])
    #     cal.pop()
    # for i in range(len(result)):
    #     for j in range(3):
    #         result[i][j] = floatSymbolToInt(result[i][j])
    # tmp = result
    # result = []
    # for i in tmp:
    #     if i not in result:
    #         result.append(i)
    # result.sort()
    # return result

def checkFoucs(F):
    if F[0]>=1 and F[0]<=factorial-2 and \
        F[1]>=1 and F[1]<=factorial-2 and \
        F[2]>=1 and F[2]<=factorial-2:
        return True
    else:
        return False

def floatSymbolToInt(symbF):
    return symbF.numerator_as_long()/symbF.denominator_as_long()

# calculate with line AB perpendicular line CD, return D
def calVertical(pointA, pointB, pointC):
    # t = z3.Reals("t")
    # x, y, z = calLineEqut(pointA, pointB)
    x, y, z = z3.Ints('x y z')
    formula = (pointB[0]-pointA[0])*(x - pointC[0])
    formula += (pointB[1]-pointA[1])*(y - pointC[1])
    formula += (pointB[2]-pointA[2])*(z - pointC[2])
    formula = formula == 0
    cal = z3.Solver()
    cal.add(formula)
    # # cal.add(x==6)
    perhaps_list = [x==0, x==factorial-1, y==0, y==factorial-1, z==0, z==factorial-1]
    cal.add(x>=0, x<=(factorial-1))
    cal.add(y>=0, y<=(factorial-1))
    cal.add(z>=0, z<=(factorial-1))
    for i in perhaps_list:
        cal.push()
        cal.add(i)
        if cal.check() != z3.sat:
            cal.pop()
            continue
        m = cal.model()
        result = [m[x].as_long(), m[y].as_long(), m[z].as_long()]
        if result == pointC:
            cal.pop()
            continue
        return result
    return False
    # pointF = [floatSymbolToInt(m.eval(x)), floatSymbolToInt(m.eval(y)), floatSymbolToInt(m.eval(z))]
    # for i in pointF:
    #     if i < 1 or i > (factorial-2):
    #         return False
    # knD = calLinePassPoint(pointC, pointF)
    # for i in knD:
    #     if (6 in i or 0 in i) and i !=pointC:
    #         return [i, pointF]
    # return False
    
def randomPoint(start, end):
    return [random.randint(start,  end) for x in range(2)]

def genSub():
    s = []
    one = [random.randint(0,  factorial-1) for x in range(2)]
    one.append(0)
    s.append(one)
    while True:
        two = randomPoint(0, factorial-1)
        two.insert(random.choice([0,1,2]), random.choice([0,6]))
        if two[0] != one[0] and two[1] != one[1] and two[2] != one[2]:
            break
    s.append(two)
    # one_two_P = calLinePassPoint(one, two)
    while True:
        three = randomPoint(0, factorial-1)
        three.insert(random.choice([0,1,2]), random.choice([0,6]))
        if three in s:
            continue
        four = calVertical(one, two, three)
        if four:
            # three_four_P = calLinePassPoint(three, four)
            # for i in three_four_P:
            #     if i in one_two_P:
            #         s.append(i)
            break
    s.append(three)
    s.append(four)
    # s.append(four[1])
    # padd = [[0,0],[0,factorial-1],[1,0],[1,factorial-1],[2,0],[2,factorial-1]]
    # s = []
    # for x in range(6):
    #     while True:
    #         tmp = randomPoint(0, factorial-1)
    #         tmp.insert(padd[x][0], padd[x][1])
    #         if tmp not in s:
    #             s.append(tmp)
    #             break
    # # s[0].append(0)
    # # s[1].append(6)
    # # s[2].insert(0, 0)
    # # s[3].insert(0, 6)
    # # s[4].insert(1, 0)
    # # s[5].insert(1, 6)
    # # for x in range(2):
    # #     tmp = randomPoint(0, factorial-2)
    # #     s.append(tmp)
    for x in range(factorial-4):
        while True:
            tmp = randomPoint(0, factorial-1)
            tmp.insert(random.choice([0,1,2]), random.choice([0,6]))
            if tmp not in s:
                s.append(tmp)
                break
    return s

def isVertical(A, B, C, D):
    return (B[0]-A[0])*(D[0]-C[0]) + (B[1]-A[1])*(D[1]-C[1]) + (B[2]-A[2])*(D[2]-C[2]) == 0

# def FromListGetVertical(Sub):
#     result = []
#     Sublist = list(itertools.combinations(Sub, 2))
#     for x in range(len(Sublist)):
#         for y in range(x+1, len(Sublist)):
#             if isVertical(Sublist[x][0], Sublist[x][1], Sublist[y][0], Sublist[y][1]):
#                 fPoint = calFocus(Sublist[x], Sublist[y])
#                 if fPoint:
#                     xP, yP, zP = fPoint
#                     if z3.simplify(xP >= 0) and z3.simplify(xP < factorial) \
#                         and z3.simplify(yP >= 0) and z3.simplify(yP < factorial) \
#                         and z3.simplify(zP >= 0) and z3.simplify(zP < factorial):
#                         result.append(fPoint)
#     return result

def checkSub(subject):
    # check vertical
    Sublist = list(itertools.combinations(subject, 2))
    n = 0
    doubleLine = itertools.combinations(Sublist, 2)
    for lines in doubleLine:
        if isVertical(lines[0][0], lines[0][1], lines[1][0], lines[1][1]):
            fPoint = calFocus([lines[0][0], lines[0][1]], [lines[1][0], lines[1][1]])
            print(fPoint)
            if fPoint and fPoint not in lines[0]:
                n += 1
    if n == 1:
        return True
    else:
        return False


def printMatrix(num):
    template = "|%%0%dd"%num_len
    template *= factorial
    template += "|\n"
    square = "-"*78+"\n"
    for x in num:
        x1 = tuple(x)
        square+= template%x1
        square += "-"*78+"\n"
    print(square)

def genCube(sixsurface):
    # 1
    for x in range(factorial):
        sixsurface[0][x][-1] = sixsurface[1][x][0]
        sixsurface[2][x][0] = sixsurface[1][x][-1]
        sixsurface[4][-1][x] = sixsurface[1][0][x]
        sixsurface[5][0][x] = sixsurface[1][-1][x]

    # 0
    for x in range(factorial):
        sixsurface[4][x][0] = sixsurface[0][0][x]
        sixsurface[3][x][-1] = sixsurface[0][x][0]
        sixsurface[5][x][0] = sixsurface[0][-1][factorial-x-1]
    
    # 2
    for x in range(factorial):
        sixsurface[4][x][-1] = sixsurface[2][0][factorial-x-1]
        sixsurface[5][x][-1] = sixsurface[2][-1][x]
        sixsurface[3][x][0] = sixsurface[2][x][-1]
    
    # 3
    for x in range(factorial):
        sixsurface[4][0][x] = sixsurface[3][0][factorial-x-1]
        sixsurface[5][-1][x] = sixsurface[3][-1][factorial-x-1]

    return sixsurface

def replaceSubPoint(matrix_list, Sub, f):
    for x in Sub:
        tmp = f(bit_len)
        if x[0] == 0:
            matrix_list[3][factorial-1-x[2]][factorial-1-x[1]] = tmp
        if x[0] == 6:
            matrix_list[1][factorial-1-x[2]][x[1]] = tmp
        if x[1] == 0:
            matrix_list[0][factorial-1-x[2]][x[0]] = tmp
        if x[1] == 6:
            matrix_list[2][factorial-1-x[2]][factorial-1-x[0]] = tmp
        if x[2] == 0:
            matrix_list[5][factorial-1-x[0]][x[1]] = tmp
        if x[2] == 6:
            matrix_list[4][x[0]][x[1]] = tmp
    return matrix_list

def waiting():                                    
    while True:                                
        for x in range(3):                    
            sys.stdout.write("\033[K\033[1DGenerate the Games %s\r\033[0m"%("."*(x+1)))
            sys.stdout.flush()                 
            time.sleep(1)
            if stop:
                return

def getSub():
    while True:
        subject = genSub()
        aP, bP, cP, dP = subject[:4]
        fPoint = calFocus([aP, bP], [cP, dP])
        if not fPoint or not checkFoucs(fPoint):
            continue
        if checkSub(subject):
            break
    return [subject, fPoint]

def Question5(subject):
    q5 = """
=================================================================================
                                Question Five
=================================================================================

Please give me answer within 20s

"""
    print(q5)
    answer = subject[1]
    subject = subject[0]
    matrix_list = [getDPrimeMatrix() for x in range(6)]
    cube = genCube(matrix_list)
    cube = replaceSubPoint(cube, subject, getTPrime)
    order = [0, 1, 2, 3, 4, 5]
    random.shuffle(order)
    # print(order)
    if order[0] == 0:
        rightx = answer[0]
        righty = answer[2]
        rightz = answer[1]
    elif order[0] == 1:
        rightx = answer[1]
        righty = answer[2]
        rightz = 6-answer[0]
    elif order[0] == 2:
        rightx = 6-answer[0]
        righty = answer[2]
        rightz = 6-answer[1]
    elif order[0] == 3:
        rightx = 6-answer[1]
        righty = answer[2]
        rightz = answer[0]
    elif order[0] == 4:
        rightx = answer[1]
        righty = 6-answer[0]
        rightz = 6-answer[2]
    elif order[0] == 5:
        rightx = answer[1]
        righty = answer[0]
        rightz = answer[2]
    o = itertools.chain(["A", "B", "C", "D", "E", "F"])
    for x in order:
        print("                                      "+o.next())
        printMatrix(cube[x])
        print("*"*78)
    print("Use A to create a coordinate system(z == 0)")
    coo = """
6^y
 |
 |
 |         x
 |__________>
0           6
"""
    print(coo)
    print("Please enter the coordinates of the answer:")
    signal.alarm(20)
    sys.stdout.write("x: ")
    sys.stdout.flush()
    x = raw_input().strip()
    sys.stdout.write("y: ")
    sys.stdout.flush()
    y = raw_input().strip()
    sys.stdout.write("z: ")
    sys.stdout.flush()
    z = raw_input().strip()
    try:
        x = int(x)
        y = int(y)
        z = int(z)
    except:
        return False
    if x == rightx and y == righty and z == rightz:
        return True
    return False

def Question4(subject):
    q4 = """
=================================================================================
                                Question Four
=================================================================================
"""
    print(q4)
    answer = subject[1]
    subject = subject[0]
    matrix_list = [genPrimeMatrix() for x in range(6)]
    cube = genCube(matrix_list)
    cube = replaceSubPoint(cube, subject, getNotPrime)
    order = [0, 1, 2, 3, 4, 5]
    random.shuffle(order)
    # print(order)
    if order[0] == 0:
        rightx = answer[0]
        righty = answer[2]
        rightz = answer[1]
    elif order[0] == 1:
        rightx = answer[1]
        righty = answer[2]
        rightz = 6-answer[0]
    elif order[0] == 2:
        rightx = 6-answer[0]
        righty = answer[2]
        rightz = 6-answer[1]
    elif order[0] == 3:
        rightx = 6-answer[1]
        righty = answer[2]
        rightz = answer[0]
    elif order[0] == 4:
        rightx = answer[1]
        righty = 6-answer[0]
        rightz = 6-answer[2]
    elif order[0] == 5:
        rightx = answer[1]
        righty = answer[0]
        rightz = answer[2]
    o = itertools.chain(["A", "B", "C", "D", "E", "F"])
    for x in order:
        print("                                      "+o.next())
        printMatrix(cube[x])
        print("*"*78)
    print("Use A to create a coordinate system(z == 0)")
    coo = """
6^y
 |
 |
 |         x
 |__________>
0           6
"""
    print(coo)
    print("Please enter the coordinates of the answer:")
    sys.stdout.write("x: ")
    sys.stdout.flush()
    x = raw_input().strip()
    sys.stdout.write("y: ")
    sys.stdout.flush()
    y = raw_input().strip()
    sys.stdout.write("z: ")
    sys.stdout.flush()
    z = raw_input().strip()
    try:
        x = int(x)
        y = int(y)
        z = int(z)
    except:
        return False
    if x == rightx and y == righty and z == rightz:
        return True
    return False

def Question3(subject):
    q3 = """
=================================================================================
                                Question Three
=================================================================================
"""
    print(q3)
    answer = subject[1]
    subject = subject[0]
    matrix_list = [genNPrimeMatrix() for x in range(6)]
    cube = genCube(matrix_list)
    cube = replaceSubPoint(cube, subject, getPrime)
    order = [0, 1, 2, 3, 4, 5]
    random.shuffle(order)
    # print(order)
    if order[0] == 0:
        rightx = answer[0]
        righty = answer[2]
        rightz = answer[1]
    elif order[0] == 1:
        rightx = answer[1]
        righty = answer[2]
        rightz = 6-answer[0]
    elif order[0] == 2:
        rightx = 6-answer[0]
        righty = answer[2]
        rightz = 6-answer[1]
    elif order[0] == 3:
        rightx = 6-answer[1]
        righty = answer[2]
        rightz = answer[0]
    elif order[0] == 4:
        rightx = answer[1]
        righty = 6-answer[0]
        rightz = 6-answer[2]
    elif order[0] == 5:
        rightx = answer[1]
        righty = answer[0]
        rightz = answer[2]
    o = itertools.chain(["A", "B", "C", "D", "E", "F"])
    for x in order:
        print("                                      "+o.next())
        printMatrix(cube[x])
        print("*"*78)
    print("Use A to create a coordinate system(z == 0)")
    coo = """
6^y
 |
 |
 |         x
 |__________>
0           6
"""
    print(coo)
    print("Please enter the coordinates of the answer:")
    sys.stdout.write("x: ")
    sys.stdout.flush()
    x = raw_input().strip()
    sys.stdout.write("y: ")
    sys.stdout.flush()
    y = raw_input().strip()
    sys.stdout.write("z: ")
    sys.stdout.flush()
    z = raw_input().strip()
    try:
        x = int(x)
        y = int(y)
        z = int(z)
    except:
        return False
    if x == rightx and y == righty and z == rightz:
        return True
    return False

def Question2(subject):
    q2 = """
=================================================================================
                                Question Two
=================================================================================
"""
    print(q2)
    answer = subject[1]
    subject = subject[0]
    matrix_list = [genEvenMatrix() for x in range(6)]
    cube = genCube(matrix_list)
    cube = replaceSubPoint(cube, subject, getOdd)
    order = [0, 1, 2, 3, 4, 5]
    random.shuffle(order)
    # print(order)
    if order[0] == 0:
        rightx = answer[0]
        righty = answer[2]
        rightz = answer[1]
    elif order[0] == 1:
        rightx = answer[1]
        righty = answer[2]
        rightz = 6-answer[0]
    elif order[0] == 2:
        rightx = 6-answer[0]
        righty = answer[2]
        rightz = 6-answer[1]
    elif order[0] == 3:
        rightx = 6-answer[1]
        righty = answer[2]
        rightz = answer[0]
    elif order[0] == 4:
        rightx = answer[1]
        righty = 6-answer[0]
        rightz = 6-answer[2]
    elif order[0] == 5:
        rightx = answer[1]
        righty = answer[0]
        rightz = answer[2]
    o = itertools.chain(["A", "B", "C", "D", "E", "F"])
    for x in order:
        print("                                      "+o.next())
        printMatrix(cube[x])
        print("*"*78)
    print("Use A to create a coordinate system(z == 0)")
    coo = """
6^y
 |
 |
 |         x
 |__________>
0           6
"""
    print(coo)
    print("Please enter the coordinates of the answer:")
    sys.stdout.write("x: ")
    sys.stdout.flush()
    x = raw_input().strip()
    sys.stdout.write("y: ")
    sys.stdout.flush()
    y = raw_input().strip()
    sys.stdout.write("z: ")
    sys.stdout.flush()
    z = raw_input().strip()
    try:
        x = int(x)
        y = int(y)
        z = int(z)
    except:
        return False
    if x == rightx and y == righty and z == rightz:
        return True
    return False

def Question1(subject):
    q1 = """
=================================================================================
                                Question One
=================================================================================
"""
    print(q1)
    answer = subject[1]
    subject = subject[0]
    matrix_list = [genOddMatrix() for x in range(6)]
    cube = genCube(matrix_list)
    cube = replaceSubPoint(cube, subject, getEven)
    order = [0, 1, 2, 3, 4, 5]
    #random.shuffle(order)
    #print(order)
    if order[0] == 0:
        rightx = answer[0]
        righty = answer[2]
        rightz = answer[1]
    elif order[0] == 1:
        rightx = answer[1]
        righty = answer[2]
        rightz = 6-answer[0]
    elif order[0] == 2:
        rightx = 6-answer[0]
        righty = answer[2]
        rightz = 6-answer[1]
    elif order[0] == 3:
        rightx = 6-answer[1]
        righty = answer[2]
        rightz = answer[0]
    elif order[0] == 4:
        rightx = answer[1]
        righty = 6-answer[0]
        rightz = 6-answer[2]
    elif order[0] == 5:
        rightx = answer[1]
        righty = answer[0]
        rightz = answer[2]
    o = itertools.chain(["A", "B", "C", "D", "E", "F"])
    # print(order)
    for x in order:
        print("                                      "+o.next())
        printMatrix(cube[x])
        print("*"*78)
    print("Use A to create a coordinate system(z == 0)")
    coo = """
6^y
 |
 |
 |         x
 |__________>
0           6
"""
    print(coo)
    print("Please enter the coordinates of the answer:")
    sys.stdout.write("x: ")
    sys.stdout.flush()
    x = raw_input().strip()
    sys.stdout.write("y: ")
    sys.stdout.flush()
    y = raw_input().strip()
    sys.stdout.write("z: ")
    sys.stdout.flush()
    z = raw_input().strip()
    try:
        x = int(x)
        y = int(y)
        z = int(z)
    except:
        return False
    if x == rightx and y == righty and z == rightz:
        return True
    return False

def welcom():
    batch = """
 _   _      __ _         _____ _______ ______  
| \ | |    /_ | |       / ____|__   __|  ____| 
|  \| |_   _| | |      | |       | |  | |__    
| . ` | | | | | |      | |       | |  |  __|   
| |\  | |_| | | |____  | |____   | |  | |      
|_| \_|\__,_|_|______|  \_____|  |_|  |_|      
                                                                       
                                                                       
 __  __       _   _          _____                      
|  \/  |     | | | |        / ____|                     
| \  / | __ _| |_| |__     | |  __  __ _ _ __ ___   ___ 
| |\/| |/ _` | __| '_ \    | | |_ |/ _` | '_ ` _ \ / _ \\
| |  | | (_| | |_| | | |   | |__| | (_| | | | | | |  __/
|_|  |_|\__,_|\__|_| |_|    \_____|\__,_|_| |_| |_|\___|
***********************************************************
Game rules:
    A 7*7*7 cube consists of 343 cubes, These are 218 cubic cells in the surface, and 125 cubic cells in the internal.
We put numbers in 218 cubes, of which seven cubes number have different attributes than others (for example, odd and even, prime and non-prime).
Connect these seven cubes to form 21 straight lines. Only two of these 21 straight lines are perpendicular and go through the same internal cube. 
Please give the coordinates of this internal cube. If you answer 5 Question, you will get the flag.
(PS: A handsome boy can use his own eyes to complete this game.)
"""
    print(batch)

def proof():
    strings = "abcdefghijklmnopqrstuvwxyzWOERFJASKL"
    prefix = "".join(random.sample(strings, 6))
    starwith = str(random.randint(10000, 99999))
    pf = """
sha256("%s"+str).hexdigest().startswith("%s") == True
Please give me str
"""%(prefix, starwith)
    print(pf)
    s = raw_input().strip()
    if sha256(prefix+s).hexdigest().startswith(starwith):
        return True
    else:
        return False

def checktime():
    # return os.path.exists("/root/ppc/start")
    # 2018/3/11 0:0:0
    t = 1520697600
    return time.time() > t

def main():
    global stop
    # if not checktime():
    #     print("Hacked by Nu1L")
    #     return
    # if not proof():
    #     return
    subjects = []
    welcom()
    wait_thread = threading.Thread(target=waiting)
    wait_thread.start()
    for i in range(1):
        subjects.append(getSub())
    stop = 1
    # for x in subjects:
    #     print(x[0])
    #     print("-->")
    #     print(x[1])
    #     print("=======")
    if Question1(subjects[0]):
    # if Question1(subjects[0]) and Question2(subjects[1]) and \
    #     Question3(subjects[2]) and Question4(subjects[3]) and \
    #     Question5(subjects[4]):
        print(flag)
        import time
        f = open("getflag.log", "a")
        addr = os.environ["SOCAT_PEERADDR"]
        f.write("%s: %s getflag\n"%(time.ctime(), addr))
        f.close()
    else:
        print("You lose!\nGoodbye!")
    
    # matrix_list = [genMatrix() for x in range(6)]
    # cube = genCube(matrix_list)
    # cube = replaceSubPoint(cube, subject)
    # for x in cube:
    #     printMatrix(x)
    #     print("*"*78+"\n")

if __name__ == '__main__':
    # try:
    #     main()
    # except:
    #     os._exit(0)
    main()
