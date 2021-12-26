class MyHashMap:
    def __init__(self):
        self.ks = set()
        self.k = []
        self.v = []

    def put(self, key: int, value: int) -> None:
        if key in self.ks:
            i = self.k.index(key) 
            self.v[i] = value
        else:
            self.ks.add(key)
            self.k.append(key)
            self.v.append(value)            

    def get(self, key: int) -> int:
        res = -1
        if key in self.ks:
            i = self.k.index(key)
            res = self.v[i]
        return res

    def remove(self, key: int) -> None:
        if key in self.ks:
            i = self.k.index(key)
            self.ks.remove(key)
            self.k.pop(i)
            self.v.pop(i)