#Given head which is a reference node to a singly-linked list. The value of each node in the linked list is either 0 or 1. The linked list holds the binary representation of a number.

#Return the decimal value of the number in the linked list.
def getDecimalValue(self, head: ListNode) -> int:
    count = 0
    curr = head
 
 #finding the length of the linkedlist
    while curr != None:
        count += 1
        curr = curr.next
        summ = 0
    curr = head
 
    #converting to decimal format
    for i in range(count-1, -1, -1):
        summ += curr.val * 2**(i)
        if curr.next is None:
            return summ
            curr = curr.next