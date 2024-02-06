# file   : lambda.py
# author:  Carlos Ordonez
# content: functional programming 
# updated: 2019.10.11
# open:    from lambda import *
#          import lambda_calc: does not work
# recursion breaks at 1000 => max rec. depth 900

from functools import *
import sys
sys.setrecursionlimit(10000)

# classical functions to access list
l_head=lambda l: l[0]
l_tail=lambda l: l[1:]
# operators
l_add=lambda x,y:x+y
l_mul=lambda x,y:x*y
l_list_desc=lambda n: [] if n==0 else [n]+l_list_desc(n-1)
l_list_asc=lambda n: [] if n==0 else l_list_asc(n-1) + [n]
l_repeat= lambda x,n: [] if n==0 else [x]+l_repeat(x,n-1)
l_sum= lambda l:reduce(l_add,l)
# l_min= lambda l: l[0] if len(l)==1 else if len(l)>1


# advanced lambda calculus
# incorrect, does not work, element expected
#curry=lambda ():[] 
# correct
curry=lambda :[] 
# induction base
curry=lambda e1:[e1]
curry=lambda e1,e2:[e1,e2]
curry=lambda e1,e2,e3:[e1,e2,e3]
curry= lambda e1,e2,e3,e4:[e1,e2,e3,e4]
# generalization not possible, [head(l):tail(l)]
curry=lambda h,t:[e1,e2]


# test

# sum of numbers
l1=l_list_asc(8)
l_sum(l1)

# + acts as concatenation
letters=['a','b','c']
l_sum(letters)
