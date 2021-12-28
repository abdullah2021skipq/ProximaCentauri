class Solution:
    def sortSentence(self, s: str) -> str:
        line = ""
        dic = {}
        s = s.split()
        print(s)
        for i in s:
            a = int(i[-1]) # index
            b = i[:-1]
            dic[a] = b
        dic = sorted(dic.items())
        for _,j in dic:
            line += j+" "
        return line.strip()