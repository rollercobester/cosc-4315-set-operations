from functools import reduce
from os.path import exists
from os import listdir
import sys

sys.setrecursionlimit(10000)

# ------------------------------------- COMMAND SPECIFICATIONS ---------------------------------------------

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

# ----------------------------------------- UTILS --------------------------------------------------

def print_error(message):
    print("Error: {}".format(message))
    exit(0)

def print_help():
    print('Call syntax: python3 setops.py set1=[filename];set2=[filename];operation=[difference|union|intersection]"')
    exit(0)

# Splits a string into a list of substrings determined by the separator
# params: text (str), sep (str)
# returns: list of substrings
def split(text, sep):
    i = text.find(sep)
    if i == -1:
        return [text]
    return [text[:i]] + split(text[i+1:], sep)

# Replaces all instances of a certain substring in a string with another string
# params: text (str), old (str), new (str)
def replace(text, old, new):
    i = text.find(old)
    if i == -1:
        return text
    return text[:i] + new + replace(text[i+len(old):], old, new)

combine = lambda x: reduce(lambda a, b: a + b, x)
strip_spaces = lambda x: replace(x, ' ', '')

# ------------------------------------- COMMAND PARSER ---------------------------------------------

# Takes a list of assertions to be made on the kwarg values and validates them
def validate_values(assertions):
    failed_assertion = next(filter(lambda x: not x[1](x[0]), assertions), None)
    if failed_assertion: print_error(failed_assertion[2].format(failed_assertion[0]))
    values = list(zip(*assertions))[0]
    return values

# Takes keys and values and returns a list of value assertions [(value, predicate, error_message), ...]
# Forces the same order as the predefined valid_kwargs
def generate_assertions(keys, values):
    return list(map(lambda x: [values[keys.index(x[0])], x[1], x[2]], valid_kwargs))

# Filters out kwargs with irrelevant keys and sends the rest to be validated
def filter_kwargs(kwargs):
    return list(filter(lambda x: x[0] in valid_keys, kwargs))

# Takes a string of keyword arguments and returns a list of key-value pairs [[key, value], ...]
def parse_kwargs(text):
    return list(map(lambda x: split(x, '='), split(text, ';')))

def parse_command(args):
    if len(args) == 0: print_error("not enough arguments")
    if len(args) >= 2: print_error("too many arguments")
    if args[0] in ['h', 'help', '-h', '-help', '--h', '--help']: print_help()
    kwargs = parse_kwargs(strip_spaces(args[0]))
    keys, values = zip(*filter_kwargs(kwargs))
    missing_key = next(filter(lambda x: x not in keys, valid_keys), None)
    if missing_key: print_error("missing key '{}'".format(missing_key))
    value_assertions = generate_assertions(keys, values)
    return validate_values(value_assertions)

# ------------------------------------------ File Parser -------------------------------------------

def list_to_set(x):
    if len(x) <= 1:    return x
    elif x[0] != x[1]: return [x[0]] + list_to_set(x[1:])
    else:              return list_to_set(x[1:])

def merge_sort(x):
    def merge(l, r):
        if not r:         return l
        elif not l:       return r
        elif l[0] < r[0]: return [l[0]] + merge(l[1:], r)
        else:             return [r[0]] + merge(l, r[1:])
    if len(x) <= 1: return x
    m = len(x) // 2
    return merge(merge_sort(x[:m]), merge_sort(x[m:]))

def word_length_letters(text, length=0):
    if not text: return length
    head, *tail = text
    word_broke = not head or (not head.isalpha() and head != "'")
    return length if word_broke else word_length_letters(tail, length + 1)

def word_length_numbers(text, length=0, decimal_found=False):
    if not text: return length
    head, *tail = text
    non_number_character = (not head.isnumeric() and head != '.')
    second_decimal       = (head == '.' and decimal_found)
    unfollowed_decimal   = (head == '.' and (len(text) == 1 or not text[1].isnumeric()))
    word_broke = not head or non_number_character or second_decimal or unfollowed_decimal
    decimal_found = decimal_found or head == '.'
    return length if word_broke else word_length_numbers(tail, length + 1, decimal_found)

# Searches for the next alphanumeric character, finds the words length, returns the word and the remaining text
def find_next_word(text):
    if not text:
        return '', ''
    elif not text[0].isalnum():
        return find_next_word(text[1:])
    i = word_length_letters(text) or word_length_numbers(text)
    return text[:i], text[i:]

# Takes a string and recursively finds the next word and builds a list of words
def text_to_words(text):
    word, remaining_text = find_next_word(text)
    return [] if not word else [word] + text_to_words(remaining_text)

def to_lowercase(text):
    if not text: return ''
    head, *tail = text
    char = chr(ord(head) + 32) if 'A' <= head <= 'Z' else head
    return char + to_lowercase(tail)

def get_file_text(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        text = combine(file.readlines())
        file.close()
        return text

def write_to_file(wordset):
    output_filenames = list(filter(lambda f: f.startswith("output") and f.endswith(".txt"), listdir()))
    output_numbers = list(map(lambda f: int(f[6:-4]), output_filenames))
    next_number = 1 if not output_filenames else max(output_numbers) + 1
    text = combine(map(lambda word: word + "\n", wordset))
    with open("output{}.txt".format(next_number), "w") as output_file:
        output_file.write(text[:-1])


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
   words1 = text_to_words(to_lowercase(get_file_text(filename1)))
   words2 = text_to_words(to_lowercase(get_file_text(filename2)))
   set1 = list_to_set(merge_sort(words1))
   set2 = list_to_set(merge_sort(words2))
   wordset = perform_operation(set1, set2, operation)
   write_to_file(wordset)