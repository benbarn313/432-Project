import numpy as np

def sort(S):
    #S1 = np.zeros(len(S),2)
    for i in range(1,len(S)):
        j = i
        while S[j][0] < S[j-1][0] or (S[j][0] == S[j-1][0] and S[j][1] < S[j-1][1]):
            temp = S[j][0]
            S[j][0] = S[j-1][0]
            S[j-1][0] = temp
            j -= 1
            if j == 0:
                break
    return S

S = [[1,1],[2,1],[5,3],[4,6],[7,6],[4,7],[9,4]]
print(sort(S))

        
