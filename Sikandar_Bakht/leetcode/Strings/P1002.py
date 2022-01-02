#Common chars

def commonChars(words)
       
        n = len(words)
        res = []
        arr = []
        for x in words:
            arr.append(list(x))
        for i in words[0]:
            count = 0
            for j in range(1, n):
                if i in arr[j]:
                    arr[j].remove(i)
                    count += 1
                else:
                    break
           
            if count == n - 1:
                res.append(i)
        return res