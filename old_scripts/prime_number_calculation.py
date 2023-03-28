#to check if number is prime or no 
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


//////////////////////////////
with open('C:/Users/halil/Desktop/input.txt') as f:
    array2 = []
    for line in f:
        array2.append(list(map(int, line.split(" "))))
        
#to replace prime numbers in array with any number or None 
def kick_primes_out(no_prime_list):
    for x in range(len(no_prime_list)):
        for y in range(len(no_prime_list[x])):
            if prime_check(no_prime_list[x][y]):
                no_prime_list[x][y] = None
    return no_prime_list
