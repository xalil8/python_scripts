def prime_check(number):
    if number>1:    
        for i in range(2,number):
            if number % i == 0:
                return False
        return True
    else:
        if number == 1:
            return False
        else:
            return None



def count(m):
    nprime = 0
    number = 1

    while nprime < m:
        number += 1
        if prime_check(number):
            nprime +=1
    return number
