from functools import reduce
from os.path import exists
import sys

sys.setrecursionlimit(10000)

# ----------------------------------------- UTILS --------------------------------------------------

# Mimics x.split(y) where x is a string
# Ex: split("a b c", ' ') = ["a", "b", "c"]
def split(text, sep):
    i = text.find(sep)
    return [text] if i == -1 else [text[:i]] + split(text[i+1:], sep)

# Mimics x.replace(y, z) where x is a string
# Ex: replace("a b c", ' ', '') = "abc"
def replace(text, old, new):
    i = text.find(old)
    if i == -1: return text
    return text[:i] + new + replace(text[i+len(old):], old, new)

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

list_to_set = lambda x: x if len(x) <= 1 else [x[0]] + list_to_set(x[1:]) if x[0] != x[1] else list_to_set(x[1:])

def word_length_letters(text, length=0):
    head, *tail = text
    word_broke = not head or (not head.isalpha() and head != "'")
    return length if word_broke else word_length_letters(tail, length + 1)

def word_length_numbers(text, length=0, decimal_found=False):
    head, *tail = text
    word_broke = not head or (decimal_found and head == '.') or (not head.isnumeric() and head != '.')
    decimal_found = decimal_found or head == "."
    return length if word_broke else word_length_numbers(tail, length + 1)

# Searches for the next alphanumeric character, finds the words length, returns the word and the remaining text
def find_next_word(text):
    if not text: 
        return '', ''
    elif not text[0].isalnum():
        return find_next_word(text[1:])
    i = word_length_letters(text) if text[0].isalpha() else word_length_numbers(text)
    return text[:i], text[i:]

# Takes a string and recursively finds the next word and builds a list of words
def text_to_words(text):
    word, remaining_text = find_next_word(text)
    return [] if not word else [word] + text_to_words(remaining_text)

def get_file_text(filename):
    with open(filename, 'r') as file:
        return combine(file.readlines())
        close(file)

# ----------------------------------------- Set Operations -----------------------------------------

# Union set operation
def union(set1, set2):
    def compare(set1, set2):
        (x, *set1_others), (y, *set2_others) = set1, set2
        if   x < y: return [x] + union(set1_others, set2)
        elif x > y: return [y] + union(set1, set2_others)
        else:       return [ ] + union(set1_others, set2)
    return set1 if not set2 else set2 if not set1 else compare(set1, set2)

# Difference set operation
def difference(set1, set2):
    def compare(set1, set2):
        (x, *set1_others), (y, *set2_others) = set1, set2
        if   x < y: return [x] + difference(set1_others, set2)
        elif x > y: return [ ] + difference(set1, set2_others)
        else:       return [ ] + difference(set1_others, set2_others)
    return set1 if not set1 or not set2 else compare(set1, set2)

# Intersection set operation
def intersect(set1, set2):
    def compare(set1, set2):
        (x, *set1_others), (y, *set2_others) = set1, set2
        if   x < y: return [ ] + intersect(set1_others, set2)
        elif x > y: return [ ] + intersect(set1, set2_others)
        else:       return [x] + intersect(set1_others, set2_others)
    return [] if not set1 or not set2 else compare(set1, set2)

def perform_operation(set1, set2, operation):
    if operation == 'union': return union(set1, set2)
    elif operation == 'difference': return difference(set1, set2)
    elif operation == 'intersection': return intersect(set1, set2)

# --------------------------------------------------------------------------------------------------

if __name__ == '__main__':
   filename1, filename2, operation = parse_command(sys.argv[1:])
   set1 = list_to_set(sort(text_to_words(get_file_text(filename1))))
   set2 = list_to_set(sort(text_to_words(get_file_text(filename2))))
   print(perform_operation(set1, set2, operation))