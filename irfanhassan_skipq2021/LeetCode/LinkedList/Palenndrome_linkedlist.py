#Given the head of a singly linked list, return true if it is a palindrome.
class Solution:
    def getMid(head):
        slow=quick=head
        while quick and quick.next:
            slow=slow.next
            quick=quick.next.next
        return slow if not quick else slow.next
        
    def reverse(start):
        prev,current=None,start
        while current:
            next=current.next
            current.next=prev
            prev=current
            current=next
        return prev
        
    def isPalindrome(self, head: ListNode) -> bool:
        mid=getMid(head)
        scan_left,scan_right=head,reverse(mid)
        while scan_right:
            if scan_left.val==scan_right.val:
                scan_left,scan_right=scan_left.next,scan_right.next
            else:
                return False
        
        return True