import sys
from typing import List

class Solution:
    def nearestValidPoint(self, x: int, y: int, points: List[List[int]]) -> int:
        
        
        mindiff = sys.maxsize
        min_index = -1
        for i, [x1, y1] in enumerate(points):
            
            curr_dist = abs(x - x1) + abs(y - y1)
            if (x1 == x or y1 == y) and (mindiff > curr_dist):
                mindiff = curr_dist
                min_index = i
                
      
        return min_index