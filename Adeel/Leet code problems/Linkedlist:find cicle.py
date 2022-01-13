# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        if head is None:
            return False
        
        visited = set()
        cur_node = head
        
        while cur_node not in visited:
            visited.add(cur_node)
            
            if cur_node.next is None:
                return False
            
            cur_node = cur_node.next
            
            
        
        return True