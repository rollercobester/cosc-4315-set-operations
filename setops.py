from os.path import exists
import sys

def print_error(message):
    print('Error: {}'.format(message))
    exit(0)

def print_help():
    print('Call syntax: python3 setops.py "set1=[filename];set2=[filename];operation=[difference|union|intersection]"')
    exit(0)

def parse_command(args):
    
    valid_keys = ('set1', 'set2', 'operation')
    predicates = (
        (lambda x: exists(x),'file \'{}\' does not exist'),
        (lambda x: exists(x), 'file \'{}\' does not exist'),
        (lambda x: x in ('difference', 'union', 'intersection'), 'invalid operation: {}')
    )

    def validate_argument():
        if len(args) == 1: return next(iter(args))
        error_message  = 'too many arguments\n' if args else 'missing argument\n'
        return print_error(error_message)

    def parse_arg(arg):
        if arg in ('-h', '-help', '--h', '--help'): return print_help()
        kwargs = map(lambda x: x.split('='), arg.replace(' ', '').split(';'))
        kwargs = filter(lambda x: x[0] in valid_keys, kwargs)
        return zip(*kwargs)

    def validate_keys(keys):
        missing_key = next(filter(lambda x: x not in keys, valid_keys), None) 
        if not missing_key: return keys
        return print_error('missing keyword argument \'{}\''.format(missing_key))

    def validate_values(values):
    
        def invalidate(assertion):
            value, (predicate, error_message) = assertion
            return not predicate(value)
        
        invalid = next(filter(invalidate, zip(values, predicates)), None)
        if not invalid: return values

        invalid_value, (_, error_message) = invalid
        return print_error(error_message.format(invalid_value))
        
    arg = validate_argument()
    keys, values = parse_arg(arg)
    keys = validate_keys(keys)
    values = validate_values(values)
    return values

def parse_text(filename):
    # TODO
    words = []
    return words

def perform_operation(set1, set2, operation):
    # TODO
    set3 = []
    return set3

def write_to_file(new_set):
    # TODO
    return

if __name__ == '__main__':

    args = tuple(sys.argv[1:])
    filename1, filename2, operation = parse_command(args)
    print(filename1, filename2, operation)
    set1 = parse_text(filename1)
    set2 = parse_text(filename2)
    new_set = perform_operation(set1, set2, operation)
    write_to_file(new_set)
    exit(0)