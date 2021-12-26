class Solution(object):
    def relativeSortArray(self, arr1, arr2):
        """
        :type arr1: List[int]
        :type arr2: List[int]
        :rtype: List[int]
        """
        c={}
        arr1.sort()
        for i in arr1:
            if(i in c):
                c[i]+=1
            else:
                c[i]=1
        ret=[]
        for i in arr2:
            ret+=[i]*c[i]
            c.pop(i)
        ret2=[]
        for i in c:
            ret2+=[i]*c[i]
        ret2.sort()
        return ret+ret2