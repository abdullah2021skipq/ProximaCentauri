#prices with discount

def finalPrices(self, prices):

    for i in range (0,len(prices)-1):             #Length-1 because last element doesn't get discount
        for j in range (i+1,len(prices)):
            if(prices[i]>=prices[j]):             #checking if discount is not greater than current price
                prices[i]-=prices[j]
                break                             #breaking from loop if disount prices is found
    return prices