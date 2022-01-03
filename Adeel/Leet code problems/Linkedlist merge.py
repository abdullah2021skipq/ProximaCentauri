# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        tem1 = list1
        tem2 = list2
        prev = None
        while tem1 != None and tem2 != None:
            if tem1.val <= tem2.val:
                prev = tem1
                tem1 = tem1.next
            else:
                if prev != None:
                    prev.next = tem2
                    x = tem2.next
                    tem2.next = tem1
                    tem2 = x
                    prev = prev.next
                else:
                    x = tem2.next
                    prev = tem2
                    tem2.next = tem1
                    tem2 = x
                    tem1 = prev
                    prev = None
                    list1 = tem1
                    
        if tem2 != None:
            if prev != None:
                prev.next = tem2
            else:
                list1 = tem2
            
        return list1
        