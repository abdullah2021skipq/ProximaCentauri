def isValid(s):
        stack = []
        
        for x in s:
            if x in {'(', '[', '{'}:
                stack.append(x)
            else:
                if not stack or stack.pop() + x not in {'()', '[]', '{}'}:
                    return False
    
        return True