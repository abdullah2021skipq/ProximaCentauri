
class Solution(object):

    def removeDuplicates(self, A):
        if not A:
            return 0

        l = 1
        for r in range(1, len(A)):
            if A[r] != A[r-1 ]: #compare if the values in new value
                A[l] = A[r] #put the right unique value
                l += 1 #increment the left pointer
                
        return l


        
