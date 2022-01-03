#Given two string arrays word1 and word2, return true if the two arrays represent the same string, and false otherwise.
class Solution(object):
    def arrayStringsAreEqual(self, word1, word2):
        str_word1 = "".join(word1)
        str_word2 = "".join(word2)
        if str_word1 == str_word2 :
            return True
        return False
        
word1=["ab",'c']
word2=["a","bc"]
test=Solution()
print(test.arrayStringsAreEqual(word1,word2))