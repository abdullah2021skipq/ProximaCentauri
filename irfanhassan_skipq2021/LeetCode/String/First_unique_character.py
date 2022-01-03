#find the first non-repeating character in it and return its index. If it does not exist, return -1.
class Solution:
    def firstUniqChar(self, string):
        sCopy = string
        for i in range(0,len(sCopy)):
            string=sCopy[i+1:len(sCopy)]
            if (sCopy[i] in string)==False and sCopy.index(sCopy[i])==i:
                return i
        return -1

test=Solution()
string = "leetcode"
print(test.firstUniqChar(string))