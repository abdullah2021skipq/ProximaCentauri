def deleteDuplicates(head):
     
    first, second = head, head.next if head else None
    while second:
        if first.val == second.val:
            second = second.next
            first.next = second
        else:
            first = second
            second = second.next
            
    return head