#Input: head = [1,2,3,4,5]
#Output: [1,3,5,2,4]
#Given the head of a singly linked list, group all the nodes with odd indices together followed by the nodes with even indices, and return the reordered list.
class Solution(object):
    def oddEvenList(self, head):

        if not head: return head       
        odd = head
        even = firstEven = head.next
                
        while even and even.next:            
            odd.next = even.next
            odd = even.next
            even.next = odd.next
            even = odd.next      
        
        odd.next = firstEven

        return head