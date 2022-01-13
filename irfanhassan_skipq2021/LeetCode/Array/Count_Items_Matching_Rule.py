#You are given an array items, where each items[i] = [typei, colori, namei] describes the type, color, and name of the ith item. You are also given a rule represented by two strings, ruleKey and ruleValue.
class Solution:
    def countMatches(self, items: List[List[str]], ruleKey: str, ruleValue: str) -> int:
        count=0
        dic={"color":1,"type":0,"name":2}
        for i in range(len(items)):
            if items[i][dic[ruleKey]]==ruleValue:
                count+=1
        return count