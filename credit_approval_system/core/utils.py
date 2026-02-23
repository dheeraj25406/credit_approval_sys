import math

def calculate_emi(p,r,n):
    r=r/(12*100)
    return p*r*math.pow(1+r,n)/(math.pow(1+r,n)-1)


def round_to_lakh(x):
    return round(x/100000)*100000