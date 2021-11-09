# -*- coding: utf-8 -*-
"""
Created on Tue May 25 14:45:48 2021

@author: CW
"""

from itertools import combinations


def get_subsets(S):
    
    subsets = []
    
    for i in range(len(S) + 1):
        subsets += list(map(set, combinations(S, i)))
    return subsets


def get_value(v, S):
    
    if S == set():
        return 0
    for c in v:
        if S == c[0]:
            return c[1]
    raise ValueError


def excess(v,S,x):
    xs = 0
    for i in S:
        xs += x[i - 1]
    return get_value(v,S) - xs


def factorial(n):
    
    fac = [1 for _ in range(n + 1)]
    
    for i in range(1,n + 1):
        fac[i] = fac[i - 1] * i
    return fac


def Shapley_Value(N, v):
    
    n,j = len(N),0
    sh = [0 for _ in range(n)]
    fac = factorial(n)
    
    for i in list(N):
        subsets = get_subsets(N.difference({i}))
        for S in subsets:
            sh[j] += fac[len(S)] * fac[n - len(S) - 1] * (get_value(v,S.union({i})) - get_value(v,S)) / fac[n]
        j += 1
    return sh


def Solidarity_Value(N, v):
    
    n,j = len(N),0
    sol = [0 for _ in range(n)]     
    fac = factorial(n)
        
    for i in list(N):
        subsets = get_subsets(N.difference({i}))
        for S in subsets:
            S.add(i)
            s = len(S)
            m = 0
            for k in S:
                m = m + get_value(v,S) - get_value(v,S.difference({k}))
            sol[j] = sol[j] + m * fac[s - 1] * fac[n - s] / (s * fac[n])
        j += 1
    return sol


def Least_Square_PreNucleolus(N, v):
    
    n,j = len(N),0
    x = [0 for _ in range(n)]
        
    def a(i):
        ans = 0
        subsets = get_subsets(N.difference({i}))
        for S in subsets:
            ans += get_value(v,S.union({i}))
        return ans
    
    for i in list(N):
        p = n * a(i)
        for k in list(N):
            p -= a(k)
        x[j] = get_value(v,N)/n + p / (n * 2 ** (n - 2))
        j += 1
    return x


def CIS(N, v):

    n,j = len(N),0
    x = [0 for _ in range(n)]
    
    w = [0 for _ in range(n)]
    wn = get_value(v,N)
    for i in list(N):
        w[j] = get_value(v,{i})
        j += 1
    j = 0
    gap = sum(w) - wn
    for i in list(N):
        x[j] = w[j] - gap / n
        j += 1
    return x


def Tau_value(N, v):
    
    n = len(N)
    x,lambda_i = [0 for _ in range(n)],[float('inf') for _ in range(n)]
    b = [(get_value(v,N) - get_value(v,N.difference({i}))) for i in N]
    
    def gap(S):
        return -excess(v,S,b)
    
    for i in N:
        subsets = get_subsets(N.difference({i}))
        for S in subsets:
            S.add(i)
            lambda_i[i - 1] = min(gap(S),lambda_i[i - 1])
    
    gn = gap(N)
    for i in N:
        x[i - 1] = b[i - 1] - lambda_i[i - 1] * gn / sum(lambda_i)
    return x
        

def bankruptcy_game(E, d):
    
    N,v = set(range(1,len(d) + 1)),[]
    subsets = get_subsets(N)
    
    for S in subsets:
        m = E
        for i in N.difference(S):
            m -= d[i - 1]
        v.append((S,max(0,m)))
    return N,v


def saving_game(N, c):
    
    v = []
    subsets = get_subsets(N)
    
    for S in subsets:
        vs = -get_value(c,S)
        for j in S:
            vs += get_value(c,{j})
        v.append((S,vs))
    return N,v


def airport_game(N,C):
    
    c = []
    subsets = get_subsets(N)
    
    for S in subsets:
        cost = 0
        for j in S:
            cost = max(cost,C[j - 1])
        c.append((S,cost))
    return N,c

if __name__ == '__main__':
    
    E = 1200
    d = [150,200,300,400,550,750,800,900,1050,1200]
    N,v = bankruptcy_game(E, d)
    print('Shapley Value:',Shapley_Value(N, v))
    print('Solidarity Value:',Solidarity_Value(N, v))
    print('Least Square PreNucleolus:',Least_Square_PreNucleolus(N, v))
    print('CIS value:',CIS(N, v))
    print('Tau value:',Tau_value(N, v))
    