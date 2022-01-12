def buddyStrings(self, s: str, goal: str) -> bool:
        diffs =[]
        goals=[]
        
        if len(s)!=len(goal):
            return False
        if s==goal:
            return len(set(s))<len(s)
        i=0
        while(i<len(s)):
            if s[i]!=goal[i]:
                diffs.append(s[i])
                goals.append(goal[i])
            i+=1

            
        if len(diffs)!=2:
            return False
        return diffs[0]==goals[1] and diffs[1]==goals[0]