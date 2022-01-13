class Solution(object):
    def romanToInt(self, s):
        number_map = {"I": 1, "V": 5, "X": 10, "L": 50, "C":100, "D": 500, "M": 1000}
        decimal = 0
        for i in range(len(s)):
            if i +1 <len(s) and number_map[s[i]] < number_map[s[i + 1]]:
                decimal -= number_map[s[i]]
            else:
                decimal += number_map[s[i]]
        return decimal

