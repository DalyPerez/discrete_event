import random as rd
import math
from probdata import *

def U(a, b):
    """
    Generate a Uniform variable u ~ U(a,b)
    """
    return a + (b-a)*rd.uniform(0, 1)

def Expon(lamb):
    """
    Generate a Exponential variable with parameter lamb
    """
    return -1 * math.log(U(0,1), math.e)/lamb

def Ber(p):
    """
    Generate a Bernoulli variable with parameter p
    """
    u = rd.uniform(0,1)
    if u < p: 
        return 1
    else:
         return 0

def dead_year(age, sex):
    """
    Return the year dead
    """
    if sex == 0:
        i_age = selector(p_die_m, age)
    else: 
        i_age = selector(p_die_w, age)

    u = U(i_age[0], 1) #probabilidad del intervalo de edad en que muere
    if sex == 0:
        i_year = selector(p_year_die_m, u)
    else:
        i_year = selector(p_year_die_w, u)
    
    year = rd.randint(max(age, i_year[0]), 125)
    return year
    

def pregnant(age):
    """
    Return 1: if a woman is pregnant
           0: if no
    """
    p = selector(p_pregnancy, age)
    return Ber(p)

def want_partner(age):
    """
    Return 1: if a person want partner
           0: if no
    """
    p = selector(p_want_partner, age)
    return Ber(p)

def get_partner(w_age, m_age):
    """
    Return 1: if they establish a couple
           0: if no
    """
    dif = abs(w_age - m_age)
    p = selector(p_get_partner, dif)
    return Ber(p)

def breaking(p = 0.2):
    """
    Return 1: if they break 
           0: if no
    """
    return Ber(p)

def time_alone(age):
    """
    Return the time needed to be alone
    """
    lamb = selector(p_time_alone, age)
    return int(math.ceil(Expon(lamb)))

def max_child_wished():
    """
    Return the max number of child wished
    """
    u = U(0,1)
    num = selector(p_wish_child, u)
    return num

def pregnancy_child():
    """
    Return the number of child in a pregnancy
    """
    u = U(0, 1)
    num = selector(p_num_child, u)
    return num

def sex_child(p = 0.5):
    """
    Return the sex of a child 
           0:men  1:women
    """
    return Ber(p)



