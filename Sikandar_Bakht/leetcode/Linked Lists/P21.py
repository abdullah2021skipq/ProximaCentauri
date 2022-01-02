#merge two sorted lists

class ListNode:
     def __init__(self, val=0, next=None):
         self.val = val
         self.next = next
         
def mergeTwoLists(list1, list2):
        
        head = ListNode()
        pointer = head
        
        while list1 != None and list2 != None:
            
            if list1.val < list2.val: 
                pointer.next = list1
                list1 = list1.next
            
            else:
                pointer.next = list2
                list2 = list2.next
            pointer = pointer.next
       
        if list1 != None: pointer.next = list1
        if list2 != None: pointer.next = list2
          
        return head.next