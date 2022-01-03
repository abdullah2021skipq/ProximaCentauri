#You are given the array paths, where paths[i] = [cityAi, cityBi] means there exists a direct path going from cityAi to cityBi. Return the destination city, that is, the city without any path outgoing to another city.
class Solution:
    def destCity(self, paths) -> str:
        res_dic = {}
        i = 0
        for path in paths:
            res_dic[path[i]] = path[i+1]
        for i, j in res_dic.items():
            city = res_dic.get(j)
            if not city:
                return j