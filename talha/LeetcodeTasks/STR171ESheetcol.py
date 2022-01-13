class Solution(object):
    def titleToNumber(self, columnTitle):
        s=0
        for c in columnTitle:
            #read unicode value for Character using ord
            s=s*26+ord(c)-64 
        return s

        