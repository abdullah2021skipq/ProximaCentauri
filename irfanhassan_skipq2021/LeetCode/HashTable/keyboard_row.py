#Given an array of strings words, return the words that can be typed using letters of the alphabet on only one row of American keyboard like the image below.
class Solution:
    def keyboardfindWords(self, words):
        
        lst = []
        qw = "qwertyuiop"
        asd = "asdfghjkl"
        zx = "zxcvbnm"
        
        for i in words:
            j = i.lower()
            if len(set(qw).intersection(j)) == len(set(j)):
                lst.append(i)
            
            elif len(set(asd).intersection(j)) == len(set(j)):
                lst.append(i)
            
            elif len(set(zx).intersection(j)) == len(set(j)):
                lst.append(i)
        
        return lst
        
x=["Hello","Alaska","Dad","Peace"]
test=Solution()
print(test.keyboardfindWords(x))