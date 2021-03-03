def df_calculator(s1, s2, n1, n2):
    SE1 = s1 / (n1 ** 0.5)
    SE2 = s2 / (n2 ** 0.5)
    liczdf = (SE1 ** 2 + SE2 ** 2) ** 2
    miandf = ((SE1 ** 4) / (n1 - 1)) + ((SE2 ** 4) / (n2 - 1))
    return liczdf / miandf

def NSE_calculator(s1, s2, n1, n2):
    SE1 = s1 / (n1 ** 0.5)
    SE2 = s2 / (n2 ** 0.5)
    return (SE1 ** 2 + SE2 ** 2) ** 0.5

def USE_calculator(lst1, lst2):
    SS1 = 0
    suma = 0
    for i in range(len(lst1)):
        suma += lst1[i]
    x1 = suma / len(lst1)
    for i in range(len(lst1)):
        SS1 += (lst1[i] - x1) ** 2
    SS2 = 0
    suma2 = 0
    for i in range(len(lst2)):
        suma2 += lst2[i]
    x2 = suma2 / len(lst2)
    for i in range(len(lst2)):
        SS2 += (lst2[i] - x2) ** 2
    sc = ((SS1 + SS2) / (len(lst1) + len(lst2) - 2)) ** 0.5
    return sc * (1/len(lst1) + 1/len(lst2)) ** 0.5

def sd(lst):
    suma = 0
    suma2 = 0
    for i in range(len(lst)):
        suma += lst[i]
    x = suma / len(lst)
    for i in range(len(lst)):
        suma2 += (lst[i] - x) ** 2
    standard = (suma2 / (len(lst) - 1)) ** 0.5
    return standard


print(df_calculator(0.4, 0.9, 4, 9))
print(NSE_calculator(8, 4, 20, 25))
#print(USE_calculator([8,12,9,11], [5,8,7,6,4]))
#print(sd([8,12,9,11]))
print((sd([152,165,163,178,172])/5**0.5)*2.015)
print(sd([11.4, 13.1, 15.1, 18.2, 16.1]))