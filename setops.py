from os.path import exists
import sys

def print_error(message):
    print('Error: {}'.format(message))
    exit(0)

def parse_command(args):

    if len(args) != 1:
        error_message = 'too many arguments\n' if args else 'missing argument\n'
        error_message += '  Expected:  python3 setops.py "set1=[filename];set2=[filename];operation=[difference|union|intersection]"'
        print_error(error_message)

    kwargs = str(args[0]).split(';')
    kwargs = list(map(lambda x: x.split('='), kwargs))
    set1_kwarg = list(filter(lambda x: x[0] == 'set1', kwargs))
    set2_kwarg = list(filter(lambda x: x[0] == 'set2', kwargs))
    operation_kwarg = list(filter(lambda x: x[0] == 'operation', kwargs))

    if not set1_kwarg:
        print_error('missing keyword argument "{}"'.format('set1'))
    elif not set2_kwarg:
        print_error('missing keyword argument "{}"'.format('set2'))
    elif not operation_kwarg:
        print_error('missing keyword argument "{}"'.format('operation'))

    filename1 = set1_kwarg[0][1]
    filename2 = set2_kwarg[0][1]
    operation = operation_kwarg[0][1]
    valid_operations = ['difference', 'union', 'intersection']

    if not exists(filename1):
        print_error('file "{}" does not exist'.format(filename1))
    elif not exists(filename2):
        print_error('file "{}" does not exist'.format(filename2))
    elif operation not in valid_operations:
        print_error('file: invalid operation')
        print_error('  Valid operations: {}'.format(valid_operations))
    
    return filename1, filename2, operation

def parse_text(file):
    words = []
    return words

def perform_operation(set1, set2):
    set3 = []
    return set3

if __name__ == '__main__':
    file1, file2, operation = parse_command(sys.argv[1:])
    set1 = parse_text(file1)
    set2 = parse_text(file2)
    set3 = perform_operation(set1, set2)
    print('\n'.join(set3))