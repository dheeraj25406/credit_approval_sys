import math
def calculate_emi(P,R,N):
    r=R/(12*100)
    return (P*r*(1+r)**N)/((1+r)**N-1)