from os.path import exists
import sys

# ----------------------------------------- UTILS --------------------------------------------------

# Mimics x.split(y) where x is a string
# Ex: split("a b c", ' ') = ["a", "b", "c"]
splitter = lambda x, y, i: [x] if i == -1 else [x[:i]] + split(x[i+1:], y)
split = lambda x, y: splitter(x, y, x.find(y))

# Mimics x.replace(y, z) where x is a string
# Ex: replace("a b c", ' ', '') = "abc"
replacer = lambda x, y, z: x if x != y else z
replace = lambda x, y, z: x if x == '' else replacer(x[0], y, z) + replace(x[1:], y, z) 

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

# Takes string argument and sends a list of kwargs in the form of "key=value" to be filtered
extract_kwargs = lambda x: filter_kwargs(parse_kwargs(strip_spaces(x)))

# Prints error message for invalid # of args
invalid_args = lambda x: print_error('too many arguments') if x else print_error('not enough arguments')

# Checks for 1 argument and sends it to be parsed into keyword arguments
parse_args = lambda x: extract_kwargs(x[0]) if len(x) == 1 else invalid_args(x)

# Retrieves arguments and sends them to be validated
parse_command = lambda x: parse_args(x)

# ------------------------------------------ File Parser -------------------------------------------

# TODO
sort = lambda x: None

# TODO
read_from_file = lambda x: None

# ----------------------------------------- Set Operations -----------------------------------------

# TODO
union = lambda set1, set2: None

# TODO
difference = lambda set1, set2: None

# TODO
intersection = lambda set1, set2: None

def perform_operations(set1, set2, operation):
    if operation == 'union': union(set1, set2)
    elif operation == 'difference': difference(set1, set2)
    elif operatioin == 'intersection': intersection(set1, set2)

# --------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    filename1, filename2, operation = parse_command(sys.argv[1:])
    set1 = read_from_file(filename1)
    set2 = read_from_file(filename2)
    perform_operation(sort(set1), sort(set2), operation)