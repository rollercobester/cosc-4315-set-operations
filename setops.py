from functools import reduce
from os.path import exists
import sys

sys.setrecursionlimit(10000)

# ----------------------------------------- UTILS --------------------------------------------------

# Mimics x.split(y) where x is a string
# Ex: split("a b c", ' ') = ["a", "b", "c"]
splitter = lambda x, y, i: [x] if i == -1 else [x[:i]] + split(x[i+1:], y)
split = lambda x, y: splitter(x, y, x.find(y))

# Mimics x.replace(y, z) where x is a string
# Ex: replace("a b c", ' ', '') = "abc"
replacer = lambda x, a, b: b if x == a else x
replace = lambda x, a, b: x if not x or not a else replacer(x[0], a, b) + replace(x[1:], a, b) 

combine = lambda x: reduce(lambda a, b: a + b, x)

# Merge sort
merge = lambda l, r: l if not r else r if not l else [l[0]] + merge(l[1:], r) if l[0] < r[0] else [r[0]] + merge(l, r[1:])
sort = lambda x: x if len(x)==1 else merge(sort(x[:len(x)//2]), sort(x[len(x)//2:]))

def print_error(message):
    print('Error: {}'.format(message))
    exit(0)

def print_help():
    print('Call syntax: python3 setops.py "set1=[filename];set2=[filename];operation=[difference|union|intersection]"')
    exit(0)

# ------------------------------------- COMMAND PARSER ---------------------------------------------

# Value validation functions
filename_predicate = lambda x: exists(x)
operation_predicate = lambda x: x in ["difference", "union", "intersection"]
filename_error = "file '{}' does not exist"
operation_error = "operation '{}' does not exist\nValid operations: [difference|union|intersection]"

# Command specifications
valid_kwargs = [
    # Key         Value validator      Error message
    ["set1",      filename_predicate,  filename_error],
    ["set2",      filename_predicate,  filename_error],
    ["operation", operation_predicate, operation_error],
]

valid_keys = list(zip(*valid_kwargs))[0]

# Takes a list of assertions to be made on the kwarg values and validates them
def validate_values(assertions):
    failed_assertion = next(filter(lambda x: not x[1](x[0]), assertions), None)
    if failed_assertion: print_error(failed_assertion[2].format(failed_assertion[0]))
    values = list(zip(*assertions))[0]
    return values

# Takes keys and values and returns a list of value assertions [(value, predicate, error_message), ...]
# Forces the same order as the predefined valid_kwargs
generate_assertions = lambda keys, values: tuple(map(lambda x: [values[keys.index(x[0])], x[1], x[2]], valid_kwargs))

# Checks kwargs for missing keys then sends them to have their values validated
def validate_keys(kwargs):
    keys, values = zip(*kwargs)
    missing_key = next(filter(lambda x: x not in keys, valid_keys), None)
    if missing_key: print_error("missing key '{}'".format(missing_key)) 
    return validate_values(generate_assertions(keys, values))

# Filters out kwargs with irrelevant keys and sends the rest to be validated
filter_kwargs = lambda x: validate_keys(list(filter(lambda x: x[0] in valid_keys, x)))

# Takes a string of kwargs and returns a list of key-value pairs [[key, value], ...]
parse_kwargs = lambda x: list(map(lambda x_: split(x_, '='), split(x, ';')))

# Takes a string and returns it without spaces
strip_spaces = lambda x: replace(x, ' ', '')

# Takes a string argument containing kwargs and sends it to get parsed and filtered
extract_kwargs = lambda x: filter_kwargs(parse_kwargs(strip_spaces(x)))

# Prints error message for invalid # of args
invalid_args = lambda x: print_error('too many arguments') if x else print_error('not enough arguments')

# Checks for 1 argument and sends it to be parsed into keyword arguments
parse_args = lambda x: extract_kwargs(x[0]) if len(x) == 1 else invalid_args(x)

# Retrieves arguments and sends them to be validated
parse_command = lambda x: parse_args(x)

# ------------------------------------------ File Parser -------------------------------------------

word_start_index  = lambda x, i=0: i if i == len(x) or x[i].isalnum() else word_start_index(x, i+1)  
letters_end_index = lambda x, i=0: i if i == len(x) or not x[i].isalpha() else letters_end_index(x, i+1)
numbers_end_index = lambda x, i=0, dec=False: i if i == len(x) or dec and x[i] == '.' or not (x[i].isnumeric() or x[i] == '.') else numbers_end_index(x, i+1, dec or x[i] == '.')
word_end_index    = lambda x: letters_end_index(x) if x[0].isalpha() else numbers_end_index(x)

def split_words(text):
    i = word_start_index(text)
    if i == len(text):
        return []
    j = word_end_index(text, i) + 1
    return [text[i:j]] + split_words(text[j:])

def get_file_text(filename):
    with open(filename, 'r') as file:
        return combine(file.readlines())
        close(file)


# ----------------------------------------- Set Operations -----------------------------------------

# Union set operation
u_greater = lambda x, y: [y[0]] + union(x, y[1:]) if x[0]  > y[0] else []
u_less    = lambda x, y: [x[0]] + union(x[1:], y) if x[0]  < y[0] else []
u_match   = lambda x, y: union(x[1:], y)          if x[0] == y[0] else []
u_compare = lambda x, y: u_greater(x, y) or u_less(x, y) or u_match(x, y)
union     = lambda x, y: x if not y else y if not x else u_compare(x, y)

# Difference set operation
d_greater  = lambda x, y: difference(x, y[1:])          if x[0] >  y[0] else []
d_less     = lambda x, y: [x[0]] + difference(x[1:], y) if x[0] <  y[0] else []
d_match    = lambda x, y: difference(x[1:], y[1:])      if x[0] == y[0] else []
d_compare  = lambda x, y: d_greater(x, y) or d_less(x, y) or d_match(x, y)
difference = lambda x, y: x if not x or not y else d_compare(x,y)

# Intersection set operation
i_greater = lambda x, y: intersect(x, y[1:])              if x[0] >  y[0] else []
i_less    = lambda x, y: intersect(x[1:], y)              if x[0] <  y[0] else []
i_match   = lambda x, y: [x[0]] + intersect(x[1:], y[1:]) if x[0] == y[0] else []
i_compare = lambda x, y: i_greater(x, y) or i_less(x, y) or i_match(x, y)
intersect = lambda x, y: [] if not x or not y else i_compare(x, y)

def perform_operations(set1, set2, operation):
    if operation == 'union': union(set1, set2)
    elif operation == 'difference': difference(set1, set2)
    elif operation == 'intersection': intersect(set1, set2)

# --------------------------------------------------------------------------------------------------

if __name__ == '__main__':
   filename1, filename2, operation = parse_command(sys.argv[1:])
   set1 = sort(list_to_set(read_from_file(filename1)))
   set2 = sort(list_to_set(read_from_file(filename2)))
   perform_operation(set1, set2, operation)