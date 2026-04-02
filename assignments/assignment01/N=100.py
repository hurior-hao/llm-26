max=10000
N2independent=[]
for N in range(1,max+1):
    A=[]
    B=[]
    for i in range(N):
        if not i%2:
            A.append(i)
        if not i%3:
            B.append(i)

    AB=[]
    for i in range(len(A)):
        for j in range(len(B)):
            if B[j]==A[i]:
                AB.append(j)

    P_AB=len(AB)/N
    P_A =len(A)/N
    P_B =len(B)/N
    if P_AB==P_A*P_B:
        N2independent.append(N)

print(N2independent)