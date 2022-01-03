# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution(object):
    def hasCycle(self, head):
        parsef, parses = head, head
        while parsef and parsef.next:
            parsef, parses = parsef.next.next, parses.next
            if parsef is parses:
                return True
        return False

        
