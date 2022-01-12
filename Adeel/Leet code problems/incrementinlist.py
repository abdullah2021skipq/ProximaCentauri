class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        incre = []
        x = 0
        for i in digits:
            x = x*10 + i
        x = x +1
        str_x = str(x)
        for items in str_x:
            incre.append(int(items))
        return incre
        
                