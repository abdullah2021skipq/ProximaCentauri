# function that reverses a string. The input string is given as an array of characters
def revers_string(string):
    neg_index=-1
    for n in range (0, round(len(string)/2)):
        ch = string[neg_index]
        string[neg_index]=string[n]
        string[n]=ch
        neg_index-=1
    return string


string = ['a','b','c','d','e']
print(revers_string(string))